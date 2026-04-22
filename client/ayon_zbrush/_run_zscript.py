import os
import asyncio

from aiohttp_json_rpc import JsonRpcClient


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
