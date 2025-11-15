# Google OAuth Setup Guide for SIGIRI

## 🎯 What You Need to Do

Your login page is now configured with **real Google OAuth 2.0** integration. When users click "Continue with Google", they will be redirected to the actual Google sign-in page (like in your screenshot).

---

## 📋 Step-by-Step Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click **"Select a Project"** at the top → **"New Project"**
4. Enter project name: **"SIGIRI"**
5. Click **"Create"**

---

### Step 2: Enable Google Sign-In API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google+ API"** or **"Google Identity"**
3. Click **"Enable"**

---

### Step 3: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** (for public users)
3. Click **"Create"**

**Fill in the required information:**
- **App name:** SIGIRI
- **User support email:** Your email
- **App logo:** Upload your logo (optional)
- **Application home page:** https://yourdomain.com
- **Authorized domains:** yourdomain.com
- **Developer contact email:** Your email

4. Click **"Save and Continue"**
5. **Scopes:** Click "Add or Remove Scopes"
   - Select: `email`, `profile`, `openid`
   - Click **"Update"** → **"Save and Continue"**
6. **Test users:** (Optional during development)
   - Add your email for testing
   - Click **"Save and Continue"**

---

### Step 4: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ Create Credentials"** → **"OAuth client ID"**
3. Select **"Web application"**

**Configure:**
- **Name:** SIGIRI Web Client
- **Authorized JavaScript origins:**
  ```
  http://localhost:3000
  http://127.0.0.1:3000
  https://yourdomain.com
  ```
- **Authorized redirect URIs:**
  ```
  http://localhost:3000/login.html
  http://127.0.0.1:3000/login.html
  https://yourdomain.com/login.html
  https://yourdomain.com/dashboard.html
  ```

4. Click **"Create"**
5. **COPY YOUR CLIENT ID** - It looks like:
   ```
   123456789-abcdefghijklmnop.apps.googleusercontent.com
   ```

---

### Step 5: Update Your Login Page

Open `frontend/login.html` and find this line (around line 300):

```html
data-client_id="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com"
```

**Replace it with your actual Client ID:**

```html
data-client_id="123456789-abcdefghijklmnop.apps.googleusercontent.com"
```

---

## 🧪 How to Test

### Local Testing:
1. Start a local server:
   ```bash
   cd /Users/perera/Downloads/Sigiri/frontend
   python3 -m http.server 3000
   ```

2. Open browser: `http://localhost:3000/login.html`

3. Click **"Continue with Google"**

4. You should see the real Google sign-in page (like in your screenshot)

5. Sign in with your Google account

6. You'll be redirected back to your dashboard

---

## ✅ What's Already Configured

Your `login.html` now includes:

1. ✅ **Google OAuth 2.0 Library** - Loaded from Google's CDN
2. ✅ **Official Google Sign-In Button** - Styled by Google
3. ✅ **Custom Fallback Button** - In case you want custom styling
4. ✅ **JWT Token Parser** - Extracts user info (name, email, picture)
5. ✅ **User Data Storage** - Saves to localStorage:
   - User email
   - User name
   - Profile picture
   - Google authentication token
6. ✅ **Auto-redirect** - Sends user to dashboard after login
7. ✅ **Error Handling** - Shows messages if something fails

---

## 🔐 Security Notes

### For Production:

1. **NEVER commit your Client ID to public repositories** if it contains secrets
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** - Google OAuth requires HTTPS in production
4. **Verify tokens on your backend** - Don't trust client-side tokens alone
5. **Implement token refresh** - Tokens expire, handle refresh logic

### Backend Verification (Recommended):

```javascript
// Example: Verify token on your backend (Node.js)
const { OAuth2Client } = require('google-auth-library');
const client = new OAuth2Client(CLIENT_ID);

async function verify(token) {
  const ticket = await client.verifyIdToken({
      idToken: token,
      audience: CLIENT_ID,
  });
  const payload = ticket.getPayload();
  const userid = payload['sub'];
  return payload;
}
```

---

## 🎨 What Users Will See

1. **On your site:** Modern login page with "Continue with Google" button
2. **After clicking:** Redirected to Google's official sign-in page (your screenshot)
3. **On Google's page:** 
   - See your app name "SIGIRI"
   - Enter email/password on Google's secure servers
   - Grant permissions (email, profile)
4. **After signing in:** Automatically returned to your dashboard

---

## 📱 Mobile Support

The Google OAuth integration works on:
- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Mobile browsers (iOS Safari, Android Chrome)
- ✅ WebView in mobile apps
- ✅ Progressive Web Apps (PWAs)

---

## 🐛 Troubleshooting

### Issue: "Error 400: redirect_uri_mismatch"
**Solution:** Add your exact URL to "Authorized redirect URIs" in Google Console

### Issue: "Access blocked: This app's request is invalid"
**Solution:** Complete the OAuth consent screen configuration

### Issue: "Popup was closed by user"
**Solution:** User closed the popup - normal behavior, no action needed

### Issue: "Client ID not found"
**Solution:** Replace `YOUR_GOOGLE_CLIENT_ID` with your actual Client ID

### Issue: "Cookies disabled"
**Solution:** Enable cookies in browser settings (required for OAuth)

---

## 📊 Current Features

Your login system now supports:

1. ✅ **Google OAuth** (Real authentication via Google)
2. ✅ **Email/Password** (Direct login on your site)
3. ✅ **Work Email** (Enterprise email support)
4. ✅ **Session Management** (localStorage)
5. ✅ **Auto-login Check** (Skip login if already logged in)
6. ✅ **Error Messages** (User-friendly feedback)
7. ✅ **Success Messages** (Confirmation feedback)
8. ✅ **Responsive Design** (Mobile-friendly)

---

## 🚀 Next Steps

1. ✅ Set up Google Cloud Console project
2. ✅ Get your OAuth Client ID
3. ✅ Update `login.html` with your Client ID
4. ✅ Test locally
5. ⏳ Deploy to production with HTTPS
6. ⏳ Implement backend token verification
7. ⏳ Add user profile management
8. ⏳ Implement logout functionality

---

## 💡 Pro Tips

1. **During Development:** Use `localhost` URLs in Google Console
2. **Test Accounts:** Add yourself as a test user during development
3. **Publishing:** Submit your app for verification once ready
4. **Branding:** Add your logo to the OAuth consent screen
5. **Monitoring:** Check Google Cloud Console for usage analytics

---

## 📞 Support

If you need help:
- Google OAuth Documentation: https://developers.google.com/identity/oauth2/web/guides/overview
- Google Cloud Console: https://console.cloud.google.com/

---

**Your login page is ready! Just add your Google Client ID and test it! 🎉**
