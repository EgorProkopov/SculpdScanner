# SCULPD Scanner

Scanner microservise of SCULPD APP for fitness. 
This microservice is responsible for user photo (scan) description and first training recommendations.


## Prerequisites

- Docker
- 'configs/' directory with all necessary configs
- .env file for local running (with open-ai api key)
- .env.docker file for docker running (with open-ai api key)
- libs from requirements.txt
- open port 8888

## .env file example

``` dotenv
PORT=8888
API_KEY=YOUR_API_KEY_HERE
SCANNER_CONFIG_PATH=/app/configs/scanner_config.yaml
REPORT_PROCESSING_CONFIG_PATH=/app/configs/report_processing_config.yaml
```

## Build and run

```bash
docker-compose build 
docker-compose up -d
```





