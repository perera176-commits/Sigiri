# 🧪 Quick Test Guide - JPG → PDF Converter

## ✅ Backend is Running!

Your backend server is now live at:
```
http://localhost:8080
```

The conversion API is ready with these endpoints:
- POST `/api/convert/upload` - Upload images
- POST `/api/convert/process/:id` - Convert to PDF  
- GET `/api/convert/status/:id` - Check progress
- GET `/api/convert/download/:id` - Download PDF

---

## 🚀 How to Test RIGHT NOW

### **Option 1: Test with Browser (Recommended)**

**Step 1:** Open a new terminal and start the frontend server:
```bash
cd /Users/perera/Downloads/Sigiri/frontend
python3 -m http.server 3000
```

**Step 2:** Open your browser:
```
http://localhost:3000/jpg-to-pdf.html
```

**Step 3:** Test the converter:
1. ✅ Click the upload area (or drag JPG files)
2. ✅ Select 1-5 JPG images from your computer
3. ✅ Click "Convert to PDF" button
4. ✅ Watch the progress (Uploading → Converting → Downloading)
5. ✅ PDF downloads automatically!

---

### **Option 2: Test with cURL (API Testing)**

**Test 1: Upload a file**
```bash
curl -X POST http://localhost:8080/api/convert/upload \
  -F "files=@/path/to/your/photo.jpg"
```

You'll get response like:
```json
{
  "success": true,
  "uploadId": "abc123-uuid",
  "files": [...]
}
```

**Test 2: Start conversion**
```bash
curl -X POST http://localhost:8080/api/convert/process/abc123-uuid \
  -H "Content-Type: application/json" \
  -d '{"format":"pdf","quality":90,"pageSize":"A4"}'
```

**Test 3: Check status**
```bash
curl http://localhost:8080/api/convert/status/abc123-uuid
```

**Test 4: Download PDF**
```bash
curl -O http://localhost:8080/api/convert/download/abc123-uuid
```

---

## 📋 What to Look For

### **✅ Success Indicators:**

1. **Upload works:**
   - Files upload without errors
   - Progress bar shows "Uploading... 100%"
   - File count appears in UI

2. **Conversion works:**
   - Progress changes to "Converting..."
   - No error messages
   - Status changes to "complete"

3. **Download works:**
   - PDF file downloads automatically
   - File opens in PDF viewer
   - Images appear in correct order
   - Quality looks good

4. **Error handling works:**
   - Upload file >10MB → Shows error
   - Upload >5 files → Shows error
   - Upload non-image → Shows error

---

## 🐛 Common Issues & Solutions

### **Issue: Frontend can't connect to backend**

**Check:** Is backend running?
```bash
# You should see:
🚀 Server is running on port 8080
📡 API available at http://localhost:8080
```

**Fix:** Make sure backend is started:
```bash
cd /Users/perera/Downloads/Sigiri/backend
node server.js
```

---

### **Issue: "Cannot find module 'sharp'"**

**Fix:** Install dependencies:
```bash
cd /Users/perera/Downloads/Sigiri/backend
npm install
```

---

### **Issue: "ENOENT: no such file or directory, mkdir 'uploads'"**

**Fix:** Server creates folders automatically, but you can manually create:
```bash
cd /Users/perera/Downloads/Sigiri/backend
mkdir uploads processed
chmod 755 uploads processed
```

---

### **Issue: Upload works but conversion fails**

**Check backend logs:**
```bash
# Look for error messages in the terminal running server.js
```

**Common causes:**
- Corrupt image file
- Unsupported image format
- Insufficient permissions
- Out of disk space

---

## 🎯 Test Scenarios

### **Scenario 1: Single Image**
- Upload: 1 JPG file (~1MB)
- Expected: PDF with 1 page
- Time: ~2 seconds

### **Scenario 2: Batch (5 Images)**
- Upload: 5 JPG files
- Expected: PDF with 5 pages
- Time: ~3-4 seconds

### **Scenario 3: Large Image**
- Upload: 1 large JPG (5-10MB)
- Expected: PDF with optimized/scaled image
- Time: ~3-5 seconds

### **Scenario 4: Error - File Too Large**
- Upload: 1 image >10MB
- Expected: Error message
- UI: Shows "File too large" notification

### **Scenario 5: Error - Wrong Format**
- Upload: 1 TXT or PDF file
- Expected: Error message
- UI: Shows "Only image files allowed"

---

## 📊 Performance Benchmarks

Test and record your results:

| Test | File Count | Total Size | Time | Status |
|------|-----------|------------|------|--------|
| Single small | 1 | 500KB | ___s | ⬜ |
| Single medium | 1 | 2MB | ___s | ⬜ |
| Single large | 1 | 8MB | ___s | ⬜ |
| Batch small | 5 | 2MB | ___s | ⬜ |
| Batch large | 5 | 20MB | ___s | ⬜ |

---

## 🎉 Success Checklist

Mark these off as you test:

**Backend:**
- [ ] Server starts without errors
- [ ] Can access http://localhost:8080
- [ ] Upload endpoint responds
- [ ] Process endpoint responds
- [ ] Status endpoint responds
- [ ] Download endpoint responds

**Frontend:**
- [ ] Page loads at http://localhost:3000/jpg-to-pdf.html
- [ ] Upload area is clickable
- [ ] Drag & drop works
- [ ] File selection works
- [ ] Convert button enables after file selection
- [ ] Progress bar appears
- [ ] PDF downloads automatically
- [ ] Success notification shows

**Quality:**
- [ ] PDF contains all uploaded images
- [ ] Images are clear (not blurry)
- [ ] Images fit properly on pages
- [ ] Page order matches upload order
- [ ] PDF opens in viewer

**Error Handling:**
- [ ] Large file shows error
- [ ] Wrong format shows error
- [ ] Too many files shows error
- [ ] Network error shows error

---

## 🚀 Next Steps After Testing

### **If Everything Works:**
1. ✅ Celebrate! Your first converter is live! 🎉
2. ✅ Deploy to production (git push)
3. ✅ Create more converters (PNG→PDF, HEIC→JPG, etc.)
4. ✅ Add advanced features (quality selector, page size)

### **If Issues Found:**
1. ✅ Note the error message
2. ✅ Check backend terminal logs
3. ✅ Check browser console (F12)
4. ✅ Refer to troubleshooting section above
5. ✅ Ask for help with specific error

---

## 📸 What a Successful Test Looks Like

**Browser UI:**
```
┌─────────────────────────────────────┐
│  JPG to PDF Converter - SIGIRI      │
├─────────────────────────────────────┤
│  [Drag & Drop Area]                 │
│  📁 2 files selected (3.2 MB)       │
│                                     │
│  [Converting... 75% ●●●●●○○○]      │
│                                     │
│  ✅ Conversion successful!          │
│     File downloaded.                │
└─────────────────────────────────────┘
```

**Backend Terminal:**
```bash
🚀 Server is running on port 8080
📡 API available at http://localhost:8080
✅ Connected to MongoDB
POST /api/convert/upload - 200 OK
POST /api/convert/process/abc123 - 200 OK
GET /api/convert/status/abc123 - 200 OK
GET /api/convert/download/abc123 - 200 OK
```

**Downloaded PDF:**
- Filename: `converted.pdf`
- Size: ~500KB - 2MB (depends on images)
- Pages: Matches number of uploaded images
- Quality: Clear and readable

---

## 🎓 Understanding the Flow

```
1. USER SELECTS FILES
   ↓
2. FRONTEND VALIDATES
   - Check file types
   - Check file sizes
   - Check file count
   ↓
3. UPLOAD TO BACKEND
   - FormData with files
   - POST /api/convert/upload
   - Backend saves to /uploads
   ↓
4. START CONVERSION
   - POST /api/convert/process
   - Backend uses Sharp + PDF-lib
   - Processes each image
   - Creates PDF
   - Saves to /processed
   ↓
5. POLL STATUS
   - GET /api/convert/status
   - Checks every 1 second
   - Waits for "complete"
   ↓
6. DOWNLOAD PDF
   - GET /api/convert/download
   - Browser downloads file
   - Backend cleans up files
   ↓
7. SUCCESS!
```

---

## 🔧 Monitoring & Debugging

**Watch Backend Logs:**
```bash
# Terminal with backend running shows:
- Upload requests
- Conversion progress
- Download requests
- Any errors
```

**Watch Browser Console:**
```bash
# Press F12 in browser, Console tab shows:
- API calls
- Progress updates
- Success/error messages
```

**Check Files:**
```bash
# Backend creates these folders:
ls -la /Users/perera/Downloads/Sigiri/backend/uploads
ls -la /Users/perera/Downloads/Sigiri/backend/processed

# Should show uploaded images and converted PDFs
```

---

## 💡 Tips for Best Results

1. **Use good quality JPG images** (not tiny thumbnails)
2. **Test with different image sizes** (small, medium, large)
3. **Test batch conversion** (multiple files at once)
4. **Test error cases** (wrong format, too large)
5. **Check PDF quality** (open and zoom in)
6. **Verify all pages** (scroll through entire PDF)
7. **Test download** (make sure file saves correctly)

---

## 🎯 Ready to Test?

**Start testing now:**

```bash
# Terminal 1 (already running):
# Backend at http://localhost:8080 ✅

# Terminal 2 (start now):
cd /Users/perera/Downloads/Sigiri/frontend
python3 -m http.server 3000

# Browser:
http://localhost:3000/jpg-to-pdf.html
```

**Upload a JPG and watch the magic happen!** ✨

---

*Good luck testing! Let me know if you encounter any issues.* 🚀
