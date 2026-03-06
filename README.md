# ![Schooli Logo](static/images/resulthub.png) Schooli – Result Management System

Schooli is a secure and user-friendly web-based Result Management System developed for managing and publishing student examination results digitally. The system allows administrators to upload and manage results, while students can check their results easily by selecting their college and entering their symbol number — without requiring a login.

## 📌 Project Overview

Schooli is designed to simplify the traditional result management process by replacing manual paperwork with a digital solution. The system includes:

- Frontend interface for students
- Backend server for processing requests
- Admin Panel for school administrators
- Result checking system
- Blog/News section
- Digital marksheets

The project is built using:
- **Backend**: Django 5.2 (Python Framework)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Render

## ⚙️ Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Online_result
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # Windows
   # or
   source env/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r result_checker_site/requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   cp .env.example .env
   # Edit .env and add your email credentials
   ```

5. **Run migrations**
   ```bash
   cd result_checker_site
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000`

## 🚀 Deployment on Render

**⚠️ IMPORTANT:** The app uses **SQLite by default locally** but **PostgreSQL in production**. This is configured automatically via `DATABASE_URL` environment variable.

### Steps to Deploy:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **On Render Dashboard:**
   - Click **Create** → **Web Service**
   - Connect your GitHub repository
   - Render will automatically use `render.yaml` for configuration

3. **Set Environment Variables:**
   In Render dashboard, add these:
   ```
   DEBUG=False
   DATABASE_URL=<auto-set by Render>
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

4. **For Email (Gmail):**
   - Go to https://myaccount.google.com/apppasswords
   - Select **Mail** and your device type
   - Generate app password
   - Use that password in `EMAIL_HOST_PASSWORD`

5. **Deploy**
   - Render will automatically build and deploy
   - Check logs if there are any issues

### Common Issues Fixed:

✅ **OTP verification failing with internal server error**
- Fixed by using PostgreSQL instead of SQLite
- Database now persists across deployments

✅ **Session data being lost**
- Added proper session expiry handling
- Email errors no longer crash the app

✅ **Static files not loading**
- Added WhiteNoise for static file serving
- CSS/JS now load properly in production

✅ **Email not sending**
- Improved error handling
- Can now test without email config

## 📁 Project Structure

```
result_checker_site/
├── results/
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, Images
├── result_checker/
│   └── settings.py        # Django settings
├── manage.py
└── requirements.txt       # Python dependencies
```

## 🔐 Security Notes

- Never commit `.env` file (protected by `.gitignore`)
- Always use environment variables for secrets
- Use Gmail App Passwords, not regular passwords
- Change `SECRET_KEY` in production

## 📚 Features

### For Students:
- Search results by symbol number
- View detailed result cards
- Print marksheets
- View grade distributions

### For Admins:
- Upload results via Excel/CSV
- Manual result entry
- Manage schools
- View all results with filters
- Export data in Excel/CSV
- Print marksheets

## 🏫 Technologies Used

- **Backend**: Django 5.2
- **Database**: PostgreSQL (Render) / SQLite (Local)
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Gunicorn
- **Hosting**: Render.com
- **Static Files**: WhiteNoise

## 📝 License

This project is developed for educational purposes.

## 🤝 Support

For setup help, see `RENDER_DEPLOYMENT.md` for detailed deployment instructions.

---

**Last Updated**: March 2026
**Status**: Production Ready
