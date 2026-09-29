import asyncio

import aiocoap
from aiocoap import Context
from aiocoap import resource


class StatusResource(resource.Resource):
    async def render_get(self, request):
        return aiocoap.Message(
            payload=b"MES CoAP server is running"
        )


async def main():
    root = resource.Site()

    root.add_resource(
        ["status"],
        StatusResource(),
    )

    root.add_resource(
        [".well-known", "core"],
        resource.WKCResource(root.get_resources_as_linkheader),
    )

    await Context.create_server_context(root)

    print("MES CoAP server listening on UDP port 5683")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
