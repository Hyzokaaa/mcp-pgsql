import asyncio

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client
from rich.pretty import pprint

from client_config import server_url

load_dotenv()


async def main():
    async with sse_client(server_url()) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()
            pprint(result.tools)

            #result = await session.call_tool("list_task", arguments={"max_results": 2})
            #pprint(result.content)

if __name__ == "__main__":
    print("Conectando a:", server_url())

    asyncio.run(main())
