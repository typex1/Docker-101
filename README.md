# Docker-101

PartyRock URL: https://partyrock.aws/u/fspiess/tM63Spm3z/Docker-Dockerfile-Generator-and-Deployment-Assistant

Use Case Description (copy & paste):
```
A web server that is listening on port 80, showing a greeting text and
 a random number that changes whenever the webpage is reloaded.
Create a simple solution, without any multi-stage parts.
```
---

Dockerfile Generation:

Here's a production-ready Dockerfile with detailed comments for your web server application:

```dockerfile
# Use official Node.js lightweight image as base
FROM node:18-slim

# Set working directory
WORKDIR /app

# Add non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create simple web server application
RUN echo 'const http = require("http"); \n\
const server = http.createServer((req, res) => { \n\
    res.writeHead(200, {"Content-Type": "text/plain"}); \n\
    res.end(`Hello! Random number: ${Math.random()}\n`); \n\
}); \n\
server.listen(80, "0.0.0.0", () => { \n\
    console.log("Server running on port 80"); \n\
});' > server.js

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 80
EXPOSE 80

# Health check to ensure container is running properly
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:80 || exit 1

# Command to run the application
CMD ["node", "server.js"]
```

Key features and best practices implemented:

1. **Base Image**:
   - Uses official Node.js slim image to minimize container size
   - Node 18 LTS for stability and security updates

2. **Security**:
   - Creates and uses non-root user (appuser)
   - Sets proper file permissions
   - Minimal base image to reduce attack surface

3. **Organization**:
   - Clear working directory structure
   - Proper file ownership

4. **Monitoring**:
   - Includes HEALTHCHECK for container health monitoring
   - Exposes port 80 explicitly

5. **Simplicity**:
   - Single-stage build since it's a simple application
   - Inline application code for this specific use case

---

Build Instructions:

Here's a detailed step-by-step guide for building, testing, tagging, and publishing the Docker image:

1. **Building the Docker Image**
```bash
# Build with proper tags from the start
docker build -t webserver:latest -t webserver:1.0.0 .
```

2. **Testing the Build**
```bash
# Run container in detached mode
docker run -d -p 80:80 --name webserver-test webserver:latest
```
```
# Verify container is running
docker ps
```
```
# Check container logs
docker logs webserver-test
```
```
# Test the application
curl http://localhost:80
```
```
# Test multiple requests to verify random number changes
for i in {1..5}; do curl http://localhost:80; done
```
```
# Check container health
docker inspect --format='{{.State.Health.Status}}' webserver-test
```
```
# Stop test container
docker stop webserver-test
```
```
# Remove test container
docker rm webserver-test
```

3. **Tagging the Image**
```bash
# Add registry-specific tags (example using Docker Hub)
docker tag webserver:latest yourusername/webserver:latest
docker tag webserver:1.0.0 yourusername/webserver:1.0.0

# Add additional tags for better versioning
docker tag webserver:latest yourusername/webserver:$(date +%Y%m%d)
```

4. **Publishing to Container Registry**
```bash
# Login to registry (example using Docker Hub)
docker login

# Push all tags
docker push yourusername/webserver:latest
docker push yourusername/webserver:1.0.0
docker push yourusername/webserver:$(date +%Y%m%d)

# Verify push
docker pull yourusername/webserver:latest
```

Best Practices:

1. **Version Control**
- Always use specific version tags (not just `latest`)
- Include date-based tags for tracking
- Use semantic versioning (major.minor.patch)

2. **Security**
- Scan images for vulnerabilities before pushing
- Use `--no-cache` when building production images
- Implement content trust: `export DOCKER_CONTENT_TRUST=1`

3. **Testing**
- Test the container in isolation
- Verify all exposed ports
- Check logs for errors
- Validate healthcheck functionality
- Test application functionality

4. **Registry Management**
- Use private registries for production images
- Implement registry access controls
- Clean up old/unused tags regularly

5. **Documentation**
```bash
# Create image documentation
echo "# Webserver Image
Version: 1.0.0
Description: Simple Node.js web server showing random numbers
Usage: docker run -p 80:80 yourusername/webserver:1.0.0" > README.md
```

6. **Automation Script Example**
```bash
#!/bin/bash
set -e

VERSION="1.0.0"
REGISTRY="yourusername"
IMAGE="webserver"

# Build
docker build --no-cache --pull -t $IMAGE:$VERSION .

# Test
docker run -d -p 80:80 --name test-$IMAGE $IMAGE:$VERSION
sleep 5
curl -f http://localhost:80 || exit 1
docker stop test-$IMAGE
docker rm test-$IMAGE

# Tag
docker tag $IMAGE:$VERSION $REGISTRY/$IMAGE:$VERSION
docker tag $IMAGE:$VERSION $REGISTRY/$IMAGE:latest

# Push
docker push $REGISTRY/$IMAGE:$VERSION
docker push $REGISTRY/$IMAGE:latest

echo "Successfully built, tested and pushed $REGISTRY/$IMAGE:$VERSION"
```

Save this as `build-and-publish.sh` and run:
```bash
chmod +x build-and-publish.sh
./build-and-publish.sh
```

---

Deployment Guide:

Here's a comprehensive deployment guide for your web server application:

# Deployment Guide for Random Number Web Server

## 1. Prerequisites and Environment Setup

### System Requirements:
- Docker Engine 20.10.x or newer
- Minimum 512MB RAM
- 1GB free disk space
- Internet connectivity for pulling images

### Installation Steps:
```bash
# Install Docker (Ubuntu)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

## 2. Container Deployment

### Pull and Run Commands:
```bash
# Build the image
docker build -t webserver:latest .

# Run the container
docker run -d \
  --name random-webserver \
  -p 80:80 \
  --restart unless-stopped \
  webserver:latest
```

## 3. Environment Variables

While this application doesn't require environment variables, you can set them if needed:
```bash
# Example with optional environment variables
docker run -d \
  --name random-webserver \
  -p 80:80 \
  -e NODE_ENV=production \
  webserver:latest
```

## 4. Network and Port Configuration

### Port Mapping:
- Internal port: 80
- Default external port: 80

### Custom Port Mapping:
```bash
# Map to different external port (e.g., 8080)
docker run -d --name random-webserver -p 8080:80 webserver:latest
```

### Network Creation (Optional):
```bash
# Create dedicated network
docker network create webserver-net

# Run container in network
docker run -d \
  --name random-webserver \
  --network webserver-net \
  -p 80:80 \
  webserver:latest
```

## 5. Container Health Monitoring

### Check Container Status:
```bash
# View container status
docker ps -a

# View container logs
docker logs random-webserver

# View health check status
docker inspect --format='{{.State.Health.Status}}' random-webserver
```

### Monitor Resource Usage:
```bash
# View container statistics
docker stats random-webserver
```

## 6. Troubleshooting

### Common Issues and Solutions:

1. **Container Won't Start:**
```bash
# Check logs for errors
docker logs random-webserver

# Verify port availability
sudo lsof -i :80
```

2. **Port Conflicts:**
```bash
# Kill process using port 80
sudo fuser -k 80/tcp

# Use alternative port
docker run -d --name random-webserver -p 8080:80 webserver:latest
```

3. **Container Crashes:**
```bash
# Check container logs
docker logs random-webserver

# Restart container
docker restart random-webserver
```

4. **Performance Issues:**
```bash
# Monitor resource usage
docker stats random-webserver

# Check system resources
free -m
df -h
```

### Verification Steps:
```bash
# Test web server
curl http://localhost:80

# Verify container is running
docker ps | grep random-webserver

# Check container health
docker inspect random-webserver | grep Health
```

## Additional Commands

### Container Management:
```bash
# Stop container
docker stop random-webserver

# Remove container
docker rm random-webserver

# Remove image
docker rmi webserver:latest
```

### Backup Container:
```bash
# Create image backup
docker save webserver:latest > webserver-backup.tar

# Load backup
docker load < webserver-backup.tar
```

Remember to:
- Regularly monitor container logs
- Keep Docker Engine updated
- Implement proper backup strategies
- Monitor system resources
- Follow security best practices

For production deployments, consider:
- Setting up container orchestration (e.g., Kubernetes)
- Implementing proper logging solutions
- Setting up monitoring and alerting
- Implementing SSL/TLS
- Regular security audits

---

Check on the commandline:

$ curl http://localhost/

Hello! Random number: 0.5057827207036754
