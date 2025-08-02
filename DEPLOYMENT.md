# 🚀 MongoDB DevOps Task - Complete Automation Guide

This guide provides a **one-click deployment** solution for the entire MongoDB DevOps stack.

## 📋 What Gets Automated

The `build-and-run.sh` script handles **everything** in the correct order:

### 🏗️ Infrastructure Setup
1. **Prerequisites Check** - Verifies Docker, Node.js, Python are installed
2. **Cleanup** - Removes any existing containers
3. **MongoDB Deployment** - Starts 3-node replica set + HAProxy load balancer
4. **Health Verification** - Waits for containers to be healthy

### ⚙️ MongoDB Configuration  
5. **Python Environment** - Sets up virtual environment with dependencies
6. **Replica Set Initialization** - Configures MongoDB cluster with proper roles
7. **Network Configuration** - Fixes container hostname resolution
8. **Application User Creation** - Creates `appuser` with database permissions
9. **Connection Verification** - Tests database connectivity

### 🚀 Application Deployment
10. **Go Application** - Builds and deploys the product reader service
11. **Node.js Application** - Installs dependencies and tests product creation
12. **Final Status Check** - Verifies all components are working

## 🎯 One-Command Deployment

```bash
# Run the complete automation script
./build-and-run.sh
```

## 📊 What You Get

After successful deployment:

### 🗄️ MongoDB Infrastructure
- **3-node replica set**: `mongo-0`, `mongo-1`, `mongo-2`
- **HAProxy load balancer**: Port 27034
- **Automatic failover**: Primary/secondary roles configured
- **Application user**: `appuser` with `readWrite` permissions

### 📱 Applications  
- **Node.js Writer**: Smart primary detection for reliable writes
- **Go Reader**: Load-balanced reading via HAProxy
- **Auto-resilience**: Both apps handle MongoDB failover

### 🔧 Tools & Scripts
- **Monitoring scripts**: Check replica set status
- **User management**: Create additional database users  
- **Connection testing**: Verify database connectivity

## 🚀 Quick Start

### Prerequisites
```bash
# Verify you have the required tools
docker --version          # Docker Engine
docker-compose --version  # Docker Compose  
python3 --version         # Python 3.x
node --version            # Node.js 14+
```

### Deployment
```bash
# Clone and deploy
git clone <your-repo>
cd devops-task-shaharnakash
./build-and-run.sh
```

### Usage After Deployment
```bash
# Create products (Node.js)
cd app-node && npm run start

# View live product reading (Go)
docker logs product-reader-go -f

# Check replica set status  
cd scripts && source venv/bin/activate && python check_replicaset_status.py

# Monitor containers
docker ps
```

## 🔍 Troubleshooting

### Common Issues

**Script fails at MongoDB initialization:**
```bash
# Check container logs
docker logs mongo-0
docker logs haproxy-lb

# Restart if needed
./build-and-run.sh
```

**Node.js version too old:**
```bash
# Install/update Node.js 18+
nvm install 18
nvm use 18
```

**Permission denied:**
```bash
# Make script executable
chmod +x build-and-run.sh
```

### Manual Steps (if automation fails)

If the automation script fails, you can run steps manually:

```bash
# 1. Start MongoDB
cd mongo && docker-compose up -d

# 2. Setup Python environment  
cd scripts && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 3. Initialize MongoDB
python init_mongo_servers.py
python fix_replica_hostnames.py  
python create_app_user.py

# 4. Start applications
cd ../app-go && docker-compose up -d
cd ../app-node && npm install && npm run start
```

## 🎉 Success Indicators

You'll know everything worked when you see:

✅ **MongoDB**: 3 healthy containers with 1 PRIMARY + 2 SECONDARY  
✅ **HAProxy**: Load balancer routing to healthy nodes  
✅ **Go App**: Reading products every 3 seconds  
✅ **Node.js**: Successfully inserting products with smart primary detection  
✅ **No Errors**: No "oplog.rs not found" or "not primary" errors

## 🛠️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Node.js App   │    │   Go App         │    │   HAProxy LB    │
│ (Smart Primary) │    │ (Load Balanced)  │    │   Port 27034    │
└─────────┬───────┘    └────────┬─────────┘    └─────────┬───────┘
          │                     │                        │
          └─────────────────────┼────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   MongoDB Replica Set  │
                    │                       │
                ┌───┴───┐   ┌───────┐   ┌───┴───┐
                │mongo-0│   │mongo-1│   │mongo-2│
                │  :30  │   │  :31  │   │  :32  │
                │  SEC  │   │  PRI  │   │  SEC  │
                └───────┘   └───────┘   └───────┘
```

## 📝 Notes

- **Production Ready**: Includes proper error handling and health checks
- **Automatic Recovery**: Handles MongoDB primary elections gracefully  
- **Monitoring**: Built-in status checks and logging
- **Scalable**: Easy to add more MongoDB nodes or applications

## 🎯 Mission Accomplished

This automation completely resolves the original issue:
- ❌ **Before**: `Collection [local.oplog.rs] not found`
- ✅ **After**: Fully functional MongoDB replica set with applications

Your DevOps stack is now enterprise-ready! 🚀