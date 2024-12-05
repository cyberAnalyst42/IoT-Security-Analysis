#!/bin/bash

clear
SUBNET="192.168.0.0/24"
#echo "\e[44mStarting network scan on $SUBNET...\n\e[0m"

nmap -sP $SUBNET -oN network_scan_results.txt > /dev/null

#echo  "\e[41mDevice Name\t\tIP Address\t\tStatus\t\tLatency\t\tOpen Ports\e[0m" > netscan_result.txt
#echo  "\n-----------------------------------------------------------------------------------------------\n" >> netscan_result.txt

echo  "Device Name            IP Address              Status            Latency          " > netscan_result.txt
echo  "--------------------------------------------------------------------------" >> netscan_result.txt

awk '
	/Nmap scan report for/ {
		device = $0
	
		if (match($0, /\(([0-9.]+)\)/, arr)) {
			ip = arr[1]
		} else {
			ip = $NF
		}
		
		sub(/Nmap scan report for /, "", device)

		split(device, device_parts, ".")
			device = device_parts[1]
	
		}
	
	/Host is up/ { status = "Up"
		}

	/latency/ { 
		gsub(/[()]/, "", $(NF-1))
		latency = $(NF-1)

		open_ports = port_scan_results[ip]
		
		printf ("%-22s %-25s %-15s %-10s\n", device, ip, status, latency)
	 } ' network_scan_results.txt >> netscan_result.txt
