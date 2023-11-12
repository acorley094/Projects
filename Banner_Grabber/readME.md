# Project Description: Banner Grabbing Tool

## Overview

The Banner Grabbing Tool is a Python script designed to gather information about a target system by connecting to specified IP addresses and retrieving banners from open ports. Banners often contain valuable information about the services running on those ports, aiding in the identification of potential security vulnerabilities.

## Key Features

1. **Flexible Port Specification:**
   - Users can specify a single port, a comma-separated list of ports, or a range of ports to scan.

2. **Real-time Connection Attempts:**
   - The tool iterates over the specified ports, attempting to establish a TCP connection and fetch banners from the target system.

3. **Informative Output:**
   - The script provides detailed output, indicating successful connections and displaying the retrieved banners.

4. **Graceful Handling of Connection Refusals:**
   - In case of a connection refusal, the tool gracefully handles the error and notifies the user, allowing for efficient troubleshooting.

5. **User-friendly Command-line Interface:**
   - Utilizes argparse for a straightforward command-line interface, enabling users to easily input target IP addresses and port specifications.

## Usage

### Command-line Syntax:

```bash
python banner_grabber.py <IP_ADDRESS> -p <PORT(S)>
```

### Example:

```bash
python banner_grabber.py 127.0.0.1 -p 80,443
```

## How It Works

1. The user provides the target IP address and the port(s) to be scanned as command-line arguments.

2. The script creates a socket and attempts to connect to the specified IP address and port(s).

3. For each port, the tool captures the banner information from the server's response.

4. The tool prints the connection status and the retrieved banner information to the console.

5. The process continues until all specified ports have been scanned or until the user interrupts the script.

## Dependencies

- Python 3.x
- argparse module

## Contribution

Contributions are welcome! Feel free to fork the repository, make enhancements, and create pull requests. Please follow the contribution guidelines outlined in the repository.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for more details.

Thank you for using the Banner Grabbing Tool! Stay informed and secure.
