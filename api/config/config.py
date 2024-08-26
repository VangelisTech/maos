import os
from dotenv import load_dotenv
import httpx
import daft
import ray
from unitycatalog import AsyncUnitycatalog, DefaultHttpxClient
from typing import Optional

load_dotenv()

class Config:
    _instance: Optional['Config'] = None

    def __init__(self):
        self._unity_catalog = None
        self._daft = None
        self._ray = None

    @classmethod
    def get_instance(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def unity_catalog(self) -> AsyncUnitycatalog:
        if self._unity_catalog is None:
            UNITY_CATALOG_URL = os.environ.get("UNITY_CATALOG_URL")
            UNITY_CATALOG_TOKEN = os.environ.get("UNITY_CATALOG_TOKEN")
            self._unity_catalog = AsyncUnitycatalog(
                base_url=UNITY_CATALOG_URL,
                token=UNITY_CATALOG_TOKEN,
                timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
                http_client=DefaultHttpxClient(
                    proxies=os.environ.get("HTTP_PROXY"),
                    transport=httpx.HTTPTransport(local_address="0.0.0.0"),
                ),
            )
        return self._unity_catalog

    def ray(self) -> ray:
        if self._ray is None:
            RAY_RUNNER_HEAD = os.environ.get("RAY_RUNNER_HEAD")
            ray.init(RAY_RUNNER_HEAD, runtime_env={"pip": ["getdaft"]})
            self._ray = ray
        return self._ray

    def daft(self) -> daft:
        if self._daft is None:
            RAY_RUNNER_HEAD = os.environ.get("RAY_RUNNER_HEAD")
            self._daft = daft.context.set_runner_ray(RAY_RUNNER_HEAD)
        return self._daft

config = Config.get_instance()