# QuantumHarmony Node

Run a QuantumHarmony node with one command.

## Quick Start

```bash
./start.sh
```

This opens the dashboard at http://localhost:9955 where you can:
- **START** / **STOP** / **RESTART** your node
- Monitor block height, peers, sync status
- View node logs

## Requirements

- Python 3
- `quantumharmony-node` binary in this directory

## Manual Start

```bash
python3 dashboard/run.py
```

## Network

**Bootnodes:**
- Alice: `51.79.26.123`
- Bob: `51.79.26.168`

**Ports:**
- `9944` - RPC
- `30333` - P2P

## License

Apache-2.0
