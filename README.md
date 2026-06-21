## Virtual Security Homelab & Documentation

This repository contains the configuration, scripts, and documentation for an isolated enterprise-grade virtual homelab. The environment is used to simulate production infrastructure for security engineering, privilege delegation, and defensive operations.

Live Documentation Portfolio: https://charleskhervie.github.io/Security-Homelab

---

## Tech Stack & Architecture

The portfolio is built using the Jekyll Chirpy theme and deployed via GitHub Actions.

* **Operating Systems:** Windows Server 2022 Standard, Windows 10 Enterprise, Ubuntu Server 22.04 LTS, Kali Linux
* **Identity Management:** Active Directory Domain Services (AD DS), DNS, Group Policy (GPOs)
* **Linux Administration:** Nginx, UFW, Fail2Ban, OpenSSH (key-based hardening)
* **Automation:** PowerShell, CMD scripting, Bash scripting, Cron
* **Networking:** Isolated Host-Only segment (192.168.10.0/24) via VMware Workstation Pro

---

## Active Project Modules

### Project 1: Enterprise Active Directory Architecture & Deployment

Link: https://charleskhervie.github.io/Security-Homelab/posts/active-directory-deployment/

* **Forest Baseline:** Established the `lab.charles.com` forest using static IPv4 configurations and local loopback DNS.
* **PowerShell Automation:** Scripted the programmatic deployment of the entire corporate hierarchy, including OUs, departmental security groups, and bulk user provisioning from a mock database.
* **Access Control:** Applied Principle of Least Privilege (PoLP), disabled nested privileges, and enforced initial password resets (`-ChangePasswordAtLogon $true`).
* **Validation:** Verified directory health and records using command-line diagnostic utilities (`dcdiag`, `nslookup`).

### Project 2: Hardened Linux Server, Backup Automation & Disaster Recovery

Link: https://charleskhervie.github.io/Security-Homelab/posts/hardened-linux-server-backup-disaster-recovery/

* **Service Deployment:** Provisioned a minimal Ubuntu Server 22.04 instance integrated into the existing AD subnet, running Nginx as a simulated corporate web service.
* **SSH Hardening:** Enforced key-based authentication, disabled root login and password auth, moved SSH to a non-standard port, and deployed Fail2Ban for automated brute-force mitigation.
* **CIS Benchmark Controls:** Applied kernel-level network hardening via `sysctl`, enforced PAM password complexity policies, locked down critical file permissions, and configured a legal warning banner.
* **Backup & Disaster Recovery:** Built and scheduled an automated Bash backup solution with 7-day retention, then executed a full simulated disaster (data/config deletion) and verified recovery using a custom restore script.

---

## Future Implementations

* **Centralized Logging:** Deploying Wazuh SIEM to aggregate telemetry from both Windows and Linux endpoints.
* **Vulnerability Management:** Authenticated scanning via Nessus Essentials across the domain environment.
* **Offensive Validation:** Simulated attack chains using Kali Linux to test and tune detection coverage.
* **Network Security:** Implementing explicit ACLs and traffic monitoring via packet analysis.

---

## Disclaimer

This environment is constructed strictly for educational and defensive security research purposes inside an isolated sandbox network.
