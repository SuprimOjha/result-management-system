# Deployment Guide for Render

This guide explains how to properly deploy the Result Management System to Render to fix the OTP verification errors.

## The Problem

**The internal server error on OTP verification is caused by SQLite database being used in production.** Render has an ephemeral file system that wipes data on every restart/redeploy. This causes:
- User data to vanish
- Session data to be lost
- OTP verification to fail with database errors

## Solution: Use PostgreSQL

Render provides free PostgreSQL databases. Follow these steps:

### Step 1: Update Environment Variables on Render

In your Render dashboard, go to **Environment** and add these variables:

```
DEBUG=False
DATABASE_URL=postgresql://username:password@host:5432/dbname
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Important:** For `EMAIL_HOST_PASSWORD`, you must use an **App Password**, not your Gmail password:
1. Go to https://myaccount.google.com/apppasswords
2. Select **Mail** as the app
3. Select **Windows Computer** (or your device type)
4. Google will generate a 16-character password
5. Use that password in `EMAIL_HOST_PASSWORD`

### Step 2: Database Setup

When you connect a PostgreSQL database on Render:
1. Click **Create Database** → select **PostgreSQL**
2. The `DATABASE_URL` will be automatically set
3. The database will be properly initialized on first deploy

### Step 3: Deploy

Push your code to GitHub. The `render.yaml` file will automatically:
- Install all dependencies
- Run migrations to create tables
- Collect static files
- Start the application with proper PostgreSQL support

### Step 4: Verify Setup

After first deployment:
1. Visit your app URL
2. Go to **Signup** page
3. Test the signup → OTP → verify flow
4. The OTP should now work without errors

## Why These Changes Were Made

### In `settings.py`:
- ✅ Added PostgreSQL support via `dj-database-url`
- ✅ Uses environment variables instead of hardcoded values
- ✅ Added WhiteNoise for static files on Render
- ✅ Security settings for HTTPS in production
- ✅ Uses `decouple` to safely load environment variables

### In `views.py` (signup and verify_otp):
- ✅ Better error handling for email failures
- ✅ Validates session data exists before using it
- ✅ Checks for duplicate email before creating user
- ✅ Handles database exceptions gracefully
- ✅ Sets session expiry time (10 minutes)

### New Files:
- ✅ `.env.example` - shows required environment variables
- ✅ `render.yaml` - Render deployment configuration
- ✅ `.gitignore` - prevents committing sensitive files

## Troubleshooting

### "ModuleNotFoundError: No module named 'dj_database_url'"
- Run `pip install -r requirements.txt` locally
- Push the change to GitHub
- Render will auto-install on next deploy

### Email not sending
- Check that `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set correctly
- Verify you're using an **App Password** (not your Gmail password)
- Check Render logs for email errors: In dashboard, go to **Logs**

### Database not created
- Make sure `DATABASE_URL` is properly set in Environment variables
- Run manual migration: In Render dashboard, open a shell and run:
  ```
  python manage.py migrate
  ```

### Still getting errors?
- Check Render logs for the actual error message
- In Render dashboard, click **Logs** to see detailed errors
- Share error message from logs for debugging

## Local Development

To develop locally before deploying:

1. Create `.env` file (never commit this):
   ```
   DEBUG=True
   SECRET_KEY=your-local-secret-key
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

2. The app will use SQLite locally (which is fine for development)

3. Test signup/OTP flow before pushing to Render

## Security Notes

⚠️ **Never commit `.env` file to GitHub!**
- The `.gitignore` file will prevent this
- Always use environment variables on Render
- Rotate email app passwords regularly

---

For more help, check Render's documentation: https://render.com/docs
