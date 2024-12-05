import subprocess
from prettytable import PrettyTable as PT

# Define target and ports
targets = ["192.168.0.1", "192.168.0.3", "192.168.0.6"]
ports = "22,80,443,443,515,631,3689,7000,7100,62078"

# Initialize the PrettyTable
table = PT()
table.field_names = ["IP Address", "Port", "State", "Service", "Version/OS"]

# Loop through each target
for target in targets:
    # Run the Nmap command
    nmap_command = f"nmap -sV -p {ports} {target}"
    result = subprocess.run(nmap_command, shell=True, capture_output=True, text=True)

# Parse the output
    for line in result.stdout.splitlines():
#    print(f"Checking line: {line}")
        if "open" in line:
        #print(f"Parsing line: {line}")
            parts = line.split()
            port = parts[0]
            state = parts[1]
            service = parts[2]
            version = " ".join(parts[3:]) if len(parts) > 3 else "N/A"
            table.add_row([target, port, state, service, version])

# Print the table
#print(table)

# Save the table to a text file
with open("pvscan_results.txt", "w") as file:
    file.write(str(table))

