# Project Description: Subdomain Enumeration Tool

## Overview

The Subdomain Enumeration Tool is a Python script designed for efficiently enumerating subdomains of a specified domain. It leverages a wordlist of potential subdomains and utilizes concurrent execution with ThreadPoolExecutor to speed up the enumeration process. This tool is valuable for reconnaissance, security assessments, and discovering potential attack surfaces.

## Key Features

1. **Concurrent Subdomain Resolution:**
   - Utilizes Python's ThreadPoolExecutor to perform concurrent resolution of subdomains, enhancing the speed of the enumeration process.

2. **Dynamic Output File Naming:**
   - Allows users to specify the output file and generates a timestamped file name to avoid overwriting previous results.

3. **User-friendly Command-line Interface:**
   - Utilizes argparse for an easy-to-use command-line interface, allowing users to input the target domain, wordlist, output file, and the number of threads to use.

4. **Informative Console Output:**
   - Provides real-time console output indicating the discovered subdomains during the enumeration process.

## Usage

### Command-line Syntax:

```bash
python subdomain_enum.py <DOMAIN> -o <OUTPUT_FILE> -w <WORDLIST_FILE> -t <THREADS>
```

### Example:

```bash
python subdomain_enum.py example.com -o results.txt -w subdomains.txt -t 8
```

## How It Works

1. The user provides the target domain, wordlist file, output file, and the number of threads as command-line arguments.

2. The script uses a ThreadPoolExecutor to concurrently resolve subdomains by submitting resolution tasks to the thread pool.

3. Each subdomain resolution task attempts to query DNS records for the specified subdomain and domain.

4. Discovered subdomains are printed to the console in real-time and appended to the output file.

5. The enumeration process continues until all subdomains from the wordlist are resolved or until the user interrupts the script.

## Dependencies

- Python 3.x
- `dns` library (for DNS resolution)

## Contribution

Contributions are welcome! Feel free to fork the repository, make enhancements, and create pull requests. Please follow the contribution guidelines outlined in the repository.

**Note:** Wordlists used in this tool are sourced from the [SecLists GitHub repository](https://github.com/danielmiessler/SecLists) for comprehensive and up-to-date subdomain possibilities.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for more details.

Thank you for using the Subdomain Enumeration Tool! Discover and analyze potential subdomains efficiently.
