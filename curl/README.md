# 📡 Networking & cURL Cheatsheet

A practical reference for cURL, MQTT, FTP, Nmap, PowerShell networking, and OpenSSL.

---

## 🔹 cURL Basics

### GET Request
curl https://www.google.com/

---

## 🔹 POST Requests

### Form Data
curl -X POST https://webhook.site/YOUR_UNIQUE_ID -d "data1=value1&data2=value2"

### JSON
curl -X POST -H "Content-Type: application/json" https://webhook.site/YOUR_UNIQUE_ID -d '{"key1":"value1"}'

### File Upload
curl -X POST https://webhook.site/YOUR_UNIQUE_ID -F "file=@image.jpg"

---

## 🔧 Headers
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/data

---

## 📁 File Handling
curl -o file.html https://example.com
curl -O https://example.com/file.zip

---

## 📡 MQTT
curl mqtt://broker.hivemq.com/topic
curl -d "msg" mqtt://broker.hivemq.com/topic

---

## 📂 FTP Upload
curl -T file.jpg ftp://USERNAME:PASSWORD@ftp.example.com/path/

---

## 🔎 Nmap
nmap example.com
nmap -p 22,80 192.168.1.1

---

## ⚡ PowerShell
Test-NetConnection example.com
Test-NetConnection example.com -Port 443

---

## 🔐 OpenSSL
openssl s_client -connect example.com:443
