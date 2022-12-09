from aiohttp import web
from asyncache import cached
from cachetools import TTLCache
from config import config
from dns.asyncresolver import resolve as dns_resolve
from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Timeout
from logger import get_logger

routers = web.RouteTableDef()
logger = get_logger(__name__)


@cached(cache=TTLCache(maxsize=config.cache_max_size, ttl=config.cache_ttl))
async def get_records(domain: str) -> list[str]:
    result = []
    for record in await dns_resolve(domain, "TXT"):
        result.append(record.strings[0].decode())
    return result


async def resolve(domain: str, /, extra: dict) -> str:
    answers = []
    logger.info("Resolving %s", domain)

    try:
        for record in await get_records(domain):
            logger.debug("Found answer: %s", record, extra=extra)
            answers.append(record)
    except NoAnswer:
        result = "No TXT record found"
        logger.info("No answer found for %s", domain, extra=extra)
    except NXDOMAIN:
        result = "No such domain"
        logger.info("No such domain: %s", domain, extra=extra)
    except NoNameservers:
        result = "No nameservers found"
        logger.info("No nameservers found for %s", domain, extra=extra)
    except Timeout:
        result = "Timeout"
        logger.warning("Timeout while resolving %s", domain, extra=extra)
    except Exception as e:
        result = "Unknown error"
        logger.error("Unknown error while resolving %s: %s", domain, e, extra=extra)
    else:
        result = "\n\n".join(sorted(answers))

    return result


@routers.get("/")
async def index(request: web.Request) -> web.Response:
    domain = request.query.get("domain") if config.debug else request.host
    extra = {
        "domain": domain,
        "ip": request.remote,
        "user_agent": request.headers.get("User-Agent"),
        "referrer": request.headers.get("Referer"),
        "method": request.method,
    }
    if not domain:
        logger.warning("No domain provided", extra=extra)
        return web.Response(status=400, text="Bad request", content_type="text/plain")
    return web.Response(content_type="text/plain", text=await resolve(domain, extra=extra))


app = web.Application(logger=logger)
app.add_routes(routers)

if __name__ == "__main__":
    web.run_app(app)
