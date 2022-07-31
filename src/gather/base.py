import abc
import gzip
import json
import os
import requests
import time


class DataChunk(abc.ABC):
    def __init__(self, gather, data_chunk_index, chunk_size, base_dir, zfill_len=3):
        self.gather = gather
        self.data_chunk_index = data_chunk_index
        self.min_chunk = self.data_chunk_index * chunk_size
        self.max_chunk = (self.data_chunk_index + 1) * chunk_size

        self.base_dir = base_dir
        self.file_name =\
            f"{self.gather.symbol.lower()}-{str(self.data_chunk_index).zfill(zfill_len)}.bkdata"
        self.full_path = os.path.join(self.base_dir, self.file_name)

        self.data = ""

    def _genesis(self, overwrite=True):
        try:
            open(self.full_path, "x")
        except FileExistsError:
            if overwrite:
                os.remove(self.full_path)
                open(self.full_path, "x")

    def _get_data(self, procpool, skip_sleep=False):
        with procpool:
            for chunk in range(self.min_chunk, self.max_chunk, 1000):
                new_data_chunk = procpool.imap(
                    self.gather.get_block_by_number,
                    range(chunk, chunk + 1000),
                )
                with gzip.open(self.full_path, "ab") as file_out:
                    lines = ("\n".join(
                        [json.dumps(b) for b in new_data_chunk]
                    ) + "\n").encode("utf-8")
                self.data = lines
                if not skip_sleep:
                    time.sleep(5)

    def get(self, procpool, overwrite=False, skip_sleep=False):
        if self.data != "":
            return self.data
        self._genesis(overwrite=overwrite)
        self._get_data(procpool, skip_sleep=skip_sleep)


class GatherDataBase(abc.ABC):
    def __init__(self, name, abbreviation, base_dir, data_chunk_properties):
        self.name = name
        self.symbol = abbreviation
        self.base_dir = os.path.join(base_dir, self.symbol.lower())
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        self.data_chunk_properties = data_chunk_properties
        self.data = dict()

    @staticmethod
    @abc.abstractmethod
    def get_block_by_number(block_number, session=requests.Session()):
        ...

    def gather_chunk(self, data_chunk_index, procpool, overwrite=True, skip_sleep=False):
        new_chunk = DataChunk(
            gather=self,
            data_chunk_index=data_chunk_index,
            base_dir=self.base_dir,
            **self.data_chunk_properties
        )
        new_chunk.get(procpool, overwrite=overwrite, skip_sleep=skip_sleep)
        self.data[data_chunk_index] = self

