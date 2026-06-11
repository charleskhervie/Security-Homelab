# $cript | Virtual Security Homelab & Documentation

This repository contains the configuration, scripts, and documentation for an isolated enterprise-grade virtual homelab. The environment is used to simulate production infrastructure for security engineering, privilege delegation, and defensive operations.

Live Documentation Portfolio: https://charleskhervie.github.io/Security-Homelab

---

## Tech Stack & Architecture

The portfolio is built using the Jekyll Chirpy theme and deployed via GitHub Actions.

* **Operating Systems:** Windows Server 2022 Standard, Windows 10 Enterprise, Kali Linux
* **Identity Management:** Active Directory Domain Services (AD DS), DNS, Group Policy (GPOs)
* **Automation:** PowerShell, CMD scripting
* **Networking:** Isolated Host-Only segment (192.168.10.0/24) via VMware Workstation / VirtualBox

---

## Active Project Modules

### Project 1: Enterprise Active Directory Architecture & Deployment
Link: https://charleskhervie.github.io/Security-Homelab/posts/active-directory-deployment/

* **Forest Baseline:** Established the `lab.charles.com` forest using static IPv4 configurations and local loopback DNS.
* **PowerShell Automation:** Scripted the programmatic deployment of the entire corporate hierarchy, including OUs, departmental security groups, and bulk user provisioning from a mock database.
* **Access Control:** Applied Principle of Least Privilege (PoLP), disabled nested privileges, and enforced initial password resets (`-ChangePasswordAtLogon $true`).
* **Validation:** Verified directory health and records using command-line diagnostic utilities (`dcdiag`, `nslookup`).

---

## Future Implementations

* **Centralized Logging:** Deploying Windows Event Forwarding (WEF) and Sysmon to aggregate telemetry.
* **Defensive Controls:** Integrating an open-source SIEM / SOC suite for detection engineering and threat hunting.
* **Network Security:** Implementing explicit ACLs and traffic monitoring via packet analysis.

---

## Disclaimer

This environment is constructed strictly for educational and defensive security research purposes inside an isolated sandbox network.
