import os
import tarfile


class BulkBlockBuilderBase:
    # Todo: checksum
    def __init__(self, data_path, gather,):
        self.data_path = data_path
        self.gather = gather

    def bk2_exists(self):
        return os.path.exists(os.path.join(self.data_path, f"{self.gather.symbol.lower()}.bk2"))

    def build_bk2(self, overwrite=True):
        if overwrite or not self.bk2_exists():
            with tarfile.open(os.path.join(self.data_path, f"{self.gather.symbol.lower()}.bk2"), "w") as tar_out:
                for bkdata in sorted([f for f in os.listdir(self.data_path) if f[-7:] == ".bkdata"]):
                    tar_out.add(os.path.join(self.data_path, bkdata), arcname=bkdata)
