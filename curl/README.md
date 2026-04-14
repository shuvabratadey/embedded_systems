# 🌐 Networking & CLI Cheat Sheet

A comprehensive reference guide for common networking tools, protocols, and command-line utilities used in development, testing, and system administration.

---

## 📋 Table of Contents

- [cURL](#curl)
  - [GET Requests](#get-requests)
  - [POST Requests](#post-requests)
  - [File Operations](#file-operations)
  - [FTP Upload](#ftp-upload)
  - [MQTT](#mqtt)
  - [Other Useful Options](#other-useful-curl-options)
- [NMAP](#nmap)
- [Test-NetConnection (PowerShell)](#test-netconnection-powershell)
- [TraceRoute](#traceroute)
- [OpenSSL](#openssl)
- [SSH](#ssh)
- [SCP](#scp)
- [Testing Tools](#testing-tools)

---

## cURL

### GET Requests

```bash
# Basic GET request
curl https://example.com/

# Get current time for a timezone
curl "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata"
```

---

### POST Requests

```bash
# Send form data
curl -X POST https://your-endpoint.com/webhook -d "field1=value1&field2=value2"

# Send JSON payload
curl -X POST -H "Content-Type: application/json" \
  https://your-endpoint.com/webhook \
  -d '{"key": "value", "id": 12345}'

# Send a file (multipart form)
curl -X POST https://your-endpoint.com/webhook -F "data=@image.jpg"
```

---

### File Operations

```bash
# Save response output to a file
curl -o output.html https://example.com

# Download a file keeping its original name
curl -O https://example.com/file.zip

# Check response headers only (no body)
curl -I https://example.com

# Verbose output for debugging
curl -v https://example.com
```

---

### FTP Upload

```bash
# Upload a file to an FTP server
curl -k -T yourfile.jpg ftp://USERNAME:PASSWORD@ftp.yourserver.com/htdocs/uploads/

# View uploaded files via File Explorer (Windows) — paste in address bar:
# ftp://USERNAME:PASSWORD@ftp.yourserver.com/htdocs/
```

> 💡 Replace `USERNAME`, `PASSWORD`, and `ftp.yourserver.com` with your actual FTP credentials.

---

### MQTT

> 📖 Full documentation: https://curl.se/docs/mqtt.html

```bash
# Subscribe to a topic
curl mqtt://mqtt.eclipseprojects.io/your-topic

# Force output to terminal (if warnings appear)
curl mqtt://mqtt.eclipseprojects.io/your-topic --output -

# Save received data to a file
curl mqtt://mqtt.eclipseprojects.io/your-topic --output data.txt

# Publish data to a topic
curl -d "your-data" mqtt://mqtt.eclipseprojects.io/your-topic
```

---

### Other Useful cURL Options

```bash
# Add custom authorization header
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/data

# Post to an IoT feed (e.g., Adafruit IO)
curl -H "X-AIO-Key: YOUR_AIO_KEY" \
  -F "value=on" \
  https://io.adafruit.com/api/v2/YOUR_USERNAME/feeds/YOUR_FEED/data
```

---

## NMAP

### Installation (Windows)

1. Download from the official page: https://nmap.org/download.html#windows
2. Run the `.exe` installer
3. Ensure **"Add Nmap to PATH"** is checked during installation

---

### Common Commands

```bash
# Ping / basic scan
nmap google.com
nmap 192.168.1.1

# Scan specific ports
nmap -p 22,80,443 192.168.1.1

# Scan all 65535 ports
nmap -p 1-65535 192.168.1.1

# OS detection
nmap -O 192.168.1.1
```

---

## Test-NetConnection (PowerShell)

> ✅ Built-in PowerShell utility — no installation required.

```powershell
# Basic ping test
Test-NetConnection google.com

# Test a specific port
Test-NetConnection google.com -Port 443

# Trace route
Test-NetConnection google.com -TraceRoute

# Check if RDP (Remote Desktop) is available
Test-NetConnection -ComputerName 192.168.1.10 -Port 3389

# Check if SMB (file sharing) is available
Test-NetConnection -ComputerName 192.168.1.20 -Port 445
```

---

## TraceRoute

```bash
# Trace the route to a host (Windows)
tracert google.com
```

---

## OpenSSL

```bash
# Test SSL/TLS connection
openssl s_client -connect example.com:443

# Show all certificates in the chain (SMTP with STARTTLS)
openssl s_client -showcerts -connect smtp.gmail.com:587 <NUL -starttls smtp
```

> 📌 **Certificate chain explained:**
> 1. **Leaf cert** — Proves the server's identity
> 2. **Intermediate cert** — Trusted middleman linking the server cert to a root
> 3. **Root cert** — Ultimate trust anchor; already trusted by your OS/browser

```bash
# Download and save the leaf (server) certificate as PEM
openssl s_client -showcerts -connect api.example.com:443 <NUL \
  | openssl x509 -outform PEM > server.pem
```

---

## SSH

```bash
# Connect to a remote machine
ssh username@hostname

# Connect to a Raspberry Pi (example)
ssh pi@192.168.0.100
# or
ssh pi@raspberrypi

# Execute a remote command and return output
ssh user@host "ls -l"
```

> ⚙️ **How remote commands work:** SSH logs in → executes the command → returns output → exits automatically.

---

## SCP

Secure Copy Protocol for transferring files over SSH.

```bash
# Copy a local file to a remote machine
scp file.txt user@host:/remote/path/

# Copy a file from a remote machine to local
scp user@host:/remote/path/file.txt .

# Copy an entire directory recursively
scp -r local-folder/ user@host:/remote/path/
```

---

## Testing Tools

### Online Webhook Tester

Use [webhook.site](https://webhook.site) to test and inspect incoming HTTP requests.

1. Visit https://webhook.site
2. Copy your unique webhook URL (e.g., `https://webhook.site/your-unique-id`)
3. Send GET, POST, or PUT requests to that URL and inspect them live

```bash
# Example: test a POST request
curl -X POST https://webhook.site/your-unique-id -d "test=hello"
```

---

## 📎 Quick Reference

| Tool | Purpose |
|------|---------|
| `curl` | HTTP/HTTPS/FTP/MQTT requests from the terminal |
| `nmap` | Network scanning and port discovery |
| `Test-NetConnection` | PowerShell ping, port test, and traceroute |
| `tracert` | Trace the network route to a host |
| `openssl` | Inspect and test SSL/TLS certificates |
| `ssh` | Secure remote shell access |
| `scp` | Secure file transfer over SSH |

---

> 💡 **Tip:** Always replace placeholder values like `USERNAME`, `PASSWORD`, `YOUR_TOKEN`, and `your-endpoint.com` with your actual credentials and endpoints before running commands.
