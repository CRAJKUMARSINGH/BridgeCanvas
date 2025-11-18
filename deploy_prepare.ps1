# BridgeCanvas Deployment Preparation Script
# Prepares the application for deployment to GitHub

Write-Host "========================================" -ForegroundColor Green
Write-Host "  BridgeCanvas Deployment Preparation  " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 1. Create .gitignore if not exists
Write-Host "[1/5] Setting up .gitignore..." -ForegroundColor Cyan
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
uploads/*
!uploads/.gitkeep
generated/*
!generated/.gitkeep
temp/
*.log

# Replit
.replit
replit.nix
.local/
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host "✅ .gitignore configured" -ForegroundColor Green

# 2. Create placeholder files for empty directories
Write-Host "[2/5] Creating directory placeholders..." -ForegroundColor Cyan
@("uploads", "generated") | ForEach-Object {
    if (!(Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
    Set-Content -Path "$_/.gitkeep" -Value ""
}
Write-Host "✅ Directory placeholders created" -ForegroundColor Green

# 3. Update README with deployment info
Write-Host "[3/5] Checking README..." -ForegroundColor Cyan
if (Test-Path "README.md") {
    Write-Host "✅ README.md exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  README.md not found" -ForegroundColor Yellow
}

# 4. Verify deployment files
Write-Host "[4/5] Verifying deployment files..." -ForegroundColor Cyan
$deploymentFiles = @{
    "vercel.json" = "Vercel deployment"
    "requirements.txt" = "Python dependencies"
    "app.py" = "Flask application"
    "bridge_processor.py" = "Core processor"
}

foreach ($file in $deploymentFiles.Keys) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file ($($deploymentFiles[$file]))" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing" -ForegroundColor Red
    }
}

# 5. Show git status
Write-Host "[5/5] Git status..." -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deployment Preparation Complete!     " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review changes: git status" -ForegroundColor White
Write-Host "  2. Add files: git add ." -ForegroundColor White
Write-Host "  3. Commit: git commit -m 'Optimize and prepare for deployment'" -ForegroundColor White
Write-Host "  4. Push: git push origin main" -ForegroundColor White
Write-Host ""
