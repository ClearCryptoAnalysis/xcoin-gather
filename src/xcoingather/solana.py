from json import JSONDecodeError
import requests

from .gather import GatherDataBase


class GatherDataSolana(GatherDataBase):
    def __init__(self, base_dir,):
        super().__init__(
            name="Solana",
            abbreviation="SOL",
            base_dir=base_dir,
            data_chunk_properties={
                "chunk_size": 100000,
                "zfill_len": 4,
            }
        )

    @staticmethod
    def get_block_by_number(block_number, session=requests.Session()):
        headers = {"Content-Type": "application/json",}
        payload = {
            "jsonrpc": "2.0",
            "method": "getBlock",
            "params": [block_number, {"transactionDetails": "signatures"}],
            "id": 69420,
        }
        request = session.post(
            "https://rpc.ankr.com/solana",
            json=payload,
            headers=headers,
            proxies={
                "http": "socks5://149.56.96.252:9300"
            },
        )
        try:
            return request.json()
        except JSONDecodeError:
            return "\n"
