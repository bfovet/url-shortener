# url-shortener

Using FastAPI, MongoDB (Beanie for interacting with it), Redis

https://blog.devops.dev/fastapi-shortener-with-mongodb-and-redis-bed14e110a3c
https://github.com/arturocuicas/fastapi_shortener/tree/main


API:
- get a short url given a long url
- redirect to the long url given a short url


Observability:
- logfire : https://logfire.pydantic.dev/docs/integrations/web-frameworks/fastapi/
- apitally: https://apitally.io/#pricing

https://github.com/blueswen/fastapi-observability
https://last9.io/blog/integrating-opentelemetry-with-fastapi/
https://medium.com/@yoosufpusaleem/building-high-performance-ai-applications-with-fastapi-a-complete-observability-setup-with-ec2df556cb42




https://github.com/dynaconf/dynaconf


TODO:
- logging
- Split shorten and redirect services
- Dockerfile
- add action to deploy to AWS ECS + Fargate
- Terraform
- unit tests with mock
