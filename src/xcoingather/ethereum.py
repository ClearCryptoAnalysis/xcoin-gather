from json import JSONDecodeError
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
        except JSONDecodeError:
            return "\n"


class EthereumBK2Builder(BulkBlockBuilderBase):
    def __init__(self, data_path, gather_path=""):
        self.gather = GatherDataEthereum(gather_path)
        super().__init__(data_path, self.gather)
