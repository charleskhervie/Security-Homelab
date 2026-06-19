---
title: "Project 2: Hardened Linux Server, Backup Automation & Disaster Recovery"
date: 2026-06-19
categories: [Homelab, Linux Hardening]
tags: [Ubuntu, Linux-Hardening, Nginx, SSH, UFW, Fail2Ban, CIS-Benchmark, Backup, Disaster-Recovery]
toc: true

---

## Objective & Network Topology

The goal of this project was to provision, harden, and automate a production-style Ubuntu Server 22.04 LTS instance inside the existing homelab environment. The server simulates an internal corporate web service running Nginx, secured with layered Linux hardening controls, and protected by a tested backup and disaster recovery workflow.

### Network Architecture

```text
Isolated Host-Only Virtual Network (192.168.10.0/24)

Windows Server 2022 Domain Controller
IP: 192.168.10.10
Role: Identity and DNS baseline from Project 1

Ubuntu Server 22.04 LTS
IP: 192.168.10.20
Role: Hardened Nginx web server, backup host, future Wazuh agent
```

### Environment Specifications

- **Operating System**: Ubuntu Server 22.04 LTS Minimal Install
- **Hostname**: `ubuntuserver`
- **Static IP**: 192.168.10.20
- **Network Configuration**: Same host-only segment as the Domain Controller
- **Primary Services**: Nginx, OpenSSH, UFW, Fail2Ban, cron-based backup automation
- **Security Baseline**: CIS-inspired Ubuntu Server hardening controls

---

## Step-by-Step Implementation

### 1. VM Provisioning & Static IP Configuration

The Ubuntu Server VM was built as a minimal, no-GUI server to mirror a production Linux deployment. Starting with fewer packages reduces the initial attack surface and forces administration through the shell, which is the normal operating model for hardened infrastructure.

**Implementation steps:**

- Created a new VMware Workstation Pro VM with 2 GB RAM, 2 CPU cores, and a 20 GB disk
- Installed Ubuntu Server 22.04 LTS using the minimal install option
- Enabled OpenSSH Server during installation for remote administration
- Assigned a static IPv4 address so the server could consistently communicate with the lab domain environment

![VM Provisioning](/assets/img/posts/project2%20hardened%20linux/1.png){: width="700" .no-lazy}
_VMware Workstation configuration for the Ubuntu Server VM_

![Static IP Configuration](/assets/img/posts/project2%20hardened%20linux/2.png){: width="700" .no-lazy}
_Ubuntu installer network configuration with static addressing_

![Ubuntu Installer Summary](/assets/img/posts/project2%20hardened%20linux/3.png){: width="700" .no-lazy}
_Installer summary before finalizing the minimal server deployment_

![Initial Ubuntu Login](/assets/img/posts/project2%20hardened%20linux/4.png){: width="700" .no-lazy}
_First console login after installation_

**Network validation:**

```bash
ping 192.168.10.10
```

```powershell
ping 192.168.10.20
```

![Ubuntu to Domain Controller Ping](/assets/img/posts/project2%20hardened%20linux/5.png){: width="700" .no-lazy}
_Ubuntu Server successfully reaching the Domain Controller_

![Windows to Ubuntu Ping](/assets/img/posts/project2%20hardened%20linux/6.png){: width="700" .no-lazy}
_Windows lab host successfully reaching the Ubuntu server_

### 2. Nginx Web Server Deployment

Nginx was deployed to simulate a corporate internal web portal hosted inside the lab subnet. This created a realistic service to protect, monitor, back up, break, and restore during the later disaster recovery test.

**Commands executed:**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

![Nginx Service Status](/assets/img/posts/project2%20hardened%20linux/7.png){: width="700" .no-lazy}
_Nginx service running and active on the Ubuntu server_

![Nginx Enabled on Boot](/assets/img/posts/project2%20hardened%20linux/8.png){: width="700" .no-lazy}
_Nginx enabled to start automatically after reboot_

The default web page was later customized to make restore validation obvious during the disaster recovery test.

```bash
sudo nano /var/www/html/index.html
```

![Internal Portal HTML](/assets/img/posts/project2%20hardened%20linux/9.png){: width="700" .no-lazy}
_Custom internal web page content configured under `/var/www/html`_

![Browser Web Test](/assets/img/posts/project2%20hardened%20linux/10.png){: width="700" .no-lazy}
_Nginx web page reachable from the Windows lab host_

### 3. SSH Hardening

The default SSH posture was hardened because password-based logins on port 22 are one of the most common targets for brute-force attacks. Administration was moved to key-based authentication on a non-standard port with root login disabled.

#### 3.1 Generate SSH Key Pair

The key pair was generated from the Windows administrator workstation.

```powershell
ssh-keygen -t ed25519 -C "lab-admin@lab.corp.local"
```

![SSH Key Generation](/assets/img/posts/project2%20hardened%20linux/11.png){: width="700" .no-lazy}
_ED25519 SSH key pair generated from the Windows VM_

#### 3.2 Install the Public Key

The public key was copied into the Ubuntu user's `authorized_keys` file.

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ubuntu_server@192.168.10.20 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

![Authorized Keys Verification](/assets/img/posts/project2%20hardened%20linux/12.png){: width="700" .no-lazy}
_Public key present in `~/.ssh/authorized_keys`_

![SSH Key Copy Test](/assets/img/posts/project2%20hardened%20linux/13.png){: width="700" .no-lazy}
_SSH key material copied from the Windows workstation to the Linux server_

#### 3.3 Harden SSH Daemon Configuration

The SSH daemon configuration was modified to remove password authentication, block root login, reduce retry attempts, and move administration to port `2222`.

```text
# /etc/ssh/sshd_config
Port 2222
PermitRootLogin no
PasswordAuthentication no
PermitEmptyPasswords no
AllowUsers ubuntu_server
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 0
X11Forwarding no
```

```bash
sudo systemctl restart sshd
```

![Hardened SSHD Config](/assets/img/posts/project2%20hardened%20linux/14.png){: width="700" .no-lazy}
_Hardened SSH daemon settings applied in `/etc/ssh/sshd_config`_

![Key-Based SSH Login](/assets/img/posts/project2%20hardened%20linux/15.png){: width="700" .no-lazy}
_Successful SSH login using the ED25519 key on port `2222`_

### 4. UFW Firewall Configuration

A default-deny firewall posture was applied. Only the lab subnet was allowed to reach the hardened SSH port and web service ports.

**Firewall baseline:**

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 192.168.10.0/24 to any port 2222 proto tcp
sudo ufw allow from 192.168.10.0/24 to any port 80 proto tcp
sudo ufw allow from 192.168.10.0/24 to any port 443 proto tcp
sudo ufw enable
```

![UFW Rules Applied](/assets/img/posts/project2%20hardened%20linux/16.png){: width="700" .no-lazy}
_UFW configured with lab-subnet-only access rules_

![UFW Status Verbose](/assets/img/posts/project2%20hardened%20linux/17.png){: width="700" .no-lazy}
_UFW active with default deny and explicit allow rules for ports `2222`, `80`, and `443`_

### 5. Fail2Ban Brute Force Protection

Fail2Ban was added as an additional detection and response layer. Even though SSH passwords were disabled, Fail2Ban still provides useful telemetry and automatic response when repeated authentication failures occur.

**Installation and service setup:**

```bash
sudo apt install fail2ban -y
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
sudo systemctl enable --now fail2ban
```

![Fail2Ban Service Check](/assets/img/posts/project2%20hardened%20linux/18.png){: width="700" .no-lazy}
_Initial Fail2Ban service status check_

**SSH jail configuration:**

```ini
[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

![Fail2Ban SSH Jail](/assets/img/posts/project2%20hardened%20linux/19.png){: width="700" .no-lazy}
_Fail2Ban SSH jail configured for the hardened SSH port_

**Verification command:**

```bash
sudo fail2ban-client status sshd
```

![Fail2Ban Status Baseline](/assets/img/posts/project2%20hardened%20linux/20.png){: width="700" .no-lazy}
_Fail2Ban SSH jail status before a ban event_

Repeated failed connection attempts triggered the jail and banned the Windows lab host IP.

![Blocked SSH Attempt](/assets/img/posts/project2%20hardened%20linux/21.png){: width="700" .no-lazy}
_SSH connection attempt timing out after protection controls were triggered_

![Fail2Ban Ban Verification](/assets/img/posts/project2%20hardened%20linux/22.png){: width="700" .no-lazy}
_Fail2Ban recording `192.168.10.10` in the banned IP list_

### 6. CIS Benchmark Hardening

System-level hardening was applied using CIS Ubuntu Server principles. The goal was not just to install services, but to reduce the operating system's attack surface and enforce safer defaults.

#### 6.1 Package Cleanup

Unnecessary and legacy network tools were removed.

```bash
sudo apt purge -y telnet rsh-client talk inetutils-telnetd xinetd
sudo apt autoremove -y
sudo apt autoclean
```

#### 6.2 Kernel Hardening

Kernel parameters were applied through `/etc/sysctl.d/99-hardening.conf`.

```text
net.ipv4.ip_forward = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.log_martians = 1
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.sysrq = 0
kernel.yama.ptrace_scope = 1
```

```bash
sudo sysctl -p /etc/sysctl.d/99-hardening.conf
```

#### 6.3 Password Policy & File Permissions

Password quality enforcement and critical file permissions were applied.

```bash
sudo apt install libpam-pwquality -y
sudo nano /etc/security/pwquality.conf
```

```text
minlen = 14
ucredit = -1
lcredit = -1
dcredit = -1
ocredit = -1
difok = 8
```

```bash
sudo chmod 640 /etc/shadow
sudo chmod 644 /etc/passwd
sudo chmod 700 /etc/cron.d /etc/cron.daily /etc/cron.hourly /etc/cron.weekly /etc/cron.monthly
```

![CIS Kernel and Permission Validation](/assets/img/posts/project2%20hardened%20linux/23.png){: width="700" .no-lazy}
_Validation of `ip_forward`, SYN cookies, and `/etc/shadow` permissions_

#### 6.4 Automatic Security Updates

Automatic security updates were enabled through `unattended-upgrades`.

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

**Additional CIS controls applied:**

- Removed unnecessary packages such as Telnet and legacy remote shell tooling
- Disabled unused services where applicable
- Configured PAM password quality requirements
- Applied critical file permission hardening
- Configured a login warning banner
- Enabled automatic security updates

### 7. Backup Automation Script

A production-style backup workflow was created to protect service configuration, web content, and logs. The backup script compresses important paths, timestamps the archive, writes operational logs, and removes old backups after the retention window.

**Backup directories:**

```bash
sudo mkdir -p /backups/daily
sudo mkdir -p /backups/logs
sudo chmod 700 /backups /backups/daily /backups/logs
```

![Backup Directory Creation](/assets/img/posts/project2%20hardened%20linux/24.png){: width="700" .no-lazy}
_Backup directories created with restricted permissions_

**Backup script:**

```bash
#!/bin/bash
BACKUP_DIR="/backups/daily"
LOG_FILE="/backups/logs/backup.log"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
HOSTNAME=$(hostname)
ARCHIVE_NAME="$HOSTNAME-backup-$DATE.tar.gz"
RETENTION_DAYS=7

SOURCES=("/etc" "/var/www/html" "/var/log")

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting backup: $ARCHIVE_NAME"
tar -czf "$BACKUP_DIR/$ARCHIVE_NAME" "${SOURCES[@]}" 2>/dev/null

if [ $? -eq 0 ]; then
  SIZE=$(du -sh "$BACKUP_DIR/$ARCHIVE_NAME" | cut -f1)
  log "Backup successful: $ARCHIVE_NAME ($SIZE)"
else
  log "ERROR: Backup failed"
  exit 1
fi

find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
log "Retention cleanup complete"
```

```bash
sudo nano /usr/local/bin/backup.sh
sudo chmod 700 /usr/local/bin/backup.sh
sudo /usr/local/bin/backup.sh
```

![Backup Script](/assets/img/posts/project2%20hardened%20linux/25.png){: width="700" .no-lazy}
_Backup script with archive creation, logging, and retention cleanup_

![Backup Execution](/assets/img/posts/project2%20hardened%20linux/26.png){: width="700" .no-lazy}
_Successful backup execution and cleanup log output_

### 8. Restore Automation Script

A restore script was created so recovery could be executed consistently under pressure. The script validates that an archive name was provided, checks that it exists, restores it to `/`, and logs the result.

**Restore script:**

```bash
#!/bin/bash
LOG_FILE="/backups/logs/restore.log"
BACKUP_DIR="/backups/daily"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

if [ -z "$1" ]; then
  echo "Usage: sudo $0 <backup-filename.tar.gz>"
  echo "Available backups:"
  ls -lh "$BACKUP_DIR"
  exit 1
fi

ARCHIVE="$BACKUP_DIR/$1"

if [ ! -f "$ARCHIVE" ]; then
  log "ERROR: Archive not found: $ARCHIVE"
  exit 1
fi

log "Starting restore from: $1"
tar -xzf "$ARCHIVE" -C /

if [ $? -eq 0 ]; then
  log "Restore successful from: $1"
else
  log "ERROR: Restore failed"
  exit 1
fi
```

```bash
sudo nano /usr/local/bin/restore.sh
sudo chmod 700 /usr/local/bin/restore.sh
```

![Restore Script](/assets/img/posts/project2%20hardened%20linux/27.png){: width="700" .no-lazy}
_Restore script with argument validation, archive checks, extraction, and logging_

### 9. Cron Scheduling

The backup job was scheduled to run every day at 2:00 AM and append cron output into a dedicated log file.

```bash
sudo crontab -e
```

```cron
0 2 * * * /usr/local/bin/backup.sh >> /backups/logs/cron.log 2>&1
```

![Cron Backup Schedule](/assets/img/posts/project2%20hardened%20linux/28.png){: width="700" .no-lazy}
_Daily 2:00 AM cron schedule for automated backups_

---

## Verification & Testing

### Test 1: Web Service Availability

Before simulating a disaster, the working state was confirmed from the Linux server. This proved the web content existed and the Nginx service was serving the expected page.

```bash
curl http://192.168.10.20
```

![Pre-Disaster Web Content](/assets/img/posts/project2%20hardened%20linux/29.png){: width="700" .no-lazy}
_Internal web page content available before disaster simulation_

### Test 2: Disaster Simulation

The disaster scenario intentionally removed the web root content and Nginx site configuration to simulate accidental deletion or destructive change.

```bash
sudo rm -rf /var/www/html/*
sudo rm -f /etc/nginx/sites-enabled/default
```

![Disaster Simulation](/assets/img/posts/project2%20hardened%20linux/30.png){: width="700" .no-lazy}
_Web content and Nginx site configuration removed to simulate service failure_

### Test 3: Backup Availability

Available backup archives were checked before running the restore process.

```bash
ls -lh /backups/daily/
```

![Available Backup Archive](/assets/img/posts/project2%20hardened%20linux/31.png){: width="700" .no-lazy}
_Backup archive present in `/backups/daily`_

### Test 4: Restore Execution

The restore script was executed against the known-good backup archive.

```bash
sudo /usr/local/bin/restore.sh ubuntuserver-backup-2026-06-19_10-12-14.tar.gz
```

![Restore Execution](/assets/img/posts/project2%20hardened%20linux/32.png){: width="700" .no-lazy}
_Restore process completed successfully from the selected archive_

### Test 5: Post-Recovery Service Validation

After restoration, the web page, Nginx configuration, firewall posture, and SSH behavior were validated again.

```bash
curl http://192.168.10.20
sudo nginx -t
sudo ufw status
```

![Recovered Web Content](/assets/img/posts/project2%20hardened%20linux/33.png){: width="700" .no-lazy}
_Recovered web content available after restore_

![Nginx Configuration Test](/assets/img/posts/project2%20hardened%20linux/34.png){: width="700" .no-lazy}
_Nginx configuration syntax validation successful_

![Firewall Validation](/assets/img/posts/project2%20hardened%20linux/35.png){: width="700" .no-lazy}
_UFW rules still active after backup and restore testing_

![SSH Access Validation](/assets/img/posts/project2%20hardened%20linux/36.png){: width="700" .no-lazy}
_SSH access behavior validated from the Windows lab host_

---

## CIS Hardening Checklist

| Control | Applied | Verified |
| --- | --- | --- |
| Unnecessary packages removed | Yes | Yes |
| Unused services disabled | Yes | Yes |
| SSH password authentication disabled | Yes | Yes |
| SSH moved to non-standard port | Yes | Yes |
| Root login disabled | Yes | Yes |
| UFW default-deny inbound policy active | Yes | Yes |
| Source-restricted firewall rules | Yes | Yes |
| Fail2Ban brute force protection | Yes | Yes |
| IP forwarding disabled | Yes | Yes |
| SYN cookies enabled | Yes | Yes |
| ICMP redirects disabled | Yes | Yes |
| Reverse path filtering enabled | Yes | Yes |
| Password minimum length set to 14 | Yes | Yes |
| Account lockout controls configured | Yes | Yes |
| Password expiry policy configured | Yes | Yes |
| `/etc/shadow` permissions set to 640 | Yes | Yes |
| Login banner configured | Yes | Yes |
| Automatic security updates enabled | Yes | Yes |

---

## Key Takeaways & Enterprise Security Impact

### Minimal Install Philosophy

Starting from a no-GUI Ubuntu Server install reduces the attack surface before any hardening is applied. Each removed package and disabled service reduces maintenance burden and removes possible entry points.

### Defense in Depth

The server does not rely on one control. SSH key authentication, a non-standard SSH port, UFW source restrictions, Fail2Ban response rules, kernel hardening, file permissions, and automatic updates all reduce exposure from different angles.

### Verified Recovery

The backup was not treated as complete until it was restored after a destructive test. Removing the web root and Nginx configuration proved that the restore script could recover both service content and configuration in a measurable recovery workflow.

### Automation Over Manual Recovery

The backup and restore processes are scripted, logged, and scheduled. This reduces human error during stressful recovery scenarios and mirrors enterprise runbook practices.

---

**Project Status**: Complete  
**Server Role**: Hardened Ubuntu Nginx web server  
**Backup Coverage**: `/etc`, `/var/www/html`, `/var/log`  
**Recovery Test**: Destructive restore test passed  
**Security Baseline**: CIS-inspired controls applied and verified
