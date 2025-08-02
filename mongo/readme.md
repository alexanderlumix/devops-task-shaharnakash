# Shahar Mongo task

# Steps 

## Check what by running exists configuration

```
docker-compose up -d
```
## Check running status

```
docker-compose ps
```

## Enter logs of restarting docker

Fix mongo port `MONGO_PORT` env.

## Rerun the docker compose

Got from logs that have security issue with `mongo-keyfile`

## The fix 

```
chmod 600 mongo-keyfile
```