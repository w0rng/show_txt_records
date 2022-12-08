from aiohttp import web
from dns.asyncresolver import resolve as dns_resolve
from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Timeout

routers = web.RouteTableDef()


@routers.get("/")
async def index(request: web.Request) -> web.Response:
    result = ""

    try:
        for record in await dns_resolve(request.host, "TXT"):
            result += record.strings[0].decode() + "\n\n"
    except NoAnswer:
        result = "No TXT record found"
    except NXDOMAIN:
        result = "No such domain"
    except NoNameservers:
        result = "No nameservers found"
    except Timeout:
        result = "Timeout"
    except:
        result = "Unknown error"
    return web.Response(content_type="text/plain", text=result)


app = web.Application()
app.add_routes(routers)

if __name__ == "__main__":
    web.run_app(app)
