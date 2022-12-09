# ShowTxtRecords

This is a simple script to show the TXT records of a domain.  

## example run
``` bash
docker build . -t showtxtrecords &&
docker run --publish=8080:80 -it showtxtrecords
```

## configuration
The configuration is done via environment variables.

| Variable | Description | Default              |
|----------|-------------|----------------------|
| `DEBUG`  | Debug mode  | `False`              |
| `PORT` | The port to listen on | `80`                 |
| `WORKERS` | The number of workers to use | `cpu_count() * 2 + 1` |
| `CACHE_MAX_SIZE` | The maximum size of the cache | `1024`               |
| `CACHE_TTL` | The time to live of the cache | `600`|
| `REDIS_USE` | Use redis as cache | `False` |
| `REDIS_HOST` | The redis host | `localhost` |
| `REDIS_PORT` | The redis port | `6379` |
| `REDIS_DB` | The redis database | `0` |
| `REDIS_PASSWORD` | The redis password | `None` |
| `REDIS_POOL_SIZE` | The redis pool size | `10` |


## License
This project is licensed under the terms of the MIT license.