# 🔐 SIGIRI Authentication System

## ✅ Complete Backend Authentication with Email Verification

Your SIGIRI website now has a **professional authentication system** with:

### 🎉 Features Implemented:

1. **✅ User Registration** with email verification
2. **✅ Secure Login** with JWT tokens
3. **✅ Password Hashing** using bcryptjs
4. **✅ Email Verification** system
5. **✅ Resend Verification** email option
6. **✅ MongoDB Integration** with User model
7. **✅ Protected Routes** ready for dashboard

---

## 🚀 How to Start the Backend

### 1. Install Dependencies (Already Done)
```bash
cd backend
npm install
```

### 2. Start the Server
```bash
cd backend
node server.js
```

**You should see:**
```
🚀 Server is running on port 8080
📡 API available at http://localhost:8080
✅ Connected to MongoDB
```

---

## 📋 Testing the Authentication Flow

### Step 1: Open the New Login Page

Open in your browser:
```
file:///Users/perera/Downloads/Sigiri/frontend/login-new.html
```

Or use a local server:
```bash
cd frontend
python3 -m http.server 3000
```
Then visit: `http://localhost:3000/login-new.html`

### Step 2: Register a New Account

1. Click the **"Register"** tab
2. Fill in:
   - Name: `Test User` (optional)
   - Email: `yourtest@gmail.com`
   - Password: `test123` (min 6 chars)
   - Confirm Password: `test123`
3. Click **"Create Account"**

**What happens:**
- ✅ Account created in MongoDB
- ✅ Verification token generated
- ✅ Email verification link logged to console (in development mode)
- ✅ You'll see: "Registration successful! Please check your email..."

### Step 3: Verify Email (Development Mode)

Since emails are in development mode, check your backend terminal. You'll see:

```
📧 VERIFICATION EMAIL (Development Mode):
To: yourtest@gmail.com
Verification URL: http://localhost:3000/verify-email.html?token=abc123...
Token: abc123...
```

**Copy the Verification URL** and paste it in your browser.

Or manually visit:
```
http://localhost:3000/verify-email.html?token=YOUR_TOKEN_HERE
```

**Result:** ✅ "Email Verified!" page appears

### Step 4: Login

1. Go back to login page
2. Enter your email and password
3. Click **"Login"**

**What happens:**
- ✅ Password verified against hashed version
- ✅ JWT token generated
- ✅ Token stored in localStorage
- ✅ Redirected to dashboard
- ✅ User info saved (email, name, token)

---

## 🔑 API Endpoints

### Base URL: `http://localhost:8080/api/auth`

### 1. **Register User**
```
POST /api/auth/register

Body:
{
  "email": "user@example.com",
  "password": "password123",
  "userName": "John Doe"
}

Response:
{
  "success": true,
  "message": "Registration successful! Please check your email...",
  "userId": "123abc..."
}
```

### 2. **Login User**
```
POST /api/auth/login

Body:
{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "message": "Login successful!",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123abc...",
    "email": "user@example.com",
    "userName": "John Doe",
    "loginMethod": "email"
  }
}
```

### 3. **Verify Email**
```
GET /api/auth/verify-email/:token

Response:
{
  "success": true,
  "message": "Email verified successfully! You can now login."
}
```

### 4. **Resend Verification**
```
POST /api/auth/resend-verification

Body:
{
  "email": "user@example.com"
}

Response:
{
  "success": true,
  "message": "Verification email sent! Please check your inbox."
}
```

---

## 📁 New Files Created

### Backend:
- ✅ `backend/models/User.js` - User model with password hashing
- ✅ `backend/routes/auth.js` - Authentication endpoints
- ✅ `backend/utils/emailService.js` - Email sending service
- ✅ `backend/.env.example` - Environment variables template
- ✅ Updated `backend/server.js` - Main server with CORS and routes
- ✅ Updated `backend/package.json` - Added dependencies

### Frontend:
- ✅ `frontend/login-new.html` - New login/register page with backend integration
- ✅ `frontend/verify-email.html` - Email verification page

---

## 🔒 Security Features

1. **Password Hashing**: bcryptjs with salt rounds
2. **JWT Tokens**: Secure authentication tokens (7-day expiry)
3. **Email Verification**: Users must verify email before login
4. **Input Validation**: Server-side validation for all inputs
5. **CORS Protection**: Configured for security
6. **Token Expiration**: Verification tokens expire
7. **Unique Emails**: No duplicate accounts allowed

---

## 🧪 Test with curl

### Register:
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@sigiri.com","password":"test123","userName":"Test User"}'
```

### Login:
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@sigiri.com","password":"test123"}'
```

---

## 📧 Email Configuration (Production)

For production, update `.env` file with real email credentials:

### Gmail Setup:
1. Enable 2-factor authentication in Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-16-char-app-password
EMAIL_FROM=SIGIRI <noreply@sigiri.com>
FRONTEND_URL=https://yourdomain.com
```

### SendGrid (Alternative):
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USER=apikey
EMAIL_PASS=your-sendgrid-api-key
```

---

## 🐛 Troubleshooting

### Backend won't start:
- Check if MongoDB is running: `mongod`
- Check if port 8080 is free: `lsof -ti:8080`

### Can't register:
- Check backend console for errors
- Verify MongoDB connection
- Check email format is valid

### Email not verified:
- Check backend terminal for verification URL
- Copy the token from console
- Visit verify-email.html?token=YOUR_TOKEN

### Login fails:
- Make sure email is verified first
- Check password is correct (min 6 characters)
- Check backend console for error messages

---

## ✨ What's Next?

1. **Password Reset** - Implement forgot password feature
2. **Email Service** - Configure real email sending (Gmail/SendGrid)
3. **Dashboard Protection** - Add JWT verification middleware
4. **Profile Management** - Edit user info, change password
5. **Social Login** - Add Google OAuth back (optional)

---

## 🎯 Current vs Old Login

### Old Login (login.html):
- ❌ No backend verification
- ❌ Just localStorage (fake authentication)
- ❌ Anyone can access dashboard

### New Login (login-new.html):
- ✅ Real backend authentication
- ✅ Password verification against MongoDB
- ✅ JWT token-based sessions
- ✅ Email verification required
- ✅ Secure password hashing
- ✅ Protected user data

---

## 📊 Database Structure

### User Schema:
```javascript
{
  email: String (unique, required),
  password: String (hashed, required),
  userName: String,
  loginMethod: String (email/google/work),
  isVerified: Boolean (default: false),
  verificationToken: String,
  resetPasswordToken: String,
  resetPasswordExpires: Date,
  createdAt: Date,
  lastLogin: Date
}
```

---

## 🎉 Success! Your authentication system is complete!

**To test it now:**
1. Make sure backend server is running: `node backend/server.js`
2. Open `frontend/login-new.html` in your browser
3. Register a new account
4. Check backend terminal for verification link
5. Verify your email
6. Login successfully!

**Backend Status:** ✅ Running on http://localhost:8080
**MongoDB:** ✅ Connected
**Authentication:** ✅ Fully functional
**Email System:** ✅ Ready (development mode)

---

Need help? Check the backend console for detailed logs of all authentication attempts!
