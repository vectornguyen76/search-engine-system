# Set Up SSL Certificate on Ubuntu Server

This guide provides instructions for setting up an SSL certificate on an Ubuntu Server using Docker, Nginx, and Certbot.

## Prerequisites

- Docker and Docker Compose installed
- Ubuntu Server with sudo privileges
- Domain name pointing to your server's IP address

## Steps

### 1. Build Docker Image

```bash
docker compose build
```

### 2. Update and Upgrade Ubuntu Packages

```bash
sudo apt-get update
sudo apt-get upgrade
```

### 3. Create Directories for Certificates

```bash
mkdir -p certificates
mkdir -p certificates/bot
```

### 4. Initialize Temporary Self-Signed Certificate

Generate a temporary self-signed certificate to ensure Nginx runs initially.

```bash
cd certificates
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout privkey.pem -out fullchain.pem
cd ..
```

### 5. Copy Configuration Files to Server

Place your `default.conf` and `docker-compose.yaml` in the project's root directory.

### 6. Start Application

```bash
docker compose up -d
```

### 7. Install Certbot

```bash
sudo apt install certbot
```

### 8. Generate Let's Encrypt Certificate

Replace `[PATH]` with your certificates directory path and `[DOMAIN_NAME]` with your domain name.

```bash
sudo certbot certonly --webroot -w [PATH]/certificates/bot -d [DOMAIN_NAME]
```

Example:

```bash
sudo certbot certonly --webroot -w /home/ubuntu/search-engine-shopee/nginx/certificates/bot -d search.vectornguyen.com
```

### 9. Copy Generated Certificates

Copy the Let's Encrypt certificates to your certificates directory.

```bash
sudo cp /etc/letsencrypt/archive/[DOMAIN_NAME]/fullchain1.pem [PATH]/certificates/fullchain.pem
sudo cp /etc/letsencrypt/archive/[DOMAIN_NAME]/privkey1.pem [PATH]/certificates/privkey.pem
```

Example:

```bash
sudo cp /etc/letsencrypt/archive/search.vectornguyen.com/fullchain1.pem /home/ubuntu/search-engine-shopee/nginx/certificates/fullchain.pem
sudo cp /etc/letsencrypt/archive/search.vectornguyen.com/privkey1.pem /home/ubuntu/search-engine-shopee/nginx/certificates/privkey.pem
```

### 10. Restart Microservice Application

```bash
docker compose restart
```

### 11. Renew Certificates

Regularly renew certificates close to expiration.

```bash
sudo certbot renew
```

## Notes

- Ensure your domain name is correctly configured to point to your server's IP.
- Regularly check for certificate expiration and renew as needed.
