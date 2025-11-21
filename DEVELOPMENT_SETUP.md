# 🛠️ SIGIRI Development Setup

## 🚀 Quick Start for Local Development

Your login page now **automatically detects** whether you're in development or production mode!

---

## 📋 Local Development Steps

### 1. Start Backend Server (Terminal 1)

```bash
cd /Users/perera/Downloads/Sigiri/backend
node server.js
```

**You should see:**
```
🚀 Server is running on port 8080
📡 API available at http://localhost:8080
✅ Connected to MongoDB
```

### 2. Start Frontend Server (Terminal 2)

```bash
cd /Users/perera/Downloads/Sigiri/frontend
python3 -m http.server 3000
```

**Or use any other local server:**
```bash
# Using Node.js http-server
npx http-server -p 3000

# Using PHP
php -S localhost:3000

# Using VS Code Live Server extension
# Right-click on index.html → "Open with Live Server"
```

### 3. Open in Browser

```
http://localhost:3000/login.html
```

---

## 🔧 Environment Auto-Detection

The login page automatically detects your environment:

| Environment | API URL | Detection |
|------------|---------|-----------|
| **Local Development** | `http://localhost:8080/api/auth` | Running from `localhost`, `127.0.0.1`, or `file://` |
| **Production** | `https://backend-yanie.ondigitalocean.app/api/auth` | Running from `https://sigiri.io` |

**Check the browser console to see which mode you're in!**

---

## ✅ Test Credentials

### Local Backend (Development)
Create users with the test script:

```bash
cd /Users/perera/Downloads/Sigiri/backend
node createTestUser.js
```

**Default test user:**
- 📧 Email: `test@sigiri.com`
- 🔐 Password: `123`

### Production Backend
Use existing users:
- 📧 Email: `test@sigiri.com`
- 🔐 Password: `123456`

---

## 🔒 Email Verification Status

### Development (Local):
- ✅ **Email verification DISABLED**
- Users can login immediately after registration
- No need to verify email

### Production:
- ✅ **Email verification DISABLED** (temporarily for testing)
- Will be re-enabled before launch

---

## 📝 Development Workflow

### Making Changes to Backend:

1. Edit files in `backend/` folder
2. Restart the server:
   ```bash
   # Stop with Ctrl+C
   node server.js
   ```

### Making Changes to Frontend:

1. Edit files in `frontend/` folder
2. Refresh browser (no restart needed)
3. Changes appear immediately

### Testing API Endpoints:

```bash
# Register a user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@test.com","password":"test123","userName":"Dev User"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@test.com","password":"test123"}'
```

---

## 🗄️ Database Configuration

### Current Setup:
```
DigitalOcean MongoDB
└─ sigiri-db-51861e51.mongo.ondigitalocean.com
   └─ Database: sigiri
      └─ Collection: users
```

**Both local and production backend use the same database!**

This means:
- ✅ Users created locally appear in production
- ✅ No need to sync databases
- ✅ Consistent data everywhere

---

## 🔍 Debugging Tips

### Check Backend Logs:
```bash
# In the terminal running node server.js
# You'll see all API requests and database operations
```

### Check Frontend Console:
```javascript
// Open browser DevTools (F12)
// Console tab shows:
// - Environment mode (Local/Production)
// - API URL being used
// - Login/register responses
```

### Common Issues:

**1. "Connection error" in login:**
- ✅ Make sure backend is running on port 8080
- ✅ Check `node server.js` terminal for errors

**2. "Invalid email or password":**
- ✅ User might not exist in database
- ✅ Check password is correct
- ✅ Try registering a new user

**3. CORS errors:**
- ✅ Use `http://localhost:3000` (not `file://`)
- ✅ Backend already has CORS enabled

---

## 📦 Before Pushing to GitHub

### Update Backend:
```bash
cd /Users/perera/Downloads/Sigiri
git add backend/
git commit -m "Backend changes"
git push origin main
```

### Update Frontend:
```bash
git add frontend/
git commit -m "Frontend changes"
git push origin main
```

**DigitalOcean will auto-deploy backend changes!**

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Start backend | `cd backend && node server.js` |
| Start frontend | `cd frontend && python3 -m http.server 3000` |
| Create test user | `cd backend && node createTestUser.js` |
| View all users | `cd backend && node viewUsers.js` |
| Test API | `curl http://localhost:8080/` |
| Open in browser | `http://localhost:3000/login.html` |

---

## 🚀 Production vs Development

| Feature | Development | Production |
|---------|-------------|------------|
| Frontend URL | `http://localhost:3000` | `https://sigiri.io` |
| Backend URL | `http://localhost:8080` | `https://backend-yanie.ondigitalocean.app` |
| Database | DigitalOcean MongoDB | Same database |
| Email Verification | Disabled | Disabled (temp) |
| Auto-deploy | Manual restart | Auto on git push |

---

## 💡 Pro Tips

1. **Keep backend terminal open** - You'll see all API requests in real-time
2. **Use browser DevTools** - Check Network tab for API calls
3. **Check console logs** - Frontend logs show which API URL is being used
4. **Test in incognito** - Avoids localStorage conflicts
5. **Use Postman** - Test API endpoints without the frontend

---

## ✨ You're Ready!

Your development environment is configured and ready to go!

**Start both servers and open `http://localhost:3000/login.html` to begin development!** 🎉
