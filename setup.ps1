# CYBER-DEF25 Challenge - Setup and Usage Guide

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CYBER-DEF25 Malware Detection System - Setup Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Docker
if (Test-Command docker) {
    $dockerVersion = docker --version
    Write-Host "[OK] Docker installed: $dockerVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Docker is not installed!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check Docker Compose
if (Test-Command docker-compose) {
    $composeVersion = docker-compose --version
    Write-Host "[OK] Docker Compose installed: $composeVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Docker Compose is not installed!" -ForegroundColor Red
    exit 1
}

# Check Python
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "[OK] Python installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Python is not installed - required for model generation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setup Steps" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create model if it doesn't exist
if (-not (Test-Path "model.pkl")) {
    Write-Host "[Step 1] Generating model.pkl..." -ForegroundColor Yellow
    if (Test-Command python) {
        python create_model.py
        if (Test-Path "model.pkl") {
            Write-Host "[OK] model.pkl created successfully" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Failed to create model.pkl" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "[ERROR] Python not found - cannot generate model" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[Step 1] model.pkl already exists" -ForegroundColor Green
}
Write-Host ""

# Step 2: Create necessary directories
Write-Host "[Step 2] Creating directories..." -ForegroundColor Yellow
@('network_logs', 'output', 'input/logs') | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Host "  Created: $_" -ForegroundColor Gray
    }
}
Write-Host "[OK] Directories ready" -ForegroundColor Green
Write-Host ""

# Step 3: Build Docker image
Write-Host "[Step 3] Building Docker image..." -ForegroundColor Yellow
docker build -t cyber-def25-malware-detection:latest .
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Docker build failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Display usage instructions
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Place your network log files (CSV format) in:" -ForegroundColor White
Write-Host "   ./network_logs/" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Run the container using Docker Compose:" -ForegroundColor White
Write-Host "   docker-compose up" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Check the results in:" -ForegroundColor White
Write-Host "   ./output/alerts.csv" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. For Jenkins pipeline:" -ForegroundColor White
Write-Host "   - Configure Docker Hub credentials in Jenkins" -ForegroundColor Gray
Write-Host "   - Update DOCKER_IMAGE in Jenkinsfile" -ForegroundColor Gray
Write-Host "   - Create a new Pipeline job" -ForegroundColor Gray
Write-Host "   - Point to your repository" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Additional Commands:" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run container directly:" -ForegroundColor White
Write-Host '  docker run -v ${PWD}/network_logs:/input/logs -v ${PWD}/output:/output cyber-def25-malware-detection:latest' -ForegroundColor Cyan
Write-Host ""
Write-Host "View Docker images:" -ForegroundColor White
Write-Host "  docker images" -ForegroundColor Cyan
Write-Host ""
Write-Host "View running containers:" -ForegroundColor White
Write-Host "  docker ps" -ForegroundColor Cyan
Write-Host ""
Write-Host "View container logs:" -ForegroundColor White
Write-Host "  docker-compose logs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Clean up:" -ForegroundColor White
Write-Host "  docker-compose down" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
