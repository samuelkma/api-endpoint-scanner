# tests/conftest.py
import asyncio
from multiprocessing import Process

import pytest
import uvicorn

from tests.dummy_app import app


@pytest.fixture(scope="session", autouse=True)
def _run_dummy_server():
    """Spin up FastAPI once per test session on 127.0.0.1:8000."""
    process = Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={
            "host": "127.0.0.1",
            "port": 8000,
            "log_level": "warning",
            "access_log": False,
        },
        daemon=True,
    )
    process.start()
    # Give Uvicorn a moment to bind the socket
    asyncio.run(asyncio.sleep(0.3))
    yield
    process.terminate()
    process.join()
