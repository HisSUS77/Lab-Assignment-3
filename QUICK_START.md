# CYBER-DEF25 Challenge - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Python 3.9+ installed

### Quick Setup

#### 1️⃣ Generate the Model (30 seconds)
```powershell
python create_model.py
```
✅ Creates `model.pkl`

#### 2️⃣ Build Docker Image (2-3 minutes)
```powershell
docker build -t cyber-def25-malware-detection:latest .
```
✅ Creates containerized application

#### 3️⃣ Run the Application (30 seconds)
```powershell
docker-compose up
```
✅ Processes logs and generates alerts

#### 4️⃣ View Results
```powershell
cat output/alerts.csv
```
✅ See detected threats

---

## 📋 File Checklist

Before running, ensure these files exist:

✅ `Dockerfile` - Container definition  
✅ `docker-compose.yml` - Orchestration config  
✅ `Jenkinsfile` - CI/CD pipeline  
✅ `inference.py` - Main script  
✅ `requirements.txt` - Dependencies  
✅ `model.pkl` - Trained model  
✅ `network_logs/` - Input directory (with CSV files)  

---

## 🔧 Common Commands

### Docker
```powershell
# Build image
docker build -t cyber-def25-malware-detection:latest .

# Run manually
docker run -v ${PWD}/network_logs:/input/logs -v ${PWD}/output:/output cyber-def25-malware-detection:latest

# List images
docker images

# Remove image
docker rmi cyber-def25-malware-detection:latest
```

### Docker Compose
```powershell
# Start
docker-compose up

# Start in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs

# Rebuild and start
docker-compose up --build
```

### Jenkins Setup
```powershell
# 1. Add Docker Hub credentials in Jenkins:
#    Manage Jenkins → Credentials → Add Credentials
#    - ID: dockerhub-credentials
#    - Username: [your-dockerhub-username]
#    - Password: [your-dockerhub-token]

# 2. Update Jenkinsfile:
#    Change: DOCKER_IMAGE = 'your-dockerhub-username/cyber-def25-malware-detection'
#    To: DOCKER_IMAGE = '[actual-username]/cyber-def25-malware-detection'

# 3. Create Pipeline Job:
#    New Item → Pipeline → Pipeline script from SCM → Git → [your-repo]
```

---

## 📊 Expected Output

### Console Output
```
============================================================
CYBER-DEF25 Malware Detection System - Starting Analysis
============================================================
INFO - Loading model from /app/model.pkl
INFO - Model loaded successfully
INFO - Found 1 log file(s) to process
INFO - Processing log file: /input/logs/sample_logs.csv
INFO - Loaded 10 log entries from /input/logs/sample_logs.csv
INFO - Detected 3 potential threats out of 10 log entries
============================================================
THREAT DETECTION SUMMARY
============================================================
Total Threats Detected: 3
High Severity: 1
Medium Severity: 1
Low Severity: 1
============================================================
```

### alerts.csv
```csv
timestamp,source_file,log_entry_id,threat_detected,threat_probability,severity,action_recommended
2025-11-28 12:00:00,sample_logs.csv,0,1,0.95,HIGH,BLOCK
2025-11-28 12:00:00,sample_logs.csv,3,1,0.67,MEDIUM,MONITOR
2025-11-28 12:00:00,sample_logs.csv,7,1,0.42,LOW,ALLOW
```

---

## 🐛 Troubleshooting

### Problem: "model.pkl not found"
**Solution:**
```powershell
python create_model.py
```

### Problem: "No log files found"
**Solution:**
```powershell
# Create sample log
Copy-Item network_logs/sample_logs.csv network_logs/test_logs.csv
```

### Problem: "Permission denied: output/"
**Solution:**
```powershell
mkdir -p output
chmod 777 output  # Linux/Mac
# or
icacls output /grant Users:F  # Windows
```

### Problem: Docker build fails
**Solution:**
```powershell
# Clean Docker cache
docker system prune -a
# Rebuild
docker build --no-cache -t cyber-def25-malware-detection:latest .
```

### Problem: Jenkins can't push to Docker Hub
**Solution:**
1. Check credentials: `dockerhub-credentials` exists in Jenkins
2. Use access token instead of password
3. Verify Docker Hub username in Jenkinsfile

---

## 📁 Project Structure
```
Lab-Assignment-3/
├── Dockerfile                    ← Part A: Container definition
├── docker-compose.yml            ← Part B: Orchestration with volume mounts
├── Jenkinsfile                   ← Part C: CI/CD pipeline
├── inference.py                  ← Main application
├── requirements.txt              ← Dependencies
├── model.pkl                     ← Trained model (generate first!)
├── create_model.py               ← Model generator
├── network_logs/                 ← INPUT: Place CSV files here
│   └── sample_logs.csv
└── output/                       ← OUTPUT: alerts.csv appears here
    └── alerts.csv
```

---

## ✅ Submission Checklist

For CYBER-DEF25 Challenge:

- [ ] Dockerfile created and tested
- [ ] docker-compose.yml with volume mounts
- [ ] Jenkinsfile with build/push/run stages
- [ ] model.pkl generated
- [ ] inference.py functional
- [ ] requirements.txt complete
- [ ] README.md documentation
- [ ] ASSIGNMENT_REPORT.md with screenshots
- [ ] All files in Git repository
- [ ] Docker Hub image pushed (optional)

---

## 🎯 Next Steps

### For Assignment Submission:
1. Take screenshots of each step
2. Fill in the ASSIGNMENT_REPORT.md template
3. Export report as PDF
4. Submit to instructor

### For Jenkins Pipeline:
1. Install Jenkins (if not already)
2. Configure Docker Hub credentials
3. Create pipeline job
4. Run and capture screenshots

### For Production:
1. Add security scanning
2. Implement monitoring
3. Set up Kubernetes deployment
4. Add automated testing

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review `ASSIGNMENT_REPORT.md` for step-by-step guide
3. Run `setup.ps1` for automated setup
4. Check Docker/Jenkins logs for errors

---

## 🎓 Learning Resources

- **Docker:** https://docs.docker.com/get-started/
- **Docker Compose:** https://docs.docker.com/compose/gettingstarted/
- **Jenkins:** https://www.jenkins.io/doc/tutorials/
- **ML with Python:** https://scikit-learn.org/stable/tutorial/

---

**Good luck with your CYBER-DEF25 Challenge! 🚀**
