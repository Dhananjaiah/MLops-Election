# Lecture 2.8 – Troubleshooting Common Setup Issues (Ports, Docker, Permissions, Proxies)

## In This Lecture You Will Learn

- [x] Diagnose and fix common development environment problems
- [x] Resolve Docker, port conflicts, and permission issues  
- [x] Work around corporate firewall and proxy restrictions

---

## Real-World Context

> **Story**: First day at a new job, Alex spent 6 hours unable to run Docker because port 8080 was taken by a corporate monitoring tool. No one told him to check running processes first. This lecture is the troubleshooting guide Alex wished he had.
>
> Environment issues are inevitable. Knowing how to fix them quickly is a superpower.

Every developer encounters setup problems. The difference between juniors and seniors is how fast they debug them.

---

## Main Content

### 1. Port Conflicts

**Problem**: "Address already in use"

```bash
# Symptom
docker run -p 8000:8000 my-api
Error: bind: address already in use

# Diagnosis: Find what's using the port
# On macOS/Linux:
lsof -i :8000

# On Windows:
netstat -ano | findstr :8000

# Solution 1: Kill the process
kill -9 <PID>

# Solution 2: Use a different port
docker run -p 8001:8000 my-api
```

**Common port conflicts:**
- 8000, 8080: Often used by dev servers
- 5000: macOS AirPlay Receiver (disable in System Preferences)
- 3000: React/Node development servers
- 5432: PostgreSQL

### 2. Docker Issues

#### **Problem: Docker Desktop Won't Start**

```bash
# Windows Solution:
# 1. Enable WSL2
wsl --install
# 2. Set WSL2 as default
wsl --set-default-version 2
# 3. Restart Docker Desktop

# macOS Solution:
# Reset Docker to factory defaults in Settings

# Linux Solution:
sudo systemctl start docker
sudo systemctl enable docker
```

#### **Problem: Permission Denied**

```bash
# Symptom
docker run hello-world
permission denied while trying to connect to Docker daemon

# Solution (Linux):
sudo usermod -aG docker $USER
newgrp docker
# Then log out and back in
```

#### **Problem: Disk Space**

```bash
# Diagnosis:
docker system df

# Solution: Clean up
docker system prune -a  # Remove all unused data
docker volume prune     # Remove unused volumes
```

### 3. Python Virtual Environment Issues

**Problem: "No module named 'X'" after installing**

```bash
# Check which Python/pip
which python
which pip

# Solution: Always activate venv first!
source venv/bin/activate
pip install -r requirements.txt
```

**Problem: "command not found: python"**

```bash
# Solution: Create alias
echo "alias python=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc
source ~/.bashrc
```

### 4. Corporate Proxy Issues

**Problem: pip/Docker can't download**

```bash
# Configure pip proxy
pip install --proxy http://user:pass@proxy:port package

# Or set environment variable
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# Configure Docker proxy
# Create ~/.docker/config.json
```

### 5. Git Issues

**Problem: Authentication failed**

```bash
# GitHub deprecated password auth

# Solution: Use Personal Access Token
# Generate token: GitHub → Settings → Developer settings → PAT
# Or: gh auth login

# For SSH:
ssh-keygen -t ed25519 -C "your@email.com"
# Add ~/.ssh/id_ed25519.pub to GitHub
```

---

## Diagrams

```
Troubleshooting Workflow:
════════════════════════

Error occurs
     │
     ▼
Read error message carefully
     │
     ├─ Port conflict? → lsof/netstat → kill or change port
     ├─ Permission? → Check user/group → sudo usermod
     ├─ Not found? → which command → Check PATH
     ├─ Network? → Test connection → Configure proxy
     └─ Still broken? → Search Stack Overflow
```

---

## Lab / Demo

### Prerequisites

- Issues from previous lectures  
- Patience and systematic debugging mindset

### Step-by-Step Instructions

```bash
# Exercise 1: Simulate port conflict
# Terminal 1:
python -m http.server 8000

# Terminal 2:
python -m http.server 8000  # Should fail

# Find and fix:
lsof -i :8000
kill <PID>

# Exercise 2: Test Docker
docker run hello-world
```

### Expected Output

```
$ lsof -i :8000
COMMAND   PID   USER
Python    1234  yourname

$ docker run hello-world
Hello from Docker!
```

### Explanation

1. Port conflicts are common when multiple services try to use the same port
2. Docker issues often relate to permissions or the daemon not running
3. Always check which python/pip you're using when in doubt

---

## Common Pitfalls / Gotchas

- ⚠️ **Pitfall 1**: Not reading error messages. They usually tell you exactly what's wrong.

- ⚠️ **Pitfall 2**: Running commands without checking context (venv active? Right directory?).

- ⚠️ **Pitfall 3**: Using outdated solutions from 2015 blog posts. Check dates!

---

## Homework / Practice

1. **Exercise 1**: Intentionally break your setup then fix it. Practice makes perfect.

2. **Exercise 2**: Document your own troubleshooting wins for future reference.

3. **Stretch Goal**: Help someone else with setup issues on the course Discussion forum.

---

## Quick Quiz

1. **What command finds which process is using port 8000?**
   - A) `ps aux | grep 8000`
   - B) `lsof -i :8000`
   - C) `netstat 8000`
   - D) `docker ps 8000`

2. **Why might pip install fail behind a corporate firewall?**
   - A) Python is blocked
   - B) Need to configure proxy settings
   - C) pip doesn't work on corporate networks
   - D) Must use conda instead

3. **True or False: You should always run Docker with sudo.**

<details>
<summary>Answers</summary>

1. **B** - `lsof -i :PORT` shows which process uses a port
2. **B** - Corporate firewalls often require proxy configuration
3. **False** - Add yourself to docker group to avoid sudo

</details>

---

## Summary

- Port conflicts: Use `lsof` to find, kill or change port
- Docker issues: Check daemon, permissions, disk space
- Virtual environment: Always activate before pip install
- Proxy: Configure in pip, Docker, and Git
- Git auth: Use tokens or SSH, not passwords
- Systematic debugging beats random Stack Overflow copying

---

## Next Steps

→ Continue to **Section 3**: Understanding the ML Lifecycle & MLOps Responsibilities

---

## Additional Resources

- [Docker Troubleshooting](https://docs.docker.com/config/daemon/troubleshoot/) - Official guide
- [Stack Overflow](https://stackoverflow.com/) - Search exact error messages
- [GitHub Issues](https://github.com/issues) - Check known issues
- [Course Discussion Forum](https://github.com/yourusername/mlops-course/discussions) - Ask questions
