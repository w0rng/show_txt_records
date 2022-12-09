from typing import Tuple, Union

from aiohttp import web
from asyncache import cached
from cachetools import TTLCache
from config import config
from dns.asyncresolver import resolve as dns_resolve
from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers, Timeout
from logger import get_logger
from redis_cache import cache_redis

routers = web.RouteTableDef()
logger = get_logger(__name__)


@cached(cache=TTLCache(maxsize=config.cache_max_size, ttl=config.cache_ttl))
async def get_records(domain: str) -> list[str]:
    result = []
    for record in await dns_resolve(domain, "TXT"):
        result.append(record.strings[0].decode())
    return result


@cache_redis(ttl=config.cache_ttl)
async def resolve(domain: str, /, extra: dict) -> Tuple[str, int]:
    answers = []
    logger.info("Resolving %s", domain)

    try:
        for record in await get_records(domain):
            logger.debug("Found answer: %s", record, extra=extra)
            answers.append(record)
    except NoAnswer:
        logger.info("No answer found for %s", domain, extra=extra)
        return "No TXT record found", 200
    except NXDOMAIN:
        logger.info("No such domain: %s", domain, extra=extra)
        return "No such domain", 404
    except NoNameservers:
        logger.info("No nameservers found for %s", domain, extra=extra)
        return "No nameservers found", 200
    except Timeout:
        logger.warning("Timeout while resolving %s", domain, extra=extra)
        return "Timeout", 500
    except Exception as e:
        logger.error("Unknown error while resolving %s: %s", domain, e, extra=extra)
        return "Unknown error", 500
    else:
        return "\n\n".join(sorted(answers)), 200


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
    result, status_code = await resolve(domain, extra=extra)
    return web.Response(content_type="text/plain", text=result, status=status_code)


app = web.Application(logger=logger)
app.add_routes(routers)

if __name__ == "__main__":
    web.run_app(app)
