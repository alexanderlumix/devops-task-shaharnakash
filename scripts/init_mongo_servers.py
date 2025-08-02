# init_mongo_servers.py
import pymongo
import yaml
import sys

CONFIG_FILE = 'mongo_servers.yml'

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def test_connection(server):
    host = server['host']
    port = server.get('port', 27017)
    user = server['user']
    password = server['password']
    uri = f"mongodb://{user}:{password}@{host}:{port}/admin?directConnection=true"
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print(f"Connected to {host}:{port} as {user} successfully.")
    except Exception as e:
        print(f"Error connecting to {host}:{port} as {user}: {e}")
    finally:
        client.close()

def init_primary(server):
    host = server['host']
    port = server.get('port', 27017)
    user = server['user']
    password = server['password']
    uri = f"mongodb://{user}:{password}@{host}:{port}/admin?directConnection=true"
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        rs_config = {
            '_id': 'rs0',
            'members': [
                {'_id': 0, 'host': 'mongo-0:27030'},
                {'_id': 1, 'host': 'mongo-1:27031'},
                {'_id': 2, 'host': 'mongo-2:27032'},
            ]
        }
        try:
            client.admin.command('replSetInitiate', rs_config)
            print(f"Replica set initiated on {host}:{port}.")
        except Exception as e:
            print(f"Replica set initiation error (may be already initiated): {e}")
    except Exception as e:
        print(f"Error connecting to {host}:{port} as {user}: {e}")
        exit(1)
    finally:
        client.close()

def main():
    config = load_config(CONFIG_FILE)
    # Only test connection to mongo-0 to avoid authentication errors during initialization
    # Note: mongo-0 has the initial admin user from MONGO_INITDB_*, others get it via replication
    primary_server = config['servers'][0]  # mongo-0
    test_connection(primary_server)
    init_primary(primary_server)

if __name__ == '__main__':
    main()
