from aiohttp import web
from dns.asyncresolver import resolve as dns_resolve

routers = web.RouteTableDef()


@routers.get("/")
async def index(request: web.Request) -> web.Response:
    # get domain name from request
    result = ""

    for record in await dns_resolve(request.host, "TXT"):
        result += record.strings[0].decode() + "\n"
    return web.Response(content_type="text/plain", text=result)


app = web.Application()
app.add_routes(routers)

if __name__ == "__main__":
    web.run_app(app)
