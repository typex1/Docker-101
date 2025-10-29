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
