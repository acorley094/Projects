#! /usr/bin/python3
AUTHOR = 'acorley094'
PROJECT = 'Banner Grabbing Tool'

import socket
import argparse

def main():
    # Configure command line argument parser
    parser = argparse.ArgumentParser(description=f"{PROJECT} written by {AUTHOR}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('IPAddress', help='IP address to connect to')
    parser.add_argument('-p', '--port', help='Port(s) to scan (single port, comma-separated list, or range)', default='80')
    args = parser.parse_args()
    config = vars(args)

    ip_address = config.get('IPAddress')

    # Parse the port argument
    ports = parse_ports(config.get('port'))

    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Iterate over the specified ports and attempt to connect
        for port in ports:
            try:
                s.connect((ip_address, port))
                response = s.recv(4096)
                print(f"Connected to {ip_address}:{port}")
                print(response)
            except ConnectionRefusedError:
                print(f"Connection to {ip_address}:{port} refused...")
            except OSError as e:
                if e.errno == 113:
                    print(f"No route to host for {ip_address}:{port}")
                else:
                    raise e  # Re-raise the exception if it's not the expected "No route to host"
    
    except KeyboardInterrupt:
        print('Quitting...')
    finally:
        s.close()

def parse_ports(port_arg):
    ports = []
    # Check if the port argument is a range
    if '-' in port_arg:
        start, end = map(int, port_arg.split('-'))
        ports.extend(range(start, end + 1))
    else:
        # Otherwise, split by comma and convert to integers
        ports.extend(map(int, port_arg.split(',')))

    return ports

if __name__ == "__main__":
    main()
