# Open Toontown BR - Docker Setup

This document explains how to run Open Toontown BR using Docker containers.

## Prerequisites

- Docker Engine
- Docker Compose
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/mister-jeperroni/open-toontown-br.git
cd open-toontown-br/docker
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Check the Astron configuration:
```bash
# Review and modify if needed
nano config/astrond.yml
```

4. Build and start services:
```bash
docker compose up -d
```

## Services

The project consists of multiple services:

- **MongoDB**: Database service (optional - you can use your own cluster by specifying the URI in `config/astrond.yml`)
- **Astron**: Message Director and State Server
- **UberDOG**: UberDog Server
- **AI Server**: District Server(s)

## Environment Variables

Create a `.env` file with the following variables:

```plaintext
# Network Configuration
MESSAGE_DIRECTOR_IP=astron:7199
EVENT_LOGGER_IP=astron:7197

# Server Configuration
MAX_CHANNELS=999999
STATE_SERVER=4002
UD_BASE_CHANNEL=1000000
AI_BASE_CHANNEL=401000000

# Authentication
AUTH_METHOD=NO_AUTH  # Options: NO_AUTH, JWT

# Districts
NUM_DISTRICTS=2
```

**Note**: When using `JWT` authentication method, you need to specify the API server in `config/Config.prc`. 
The API server can be found at: https://github.com/mister-jeperroni/open-toontown-br-api

## Common Commands

### Service Management
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Rebuild everything
docker compose build --no-cache
docker compose up -d
```

### Monitoring
```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f astron
docker compose logs -f uberdog
docker compose logs -f ai-server
```

### Cleanup
```bash
# Remove containers, networks, and volumes
docker compose down -v

# Deep clean (removes all unused Docker resources)
docker system prune -a --volumes
```

## Troubleshooting

1. **MongoDB Issues**
   ```bash
   # Check MongoDB status
   docker compose logs mongodb
   ```

2. **Astron Connection Issues**
   ```bash
   # Verify service health
   docker compose ps
   ```

3. **District Server Issues**
   ```bash
   # Check AI server logs
   docker compose logs ai-server
   ```

## Development

To modify the configuration:

1. Environment variables: Edit `.env`
2. Service configuration: Edit `docker-compose.yml`
3. Container builds: Edit Dockerfiles in respective directories

## Notes

- Source code is mounted as read-only in containers
- MongoDB data persists through Docker volumes
- Astron logs are stored in `astron_logs` volume

## Project Structure

```
docker/
├── .env                  # Environment variables
├── .env.example         # Example environment file
├── docker-compose.yml   # Service configuration
├── astron/             # Astron server files
├── uberdog/            # UberDOG server files
└── ai-server/          # AI server files
```