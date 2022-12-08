# ShowTxtRecords

This is a simple script to show the TXT records of a domain.  

## example run
``` bash
docker build . -t showtxtrecords &&
docker run --publish=8080:80 -it showtxtrecords
```

## configuration
The configuration is done via environment variables.

| Variable | Description | Default |
|----------|-------------|--------|
| `PORT` | The port to listen on | `80` |
| `WORKERS` | The number of workers to use | `cpu_count() * 2 + 1` |


## License
This project is licensed under the terms of the MIT license.