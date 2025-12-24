# Become a QuantumHarmony Validator

This guide explains how to join the QuantumHarmony testnet as a validator.

## Overview

QuantumHarmony uses **governance-based validator admission**. New validators must be approved by existing validators before they can produce blocks.

**Process:**
1. Run your node and sync with the network
2. Generate your unique SPHINCS+ session key
3. Submit your public key for governance approval
4. Wait for validator vote (typically 24-48 hours)
5. After approval, you'll become active at the next session rotation

---

## Step 1: Start Your Node

```bash
git clone https://github.com/Paraxiom/quantum-harmony-node.git
cd quantum-harmony-node
./start.sh
```

Wait for your node to sync. Check the dashboard at http://localhost:8080

**Sync Status:**
- Block height should match the network (~increasing every 6 seconds)
- "Syncing: No" means you're caught up
- 2-3 peers connected is normal

---

## Step 2: Generate Session Key

### Option A: Via Dashboard (Recommended)

1. Open http://localhost:8080
2. Go to **Key Management** section
3. Click **Generate New Key**
4. Copy your **Session Key** (64-byte public key starting with `0x`)

### Option B: Via RPC

```bash
curl -s http://localhost:9944 \
  -H "Content-Type: application/json" \
  -d '{"id":1,"jsonrpc":"2.0","method":"author_rotateKeys","params":[]}' \
  | jq -r '.result'
```

**Important:** Your secret key is automatically stored in the node's keystore. Never share your secret key.

---

## Step 3: Request Validator Status

Email your public session key to: **sylvain@paraxiom.org**

Include:
- Your session key (the 0x... public key from Step 2)
- Your node name (optional)
- Your location/provider (optional, helps with geographic distribution)

**Example email:**
```
Subject: QuantumHarmony Validator Request

Session Key: 0xa35fcf7e9fcace0d218088b1b25f86d68814541e6037297b64d3e467a1528dad28b28b8c24a599997d2267122a52b27b9c1ea7c991201d22eaf3d466d6ab8458

Node Name: MyValidator
Location: AWS us-east-1
```

---

## Step 4: Governance Vote

After receiving your request:

1. A governance proposal is created with your public key
2. Existing validators vote on the proposal (voting period: ~10 blocks)
3. If approved (majority yes votes), your key is added to the pending validator set

You'll receive confirmation when approved.

---

## Step 5: Activation

After governance approval, your validator activates at the **next session rotation**.

- Sessions rotate every ~6 hours
- Check your logs for: `Number of authorities: 4` (or higher)
- When active, you'll see: `Claimed slot for block #XXX`

**Verify you're active:**
```bash
docker logs quantumharmony-node 2>&1 | grep "Claimed slot"
```

---

## Troubleshooting

### "Key not found in keystore"
This is **normal** until your validator is activated. It means:
- Your node is checking if it should author blocks
- Your key isn't in the active set yet
- Wait for session rotation after governance approval

### Node not syncing
- Check peers: `curl http://localhost:9944 -d '{"id":1,"jsonrpc":"2.0","method":"system_health"}'`
- Ensure port 30333 is open for P2P
- Try restarting: `docker-compose restart node`

### Genesis mismatch
If your genesis hash doesn't match the network:
```bash
git pull
docker-compose down -v
./start.sh
```

---

## Current Network

**Production Validators:**
| Validator | Location | Status |
|-----------|----------|--------|
| Validator 1 | Montreal, CA | Active |
| Validator 2 | Beauharnois, CA | Active |
| Validator 3 | Frankfurt, DE | Active |

**Genesis Hash:** `0xc18cc638862625ae46879052e3fcff864a1ae408a8166b65934ce7e153b8b5e1`

---

## Questions?

- GitHub Issues: https://github.com/Paraxiom/quantum-harmony-node/issues
- Email: sylvain@paraxiom.org
