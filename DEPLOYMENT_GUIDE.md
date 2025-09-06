# BridgeCanvas Deployment Guide

## Overview
BridgeCanvas is a professional bridge design application that generates DXF drawings and analysis reports from Excel parameter files. This guide covers deployment options for both Vercel (Flask) and Streamlit Cloud.

## 🚀 Quick Start Options

### Option 1: Flask App (Vercel Deployment)
- **Best for**: Production deployments, custom domains, serverless functions
- **Features**: Full web interface, database support, professional UI
- **Run locally**: Double-click `run_bridge_app.bat`

### Option 2: Streamlit App (Streamlit Cloud)
- **Best for**: Data science teams, rapid prototyping, interactive analysis
- **Features**: Interactive widgets, real-time updates, data visualization
- **Run locally**: Double-click `run_streamlit_app.bat`

## 📋 Prerequisites

### System Requirements
- Windows 10/11 (for local development)
- Python 3.8 or higher
- 4GB RAM minimum
- 1GB free disk space

### Required Software
1. **Python 3.8+**: Download from [python.org](https://python.org)
2. **Git**: Download from [git-scm.com](https://git-scm.com)
3. **Web Browser**: Chrome, Firefox, or Edge

## 🏃‍♂️ Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/BridgeCanvas.git
cd BridgeCanvas
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application

#### Flask App (Port 5000)
```bash
# Option A: Use batch file (Windows)
run_bridge_app.bat

# Option B: Command line
python app.py
```

#### Streamlit App (Port 8501)
```bash
# Option A: Use batch file (Windows)
run_streamlit_app.bat

# Option B: Command line
cd streamlit_app
streamlit run streamlit_app.py
```

### 4. Access Application
- **Flask**: http://localhost:5000
- **Streamlit**: http://localhost:8501

## 🌐 Vercel Deployment (Flask)

### 1. Prepare for Vercel
- Ensure `vercel.json` is in root directory
- Verify `requirements.txt` is up to date
- Test locally with `python app.py`

### 2. Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### 3. Environment Variables
Set in Vercel dashboard:
- `DATABASE_URL`: Your database connection string
- `SESSION_SECRET`: Random secret for session management

### 4. Custom Domain (Optional)
- Add domain in Vercel dashboard
- Configure DNS records
- Enable HTTPS

## ☁️ Streamlit Cloud Deployment

### 1. Prepare Repository
- Ensure `streamlit_app/` directory contains all files
- Verify `requirements.txt` is in root directory
- Test locally with Streamlit

### 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set main file path: `streamlit_app/streamlit_app.py`
4. Click "Deploy"

### 3. Configuration
- **Python version**: 3.8+
- **Requirements file**: `requirements.txt`
- **Main file**: `streamlit_app/streamlit_app.py`

## 🔧 Configuration Options

### Environment Variables
```bash
# Flask App
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:port/db
SESSION_SECRET=your-secret-key

# Streamlit App
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Database Configuration
```python
# SQLite (default, local development)
DATABASE_URL = "sqlite:///bridge_designs.db"

# PostgreSQL (production)
DATABASE_URL = "postgresql://user:pass@host:port/db"
```

## 📁 File Structure
```
BridgeCanvas/
├── app.py                 # Flask application
├── bridge_processor.py    # Core bridge logic
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── run_bridge_app.bat    # Flask launcher
├── run_streamlit_app.bat # Streamlit launcher
├── streamlit_app/        # Streamlit application
│   ├── streamlit_app.py  # Streamlit interface
│   ├── bridge_processor.py
│   └── .streamlit/       # Streamlit configuration
├── templates/            # HTML templates
├── static/              # Static assets
├── uploads/             # File uploads
└── generated/           # Output files
```

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :5000

# Kill process
taskkill /PID <process_id> /F
```

#### Python Not Found
- Ensure Python is in PATH
- Restart command prompt after Python installation
- Verify with `python --version`

#### Package Installation Errors
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with user flag
pip install --user -r requirements.txt
```

#### DXF Generation Errors
- Check Excel file format (.xlsx or .xls)
- Verify required columns exist
- Check file permissions in generated/ directory

### Performance Optimization

#### Flask App
- Enable gunicorn for production
- Use Redis for session storage
- Implement file caching

#### Streamlit App
- Use `@st.cache_data` for expensive operations
- Optimize data processing
- Implement lazy loading

## 🔒 Security Considerations

### Production Deployment
- Change default secret keys
- Enable HTTPS
- Implement rate limiting
- Add input validation
- Use environment variables for secrets

### File Upload Security
- Validate file types
- Limit file sizes
- Scan for malware
- Store files securely

## 📊 Monitoring and Logging

### Application Logs
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Performance Monitoring
- Response time tracking
- Error rate monitoring
- Resource usage monitoring
- User activity analytics

## 🔄 Updates and Maintenance

### Regular Updates
- Update dependencies monthly
- Security patches immediately
- Feature updates quarterly
- Database backups daily

### Backup Strategy
```bash
# Database backup
sqlite3 bridge_designs.db ".backup backup.db"

# File backup
xcopy generated backup\generated /E /I
```

## 📞 Support and Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Vercel Documentation](https://vercel.com/docs)

### Community
- GitHub Issues
- Stack Overflow
- Discord Community

### Professional Support
- Email: support@bridgecanvas.com
- Phone: +1-555-BRIDGE
- Hours: Mon-Fri 9AM-6PM EST

---

**Last Updated**: December 2024
**Version**: 2.0.0
**Author**: BridgeCanvas Team
