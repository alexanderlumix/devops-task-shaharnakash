const { MongoClient } = require('mongodb');

// Array of all MongoDB nodes for smart primary detection
const mongoNodes = [
  { host: '127.0.0.1', port: 27030, name: 'mongo-0' },
  { host: '127.0.0.1', port: 27031, name: 'mongo-1' }, 
  { host: '127.0.0.1', port: 27032, name: 'mongo-2' }
];

async function findPrimaryNode() {
  console.log('🔍 Finding current primary node...');
  
  for (const node of mongoNodes) {
    try {
      // Try to connect to each node with admin credentials to check status
      const adminUri = `mongodb://mongo-0:mongo-0@${node.host}:${node.port}/admin?directConnection=true&authSource=admin`;
      const adminClient = new MongoClient(adminUri, { 
        serverSelectionTimeoutMS: 3000 
      });
      
      await adminClient.connect();
      const status = await adminClient.db('admin').command({ replSetGetStatus: 1 });
      await adminClient.close();
      
      // Find the primary in the replica set status
      const primaryMember = status.members.find(member => member.stateStr === 'PRIMARY');
      if (primaryMember) {
        console.log(`✅ Found primary: ${primaryMember.name}`);
        
        // Match the primary name to our node list
        const primaryPort = primaryMember.name.split(':')[1];
        const primaryNode = mongoNodes.find(n => n.port.toString() === primaryPort);
        return primaryNode;
      }
    } catch (err) {
      console.log(`⚠️  Could not check ${node.name}: ${err.message}`);
      continue;
    }
  }
  
  throw new Error('❌ Could not find any primary node');
}

async function connectToPrimary() {
  const primaryNode = await findPrimaryNode();
  
  // Connect to the identified primary with app credentials
  const appUri = `mongodb://appuser:appuserpassword@${primaryNode.host}:${primaryNode.port}/appdb?directConnection=true&authSource=appdb`;
  const client = new MongoClient(appUri, { 
    useUnifiedTopology: true,
    retryWrites: true 
  });
  
  console.log(`🚀 Connected to primary: ${primaryNode.name} (port ${primaryNode.port})`);
  return { client, primaryNode };
}

async function run() {
  try {
    const { client, primaryNode } = await connectToPrimary();
    
    await client.connect();
    const db = client.db('appdb');
    const products = db.collection('products');
    
    const randomName = 'Product_' + Math.random().toString(36).substring(2, 10);
    const result = await products.insertOne({ 
      name: randomName, 
      createdAt: new Date(),
      insertedVia: 'smart-primary-detection',
      primaryUsed: primaryNode.name
    });
    
    console.log('✅ Successfully inserted product:', result.insertedId, 'with name:', randomName);
    
    await client.close();
    
  } catch (err) {
    console.error('❌ Error:', err.message);
    
    if (err.message.includes('not primary')) {
      console.log('🔄 Primary changed during operation, please retry');
    }
  }
}

run();
