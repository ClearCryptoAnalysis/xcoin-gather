import gzip
import json
import os
import requests

from .blockbuilder import BulkBlockBuilderBase
from .gather import GatherDataBase


class GatherDataEthereum(GatherDataBase):
    def __init__(self, base_dir,):
        super().__init__(
            name="Ethereum",
            abbreviation="ETH",
            base_dir=base_dir,
            data_chunk_properties={
                "chunk_size": 100000,
                "zfill_len": 3,
            }
        )

    @staticmethod
    def get_block_by_number(block_number, session=requests.Session()):
        headers = {"Content-Type": "application/json",}
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), False],
            "id": 420,
        }
        request = session.post(
            "https://rpc.ankr.com/eth/",
            json=payload,
            headers=headers,
        )
        try:
            return request.json()["result"]
        except json.JSONDecodeError:
            return "\n"


class EthereumBK2Builder(BulkBlockBuilderBase):
    def __init__(self, data_path, gather_path=""):
        self.gather = GatherDataEthereum(gather_path)
        super().__init__(data_path, self.gather)

    def validate(self, bkdata_file_name):
        file_path = os.path.join(self.data_path, bkdata_file_name)
        with gzip.open(file_path, "rb") as bkdata_in:
            lines = bkdata_in.readlines()
        invalid_lines = dict()
        for idx, line in enumerate(lines):
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                invalid_lines[idx] = line
        return invalid_lines
