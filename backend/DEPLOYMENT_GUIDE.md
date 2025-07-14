# 📁 File Upload Deployment Guide

## 🚨 **Critical Issue: File Storage in Production**

### **Current Problem**
- Files are stored locally in `/media/` folder
- **Render/Vercel**: Files are LOST on restart (ephemeral storage)
- **No persistent file storage** configured

### **Impact**
- ❌ Registration documents disappear
- ❌ Audio files lost
- ❌ Department certificates missing
- ❌ User uploads not accessible

## ✅ **Solutions**

### **Option 1: AWS S3 (Recommended)**

**1. Create AWS S3 Bucket:**
```bash
# Create bucket in AWS Console or CLI
aws s3 mb s3://myguardian-uploads
```

**2. Set Environment Variables in Render:**
```bash
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=myguardian-uploads
AWS_S3_REGION_NAME=us-east-1
DEBUG=False
```

**3. Deploy to Render:**
```bash
git add .
git commit -m "Add AWS S3 storage for production"
git push origin main
```

### **Option 2: Firebase Storage (Already Available)**

**1. Set Environment Variables in Render:**
```bash
STORAGE_BACKEND=firebase
FIREBASE_STORAGE_BUCKET=guardian-16d00.firebasestorage.app
FIREBASE_PROJECT_ID=guardian-16d00
DEBUG=False
```

**2. Add Firebase Service Account:**
- Download service account JSON from Firebase Console
- Add as environment variable: `GOOGLE_APPLICATION_CREDENTIALS`

### **Option 3: Google Cloud Storage**

**1. Set Environment Variables:**
```bash
STORAGE_BACKEND=gcs
GS_BUCKET_NAME=myguardian-uploads
GS_PROJECT_ID=your-project-id
DEBUG=False
```

## 🔧 **Implementation Status**

### **✅ Already Implemented**
- Cloud storage configuration in `settings.py`
- Support for AWS S3, Firebase, Google Cloud
- Automatic fallback to local storage in development
- File upload endpoints with proper parsing

### **📋 Required Dependencies**
```bash
django-storages==1.14.2
boto3==1.34.0  # For AWS S3
google-cloud-storage  # For GCS/Firebase
```

### **🔍 File Upload Endpoints**
- **Registration**: `POST /api/auth/registration-request/`
- **Department Registration**: `POST /api/devices/departments/register/`
- **Device Audio**: `POST /api/devices/data/`

## 🚀 **Quick Setup for Render**

### **Step 1: Choose Storage Backend**
Recommend **Firebase** since you already have it configured:

### **Step 2: Add Environment Variables in Render Dashboard**
```
STORAGE_BACKEND=firebase
FIREBASE_STORAGE_BUCKET=guardian-16d00.firebasestorage.app
FIREBASE_PROJECT_ID=guardian-16d00
DEBUG=False
```

### **Step 3: Deploy**
```bash
git add .
git commit -m "Configure Firebase storage for production"
git push origin main
```

### **Step 4: Test File Uploads**
1. Try registration with document upload
2. Check Firebase Storage Console
3. Verify files are accessible via URLs

## 📊 **Storage Comparison**

| Storage | Cost | Setup | Reliability | Integration |
|---------|------|-------|-------------|-------------|
| **AWS S3** | Low | Medium | Excellent | Easy |
| **Firebase** | Low | Easy | Excellent | Already setup |
| **Google Cloud** | Low | Medium | Excellent | Medium |
| **Local** | Free | None | ❌ Lost on restart | N/A |

## 🔐 **Security Notes**

### **File Access Control**
- Set appropriate bucket permissions
- Use signed URLs for private files
- Implement file type validation
- Limit file sizes (currently 10MB)

### **Environment Variables**
- Never commit credentials to git
- Use Render's environment variable system
- Rotate keys regularly

## 🧪 **Testing**

### **Local Development**
```bash
# Test with local storage
DEBUG=True python manage.py runserver
```

### **Production Testing**
```bash
# Test cloud storage configuration
python cloud_storage_config.py
```

## 📱 **Frontend Considerations**

### **File Upload URLs**
- Development: `http://localhost:8000/media/file.pdf`
- Production: `https://bucket-name.s3.amazonaws.com/file.pdf`

### **CORS Configuration**
Ensure your storage bucket allows CORS from your frontend domain.

## 🆘 **Troubleshooting**

### **Files Not Uploading**
1. Check environment variables
2. Verify bucket permissions
3. Check CORS settings
4. Review Django logs

### **Files Not Accessible**
1. Check bucket public access
2. Verify MEDIA_URL configuration
3. Test direct bucket URLs

### **Performance Issues**
1. Use CDN (CloudFront for S3)
2. Optimize file sizes
3. Implement lazy loading

## 📞 **Support**

If you encounter issues:
1. Check Render deployment logs
2. Test storage configuration script
3. Verify environment variables
4. Check bucket permissions
