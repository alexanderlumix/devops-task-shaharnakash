# Python 

## Steps

## run exists code

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

## run command

```
python init_mongo_servers.py
```

Found `Collection [local.oplog.rs] not found`

## Fix configuration

Remove backup on `haproxy.cfg` to allow HA.

Reinitialized replicaset.

## Fix rs_config

Use container mongo name

## Fix create user to run on primary node

## Create script to fix replica hostnames