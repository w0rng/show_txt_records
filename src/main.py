from aiohttp import web
from asyncache import cached
from cachetools import TTLCache
from dns.asyncresolver import resolve as dns_resolve
from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Timeout

routers = web.RouteTableDef()


@cached(cache=TTLCache(maxsize=1024, ttl=600))
async def resolve(domain: str) -> str:
    answers = []

    try:
        for record in await dns_resolve(domain, "TXT"):
            answers.append(record.strings[0].decode())
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
    else:
        result = "\n\n".join(sorted(answers))

    return result


@routers.get("/")
async def index(request: web.Request) -> web.Response:
    domain = request.host
    return web.Response(content_type="text/plain", text=await resolve(domain))


app = web.Application()
app.add_routes(routers)

if __name__ == "__main__":
    web.run_app(app)
