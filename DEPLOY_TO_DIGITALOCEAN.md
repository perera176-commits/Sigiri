# 🚀 Deploy SIGIRI Backend to DigitalOcean Droplet

## 📋 What We're Deploying:

Your Node.js backend with:
- ✅ Authentication API (JWT)
- ✅ MongoDB Atlas connection
- ✅ Email verification system
- ✅ User management

---

## Step 1: Create a DigitalOcean Droplet

### 1.1 Go to DigitalOcean
- Navigate to: https://cloud.digitalocean.com/droplets
- Click **"Create"** → **"Droplets"**

### 1.2 Choose Configuration
**Image:** Ubuntu 24.04 (LTS) x64

**Plan:**
- **Basic** plan
- **Regular CPU**
- **$6/month** (1 GB RAM, 1 vCPU, 25 GB SSD, 1 TB transfer)
- (Can upgrade later if needed)

**Datacenter Region:**
- Choose closest to your users
- Recommended: **New York** or **San Francisco**

**Authentication:**
- Choose **"SSH keys"** (more secure)
- Or use **"Password"** (simpler but less secure)

**Hostname:**
- Name it: `sigiri-backend` or `sigiri-api`

**Click "Create Droplet"**

Wait 1-2 minutes for it to provision.

---

## Step 2: Connect to Your Droplet

### 2.1 Get IP Address
After creation, you'll see an IP address like: `142.93.123.45`

### 2.2 SSH into Droplet
Open your terminal:

```bash
ssh root@YOUR_DROPLET_IP
# Example: ssh root@142.93.123.45
```

If prompted, type `yes` to continue connecting.

---

## Step 3: Set Up Server Environment

Once connected to your droplet, run these commands:

### 3.1 Update System
```bash
apt update && apt upgrade -y
```

### 3.2 Install Node.js (v20 LTS)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
apt install -y nodejs
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x
```

### 3.3 Install PM2 (Process Manager)
```bash
npm install -g pm2
pm2 --version
```

### 3.4 Install Git
```bash
apt install -y git
git --version
```

### 3.5 Install Nginx (Web Server)
```bash
apt install -y nginx
nginx -v
```

---

## Step 4: Deploy Your Backend Code

### 4.1 Clone Your Repository
```bash
cd /var/www
git clone https://github.com/perera176-commits/Sigiri.git
cd Sigiri/backend
```

### 4.2 Install Dependencies
```bash
npm install
```

### 4.3 Create .env File
```bash
nano .env
```

Paste this (replace with your actual values):
```env
# Server Configuration
PORT=8080

# MongoDB Atlas Connection
MONGO_URI=mongodb+srv://master-converter-user:RtZtvSpXgp61cUhW@master-converter-cluste.h0rh5nr.mongodb.net/sigiri?retryWrites=true&w=majority&appName=master-converter-cluster

# JWT Secret
JWT_SECRET=sigiri-super-secret-jwt-key-change-in-production-2025

# Frontend URL (your live website)
FRONTEND_URL=https://sigiri.io

# Email Configuration (Optional)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASS=your-app-password
# EMAIL_FROM=SIGIRI <noreply@sigiri.com>
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### 4.4 Test Backend
```bash
node server.js
```

You should see:
```
🚀 Server is running on port 8080
📡 API available at http://localhost:8080
✅ Connected to MongoDB
```

Press `Ctrl+C` to stop.

---

## Step 5: Configure PM2 (Keep Backend Running)

### 5.1 Start with PM2
```bash
pm2 start server.js --name "sigiri-backend"
pm2 save
pm2 startup
```

Copy and run the command that PM2 gives you (looks like `sudo env PATH=...`)

### 5.2 Check Status
```bash
pm2 status
pm2 logs sigiri-backend  # View logs
```

---

## Step 6: Configure Nginx (Reverse Proxy)

### 6.1 Create Nginx Configuration
```bash
nano /etc/nginx/sites-available/sigiri-api
```

Paste this:
```nginx
server {
    listen 80;
    server_name api.sigiri.io;  # Or use your droplet IP

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Save:** `Ctrl+X`, `Y`, `Enter`

### 6.2 Enable Configuration
```bash
ln -s /etc/nginx/sites-available/sigiri-api /etc/nginx/sites-enabled/
nginx -t  # Test configuration
systemctl reload nginx
```

### 6.3 Configure Firewall
```bash
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw enable
ufw status
```

---

## Step 7: Set Up Domain (Optional but Recommended)

### Option A: Using Subdomain (api.sigiri.io)

1. Go to your domain registrar (where you bought sigiri.io)
2. Add DNS record:
   - **Type:** A Record
   - **Host:** api
   - **Value:** Your droplet IP (e.g., 142.93.123.45)
   - **TTL:** Automatic or 3600

3. Wait 5-30 minutes for DNS propagation

### Option B: Using Droplet IP Directly
Skip domain setup and use: `http://YOUR_DROPLET_IP:8080`

---

## Step 8: Set Up SSL (HTTPS) - Recommended

### 8.1 Install Certbot
```bash
apt install -y certbot python3-certbot-nginx
```

### 8.2 Get SSL Certificate
```bash
certbot --nginx -d api.sigiri.io
```

Follow the prompts:
- Enter your email
- Agree to terms
- Choose to redirect HTTP to HTTPS

### 8.3 Test Auto-Renewal
```bash
certbot renew --dry-run
```

---

## Step 9: Update Frontend

### 9.1 Update API URL in frontend/login.html

Change from:
```javascript
const API_URL = 'http://localhost:8080/api/auth';
```

To:
```javascript
const API_URL = 'https://api.sigiri.io/api/auth';
// Or: const API_URL = 'http://YOUR_DROPLET_IP/api/auth';
```

### 9.2 Update CORS in backend/server.js

Add your frontend domain to CORS:
```javascript
app.use(cors({
  origin: ['https://sigiri.io', 'http://localhost:3000'],
  credentials: true
}));
```

### 9.3 Commit and Push
```bash
git add frontend/login.html backend/server.js
git commit -m "Update API URL for production"
git push origin main
```

Then redeploy frontend to GitHub Pages.

---

## Step 10: Update MongoDB Atlas IP Whitelist

### 10.1 Get Droplet Public IP
```bash
curl ifconfig.me
```

### 10.2 Add to MongoDB Atlas
1. Go to MongoDB Atlas → Database → Network Access
2. Click "Add IP Address"
3. Add your droplet's IP address
4. Or use `0.0.0.0/0` (allow from anywhere - less secure but easier)

---

## 🧪 Testing

### Test Backend Directly
```bash
# On your droplet
curl http://localhost:8080
```

### Test from Outside
```bash
# On your local machine
curl http://YOUR_DROPLET_IP
# Or: curl https://api.sigiri.io
```

### Test Authentication
1. Go to https://sigiri.io/login.html
2. Register a new account
3. Verify email
4. Login successfully

---

## 📊 Useful Commands

### PM2 Management
```bash
pm2 status                    # Check status
pm2 logs sigiri-backend       # View logs
pm2 restart sigiri-backend    # Restart
pm2 stop sigiri-backend       # Stop
pm2 delete sigiri-backend     # Remove
```

### Update Code
```bash
cd /var/www/Sigiri/backend
git pull origin main
npm install
pm2 restart sigiri-backend
```

### Check Nginx
```bash
systemctl status nginx
nginx -t
systemctl reload nginx
```

### View Logs
```bash
pm2 logs sigiri-backend --lines 100
tail -f /var/log/nginx/error.log
```

---

## 🔒 Security Best Practices

1. ✅ Use SSH keys (not password)
2. ✅ Enable UFW firewall
3. ✅ Use HTTPS (SSL certificate)
4. ✅ Don't commit .env to git
5. ✅ Use strong JWT secret
6. ✅ Update packages regularly: `npm update`
7. ✅ Monitor PM2 logs regularly
8. ✅ Set up MongoDB Atlas IP whitelist

---

## 💰 Cost Breakdown

- **DigitalOcean Droplet:** $6/month (Basic)
- **MongoDB Atlas:** Free (M0 tier)
- **Domain:** Already owned (sigiri.io)
- **SSL Certificate:** Free (Let's Encrypt)

**Total: $6/month**

---

## 🎯 Next Steps After Deployment

1. ✅ Test registration and login on live site
2. ✅ Monitor server logs: `pm2 logs sigiri-backend`
3. ✅ Set up MongoDB backups in Atlas
4. ✅ Configure email service (Gmail/SendGrid)
5. ✅ Add password reset functionality
6. ✅ Set up monitoring (Uptime Robot, etc.)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
pm2 logs sigiri-backend
# Check for errors
```

### Can't connect to MongoDB
- Check MongoDB Atlas IP whitelist
- Verify connection string in .env
- Test: `curl https://api.sigiri.io`

### Nginx errors
```bash
nginx -t
tail -f /var/log/nginx/error.log
```

### Frontend can't reach backend
- Check CORS configuration
- Verify API URL in login.html
- Test: `curl https://api.sigiri.io/api/auth`

---

## 📞 Need Help?

1. Check PM2 logs: `pm2 logs sigiri-backend`
2. Check Nginx logs: `tail -f /var/log/nginx/error.log`
3. Test connectivity: `curl https://api.sigiri.io`

---

**Ready to deploy! Let's go through these steps together!** 🚀
