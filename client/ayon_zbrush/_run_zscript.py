import os
import asyncio
import logging
import traceback
import sys
from datetime import datetime

from aiohttp_json_rpc import JsonRpcClient

logger = logging.getLogger(__name__)

# Define error log file path
ERROR_LOG_FILE = os.path.join(os.path.dirname(__file__), "error_log.txt")


async def host_tools_widget(launcher_type=None):
    """Connect to WEBSOCKET_URL, call ping() and disconnect."""

    rpc_client = JsonRpcClient()
    ws_port = int(os.environ["WEBSOCKET_URL"].split(":")[-1])
    try:
        await rpc_client.connect("localhost", ws_port)
        await rpc_client.call(launcher_type)
    finally:
        await rpc_client.disconnect()


def main(launcher):
    asyncio.run(host_tools_widget(launcher))
