#!/bin/bash
# setup_rt_kernel.sh – install and configure real‑time kernel for Ubuntu 22.04
sudo apt update
sudo apt install linux-image-rt-amd64 linux-headers-rt-amd64
# Isolate CPUs 2-3 for SDR and FPGA threads
echo "isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3" | sudo tee -a /etc/default/grub
sudo update-grub
# After reboot, set IRQ affinity
echo "2" | sudo tee /proc/irq/$(cat /proc/interrupts | grep xhci_hcd | head -1 | awk '{print $1}' | tr -d ':')/smp_affinity
# Add real‑time group limits
sudo tee /etc/security/limits.d/99-rt.conf <<EOF
@realtime - rtprio 99
@realtime - memlock unlimited
EOF
sudo usermod -a -G realtime $USER
echo "Reboot required."