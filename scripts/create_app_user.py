import pymongo

MONGO_HOST = '127.0.0.1'
ADMIN_USER = 'mongo-0'
ADMIN_PASS = 'mongo-0'

APP_DB = 'appdb'
APP_USER = 'appuser'
APP_PASS = 'appuserpassword'

def find_primary():
    """Find the current primary node by checking all nodes"""
    mongo_ports = [27030, 27031, 27032]
    
    for port in mongo_ports:
        try:
            print(f"🔍 Checking node on port {port}...")
            uri = f"mongodb://{ADMIN_USER}:{ADMIN_PASS}@{MONGO_HOST}:{port}/admin?directConnection=true&authSource=admin"
            client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=3000)
            
            # Check if this node is primary
            result = client.admin.command('isMaster')
            if result.get('ismaster', False):
                print(f"✅ Found primary on port {port}")
                client.close()
                return port
            else:
                print(f"⚠️ Port {port} is secondary")
                client.close()
                
        except Exception as e:
            print(f"❌ Port {port} failed: {str(e)[:50]}...")
            continue
    
    raise Exception("❌ Could not find any primary node")

def create_app_user():
    # First, find the current primary
    primary_port = find_primary()
    
    # Connect directly to the primary
    uri = f"mongodb://{ADMIN_USER}:{ADMIN_PASS}@{MONGO_HOST}:{primary_port}/admin?directConnection=true&authSource=admin"
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    print(f"🚀 Connected to primary on port {primary_port}")
    db = client[APP_DB]
    try:
        db.command("createUser", APP_USER,
                   pwd=APP_PASS,
                   roles=[{"role": "readWrite", "db": APP_DB}])
        print(f"User '{APP_USER}' created with readWrite role on database '{APP_DB}'.")
    except pymongo.errors.OperationFailure as e:
        if 'already exists' in str(e):
            print(f"User '{APP_USER}' already exists.")
        else:
            print(f"Failed to create user: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    create_app_user()
