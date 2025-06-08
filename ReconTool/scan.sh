#!/bin/bash

# Load configuration
config_file="config.txt"
if [ -f "$config_file" ]; then
    source "$config_file"
else
    echo "Error: Configuration file '$config_file' not found."
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

domain=$1

# Create a directory with the domain name for storing scan results
output_dir="$domain" 
if [ ! -d "$output_dir" ]; then
    mkdir "$output_dir" || { echo "Error creating output directory"; exit 1; }
else
    echo "Output directory '$output_dir' already exists. Proceeding..."
fi

output_folder="$(date +%Y%m%d_%H%M)"
if [ ! -d "$output_dir/$output_folder" ]; then
    mkdir "$output_dir/$output_folder" || { echo "Error creating output directory"; exit 1; }
else
    echo "Output folder '$output_dir/$ouput_folder' already exists. Proceeding..."
fi

# Function to run a scan in the background and print a message when finished
run_scan() {
    tool=$1
    
    output_file="$output_dir/$output_folder/$tool.txt"
    case $tool in
        "wpscan")
            sudo wpscan --force -v -e --rua --url "https://$domain" --output "$output_file" --ignore-main-redirect --api-token "$WPSCAN_API_KEY" & 
            ;;
        "whatweb")
            whatweb -v -a 3 "https://$domain" > "$output_file" &
            ;;
        "nmap")
            sudo nmap -sT -sV -A -O "$domain" -oN "$output_file" &
            ;;
        "dig")
            dig "$domain" > "$output_file" &
            ;;
        "whois")
            whois "$domain" > "$output_file" &
            ;;
	"dnsenum")
            dnsenum "$domain" > "$output_file" &
            ;;
        "nikto")
       	    nikto -h "$domain" > "$output_file" &
       	    ;;
       	 
    esac

    # Get the PID of the last background process
    last_pid=$!
    echo "Scan with $tool is running in the background (PID: $last_pid)."

    # Wait for the background process to finish
    wait $last_pid

    echo "Scan with $tool is finished."
}

# Run scans in the background
echo "Running scans in the background..."



run_scan "whois"
run_scan "dig"
run_scan "whatweb"
run_scan "nmap"
run_scan "dnsenum"
run_scan "wpscan"
run_scan "nikto"

echo "All scans are finished. Scan results saved in $output_dir"
