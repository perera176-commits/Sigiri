# 🚀 Deploy Backend to DigitalOcean App Platform

## ✅ Prerequisites Checklist:
- [x] MongoDB Database: DigitalOcean Managed MongoDB
- [x] GitHub Repository: perera176-commits/Sigiri
- [x] Backend Code: Ready in `/backend` folder

## 📋 Deployment Steps:

### Step 1: Push Latest Code to GitHub

```bash
cd /Users/perera/Downloads/Sigiri
git add -A
git commit -m "Prepare backend for DigitalOcean deployment"
git push origin main
```

### Step 2: Create App on DigitalOcean

1. **Go to DigitalOcean Dashboard**
   - Visit: https://cloud.digitalocean.com/apps
   - Click **"Create App"**

2. **Connect GitHub Repository**
   - Choose: **GitHub**
   - Select Repository: `perera176-commits/Sigiri`
   - Branch: `main`
   - Click **"Next"**

3. **Configure Resources**
   - **Source Directory:** `/backend`
   - **Run Command:** `node server.js`
   - **HTTP Port:** `8080`
   - Click **"Next"**

4. **Set Environment Variables**
   Click **"Edit"** and add these variables:

   | Key | Value | Type |
   |-----|-------|------|
   | `PORT` | `8080` | Plain Text |
   | `MONGO_URI` | `mongodb+srv://doadmin:8R0H2u1j39k4X5nr@sigiri-db-51861e51.mongo.ondigitalocean.com/sigiri?tls=true&authSource=admin` | **SECRET** |
   | `JWT_SECRET` | `sigiri-super-secret-jwt-key-change-in-production-2025` | **SECRET** |
   | `FRONTEND_URL` | `https://sigiri.io` | Plain Text |
   | `NODE_ENV` | `production` | Plain Text |

5. **Choose Plan**
   - Select: **Basic** ($5/month) or **Trial** (if available)
   - Click **"Next"**

6. **Name Your App**
   - App Name: `sigiri-backend`
   - Click **"Create Resources"**

### Step 3: Wait for Deployment
- Deployment takes ~5-10 minutes
- You'll see build logs in real-time
- Status will change to **"Deployed"** when ready

### Step 4: Get Your Backend URL
After deployment, you'll get a URL like:
```
https://sigiri-backend-xxxxx.ondigitalocean.app
```

Copy this URL - you'll need it!

### Step 5: Update Frontend

Update `frontend/login.html` with your new backend URL:

```javascript
// Change line 316 from:
const API_URL = 'https://sigiri-slgI6.ondigitalocean.app/api/auth';

// To your actual URL:
const API_URL = 'https://sigiri-backend-xxxxx.ondigitalocean.app/api/auth';
```

### Step 6: Test Your Backend

1. **Test Health Endpoint:**
   ```bash
   curl https://your-backend-url.ondigitalocean.app/
   ```
   
   Should return:
   ```json
   {
     "message": "SIGIRI Backend API",
     "status": "running"
   }
   ```

2. **Test Registration:**
   ```bash
   curl -X POST https://your-backend-url.ondigitalocean.app/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"123456"}'
   ```

3. **Test on Website:**
   - Go to https://sigiri.io/login.html
   - Try to register/login
   - Should work now! ✅

---

## 🔧 Alternative: Quick Deploy via CLI

If you have `doctl` installed:

```bash
cd /Users/perera/Downloads/Sigiri
doctl apps create --spec .do/app.yaml
```

---

## ❓ Common Issues

### Issue 1: Build Fails
**Solution:** Make sure `package.json` is in the `/backend` folder

### Issue 2: Can't Connect to MongoDB
**Solution:** Check that `MONGO_URI` environment variable is set correctly

### Issue 3: "Module not found" errors
**Solution:** Make sure `package.json` lists all dependencies

---

## 📊 Cost Estimate

| Service | Cost | Notes |
|---------|------|-------|
| MongoDB Database | Free (512MB) or $15/month | Already have this |
| App Platform (Basic) | $5/month | For backend API |
| **Total** | **$5/month** | (assuming free MongoDB) |

---

## ✅ After Deployment Checklist:

- [ ] Backend deployed to DigitalOcean App Platform
- [ ] Environment variables configured
- [ ] MongoDB connection working
- [ ] Backend URL obtained
- [ ] Frontend updated with backend URL
- [ ] Tested registration on live site
- [ ] Tested login on live site

---

## 🎯 Your Backend URL Format:

After deployment, your backend will be available at:
```
https://sigiri-backend-[random].ondigitalocean.app
```

Update this in:
- `frontend/login.html` (line 316)
- `frontend/verify-email.html` (if exists)

---

Need help with any step? Just ask! 😊
