---
title: "Project 0: Building a Blue Team Homelab - Introduction"
date: 2026-06-01
categories: [Homelab, Setup]
tags: [Virtualization, VMware, Network, Architecture]

---

For quite some time, I have wanted to build my own dedicated homelab for defensive security and Blue Team operations.I was heavily relying on guided online training platforms. While those environments are amazing, you download a configuration file, jump on their VPN, and follow a pre-determined track. You are mostly forced to look at exactly what they built for you, rather than having the freedom to perform open-ended testing, customization, and independent research. 

Now, I am finally building my own virtual sandbox network. This project series is meant to document that exact setup for anyone tracking down this path who wants a reliable baseline to practice specific methodologies, security engineering tools, and blue team defense. 

## Why a Virtual Workstation?

Let me explain the reasoning behind this setup. Over the last few years, I have read countless hardware recommendation threads, server subreddits, and tutorial videos where everyone says things like, "Hey, just buy some old enterprise rack servers or used switches on eBay for $200 and you are set." 

Realistically, the secondhand market is completely different depending on your location. Locally, finding outdated enterprise routers or switches usually means dealing with inflated markups for gear that is ancient, incredibly loud, and draws massive amounts of power. Buying a legacy multi-processor server is even worse—they are expensive, spare parts are a pain to track down, and you take a massive gamble on component degradation. 

Instead of dealing with the overhead, noise, and cost of physical server racks, it made significantly more sense to put that capital directly into upgrading my primary workstation laptop. It is completely portable, reliable, and more than capable of handling concurrent virtual infrastructure. That is why I am building this lab 100% virtual inside my host machine. 

## Hardware Specifications

Defensive labs—especially if you plan to aggregate system events or integrate security information and event management (SIEM) consoles later—are resource-heavy. While you won't need to run every single target endpoint simultaneously during early build phases, you still need a solid processing baseline to prevent the host hypervisor from freezing up. 

I am currently running this entire setup on an **Acer Nitro V15** with the following technical specifications:

* **CPU:** Intel Core i5-13420H
* **RAM:** 32GB DDR5 5600MHz 
* **OS Storage:** 512GB NVMe M.2 SSD 
* **Lab/VM Storage:** 2TB NVMe M.2 SSD (Dedicated Expansion)

When picking out a laptop for virtualization engineering, the most critical factor is the processor layout, since CPUs cannot be upgraded later on. 

## Tool Stack

These are the primary platform tools utilized across this infrastructure series:

1. **VMware Workstation Pro** – Deployed as the core Type-2 hypervisor engine to configure host virtual networks, manage isolated host-only subnets, and handle configuration snapshots before breaking configurations.
2. **Draw.io** – An open-source diagramming utility used to explicitly map out network configurations, segment localized VLAN targets, and trace traffic routing topology layers.
3. **Joplin / Markdown Notes** – A markdown-based system directory mapping documentation log. Keeping precise logs of active static IP ranges, asset configuration variables, and credentials is essential to prevent losing track of machine variables.

