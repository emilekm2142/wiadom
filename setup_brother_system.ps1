# Wiadom Setup Script
# Run this as Administrator in PowerShell

Write-Host "🚀 Setting up Wiadom..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script needs to be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Create directory for the project
$projectDir = "$env:USERPROFILE\Documents\Wiadom"
Write-Host "📁 Creating project directory: $projectDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $projectDir | Out-Null
Set-Location $projectDir

# Download and install Python if not already installed
Write-Host "🐍 Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python is already installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "📥 Python not found. Installing Python..." -ForegroundColor Yellow
    
    # Download Python installer
    $pythonUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    Write-Host "⬇️ Downloading Python installer..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    
    Write-Host "🔧 Installing Python..." -ForegroundColor Cyan
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
    
    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "✅ Python installation completed!" -ForegroundColor Green
}

# Check if Git is installed
Write-Host "Checking Git installation..." -ForegroundColor Cyan
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found! Installing Git..." -ForegroundColor Yellow
    
    # Download Git installer
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe"
    $gitInstaller = "$env:TEMP\git-installer.exe"
    
    Write-Host "⬇️ Downloading Git installer..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
    
    Write-Host "🔧 Installing Git..." -ForegroundColor Cyan
    Start-Process -FilePath $gitInstaller -ArgumentList "/SILENT" -Wait
    
    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "✅ Git installation completed!" -ForegroundColor Green
}

# Download the code from GitHub
Write-Host "📥 Downloading Wiadom from GitHub..." -ForegroundColor Cyan
try {
    git clone https://github.com/emilekm2142/wiadom.git .
    Write-Host "✅ Code downloaded successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download from GitHub!" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
    pause
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Create startup script (visible version)
@"
@echo off
echo Starting Wiadom...
cd /d "%~dp0"
python wiadom.py
pause
"@ | Out-File -FilePath "start_wiadom.bat" -Encoding ASCII

# Create silent startup script for autostart
@"
@echo off
cd /d "%~dp0"
pythonw wiadom.py
"@ | Out-File -FilePath "start_wiadom_silent.bat" -Encoding ASCII

# Create desktop shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Wiadom.lnk")
$Shortcut.TargetPath = "$projectDir\start_wiadom.bat"
$Shortcut.WorkingDirectory = $projectDir
$Shortcut.IconLocation = "shell32.dll,25"
$Shortcut.Description = "Wiadom - Message System"
$Shortcut.Save()

# Add to Windows startup folder (autostart)
Write-Host "🚀 Adding Wiadom to Windows startup..." -ForegroundColor Cyan
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$startupShortcut = "$startupFolder\Wiadom.lnk"

# Create startup shortcut
$WshShell = New-Object -comObject WScript.Shell
$StartupShortcut = $WshShell.CreateShortcut($startupShortcut)
$StartupShortcut.TargetPath = "$projectDir\start_wiadom_silent.bat"
$StartupShortcut.WorkingDirectory = $projectDir
$StartupShortcut.WindowStyle = 7  # Minimized
$StartupShortcut.Description = "Wiadom - Auto Start"
$StartupShortcut.Save()

Write-Host "✅ Wiadom will now start automatically with Windows!" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Add your .wav sound files to the 'sounds' folder" -ForegroundColor White
Write-Host "2. Add your image files (.jpg, .png, .gif) to the main folder" -ForegroundColor White
Write-Host "3. Double-click 'Wiadom' on desktop to start" -ForegroundColor White
Write-Host ""
Write-Host "📁 Project location: $projectDir" -ForegroundColor Yellow
Write-Host "🌐 Web interface will be at: http://localhost:8080" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to open the project folder..." -ForegroundColor Green
pause
explorer $projectDir