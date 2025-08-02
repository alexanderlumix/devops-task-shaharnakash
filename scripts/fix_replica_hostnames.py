#!/usr/bin/env python3

import pymongo
import sys

def fix_replica_hostnames():
    """Fix replica set configuration to use container hostnames instead of 127.0.0.1"""
    try:
        # Connect to mongo-0 using direct connection
        uri = "mongodb://mongo-0:mongo-0@127.0.0.1:27030/admin?directConnection=true&authSource=admin"
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=10000)
        
        print("Connected to mongo-0, checking replica set configuration...")
        
        # Get current replica set configuration
        current_config = client.admin.command('replSetGetConfig')
        rs_config = current_config['config']
        
        print("Current configuration:")
        for i, member in enumerate(rs_config['members']):
            print(f"  Member {i}: {member['host']}")
        
        # Update hostnames to use container names
        rs_config['members'][0]['host'] = 'mongo-0:27030'
        rs_config['members'][1]['host'] = 'mongo-1:27031'
        rs_config['members'][2]['host'] = 'mongo-2:27032'
        
        # Increment version for reconfiguration
        rs_config['version'] += 1
        
        print("\nUpdated configuration:")
        for i, member in enumerate(rs_config['members']):
            print(f"  Member {i}: {member['host']}")
        
        # Apply the reconfiguration with force=True
        print("\nApplying reconfiguration...")
        result = client.admin.command('replSetReconfig', rs_config, force=True)
        
        if result.get('ok') == 1:
            print("✅ Replica set reconfigured successfully!")
            print("Waiting for replica set to stabilize...")
            
            # Wait a moment and check status
            import time
            time.sleep(5)
            
            try:
                status = client.admin.command('replSetGetStatus')
                print(f"Replica set '{status['set']}' status:")
                for member in status['members']:
                    print(f"  {member['name']}: {member['stateStr']}")
            except Exception as status_error:
                print(f"Note: Could not get status immediately: {status_error}")
                print("This is normal during reconfiguration - the replica set needs time to stabilize.")
        else:
            print(f"❌ Reconfiguration failed: {result}")
            
    except pymongo.errors.OperationFailure as e:
        print(f"❌ MongoDB operation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection or other error: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == '__main__':
    fix_replica_hostnames()