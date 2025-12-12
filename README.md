# QuantumHarmony Node Operator

Run a QuantumHarmony node with one command using Docker.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Paraxiom/quantum-harmony-node.git
cd quantum-harmony-node

# Start everything
docker-compose up -d

# View logs
docker-compose logs -f node
```

Open http://localhost:8080 for the operator dashboard.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  NODE OPERATOR STACK                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌──────────────────┐    ┌──────────────────────────┐  │
│   │  QuantumHarmony  │    │    LCARS Dashboard       │  │
│   │      Node        │    │    (port 8080)           │  │
│   │   (port 9944)    │    └──────────────────────────┘  │
│   └────────┬─────────┘                                   │
│            │                                             │
│   ┌────────▼─────────────────────────────────────────┐  │
│   │              Nginx Reverse Proxy                  │  │
│   │           (ports 80, 443)                         │  │
│   └──────────────────────────────────────────────────┘  │
│                                                          │
├─────────────────────────────────────────────────────────┤
│   SPHINCS+-256s POST-QUANTUM SECURED                     │
└─────────────────────────────────────────────────────────┘
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| node | 9944 | RPC/WebSocket endpoint |
| node | 30333 | P2P networking |
| node | 9615 | Prometheus metrics |
| dashboard | 8080 | Operator web UI |
| nginx | 80/443 | Reverse proxy |

## Dashboard Features

- **Status**: Block height, peers, sync status
- **Blocks**: Recent block explorer
- **Runtime**: Forkless upgrade submission
- **Keys**: Validator key management
- **Quantum**: Post-quantum security status

## Configuration

### Environment Variables

Create a `.env` file:

```bash
NODE_NAME=MyNode
```

### Custom Chain Spec

Replace `configs/chain-spec.json` with your chain spec.

## Network

**Production Testnet Bootnodes:**
- Alice: `51.79.26.123`
- Bob: `51.79.26.168`

**Ports Required:**
- `30333` - P2P (must be open for peers)
- `9944` - RPC (optional, for external access)

## Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View node logs
docker-compose logs -f node

# Restart node only
docker-compose restart node

# Check status
docker-compose ps
```

## Requirements

- Docker
- Docker Compose

## License

Apache-2.0
