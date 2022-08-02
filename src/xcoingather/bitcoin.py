from json import JSONDecodeError
import requests
from string import Template

from .gather import GatherDataBase


class GatherDataBitcoin(GatherDataBase):
    def __init__(self, base_dir,):
        super().__init__(
            name="Bitcoin",
            abbreviation="BTC",
            base_dir=base_dir,
            data_chunk_properties={
                "chunk_size": 10000,
                "zfill_len": 3,
            }
        )

    @staticmethod
    def get_block_by_number(block_number, session=requests.Session()):
        request_template = Template("https://blockchain.info/rawblock/$block_hash?format=json")
        request = session.get(
            request_template.safe_substitute(
                {
                    "block_hash": block_number,
                }
            ),
            headers={},
            proxies={
                "http": "socks5://64.138.255.146:80"
            },
        )
        try:
            return request.json()
        except JSONDecodeError:
            return "\n"
        except ConnectionResetError:
            raise ConnectionResetError(f"block number {block_number}")
