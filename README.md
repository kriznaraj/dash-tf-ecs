# Dash Docker ECS



## Build and run

```sh
docker build -t dash .

docker run -p 8050:8050 \
-v "$(pwd)"/app:/app \
--rm dash
```

## Access the page

Go to `http://localhost:8050` in browser.

## Switch debug mode in Dockerfile

```dockerfile
ENV DASH_DEBUG_MODE True # False
```

## Development

Install the app requirements for development to get better editor support.

```sh
pipenv install -r app/requirements.txt
```


## Deploy in AWS ECS

```sh
terraform apply
```
