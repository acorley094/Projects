# DNS Enumeration Tool

## Overview

The DNS Enumeration Tool is a Python script designed to perform DNS enumeration on a specified domain, extracting various DNS record types to gather information about the domain's infrastructure. This tool aids in understanding the domain's DNS configuration and can be valuable for security assessments and network reconnaissance.

## Key Features

1. **Dynamic Output File Naming:**
   - The script generates an output file with a timestamp to avoid overwriting previous results when using the default output file name.

2. **Flexible Record Type Enumeration:**
   - Users can specify a variety of DNS record types to enumerate, including A, AAAA, CNAME, MX, NS, PTR, SOA, SRV, HINFO, LOC, RP, and TXT.

3. **Informative Console Output:**
   - The tool provides real-time console output, displaying the enumerated DNS record types along with the corresponding server information.

4. **User-friendly Command-line Interface:**
   - Utilizes argparse for an easy-to-use command-line interface, allowing users to input the target domain and optional output file.

## Usage

### Command-line Syntax:

```bash
python dns_enum.py <DOMAIN> -o <OUTPUT_FILE>
```

### Example:

```bash
python dns_enum.py example.com -o results.txt
```

## How It Works

1. The user provides the target domain and optional output file as command-line arguments.

2. The script uses the `dns` library to resolve the specified DNS record types for the given domain.

3. For each specified DNS record type, the tool captures the server information from the DNS response.

4. The tool prints the enumerated DNS record types and corresponding server information to the console.

5. The information is also written to the output file for future reference.

6. The process continues until all specified DNS record types have been enumerated or until the user interrupts the script.

## Dependencies

- Python 3.x
- `dns` library

## Contribution

Contributions are welcome! Feel free to fork the repository, make enhancements, and create pull requests. Please follow the contribution guidelines outlined in the repository.


## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for more details.

Thank you for using the DNS Enumeration Tool! Explore and understand domain configurations securely.
