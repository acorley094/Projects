#! /usr/bin/python3
AUTHOR = 'acorley094'
PROJECT = 'DNS Enumeration Tool'

# Import necessary libraries
from datetime import datetime
from dns import resolver
import argparse

def main():
    # Configure command line argument parser
    parser = argparse.ArgumentParser(description=f"{PROJECT} written by {AUTHOR}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('domain', help='domain to enumerate')
    parser.add_argument('-o' ,'--output', default='default', help='name of the output file')
    args = parser.parse_args()
    config = vars(args)

    # Get user values from config
    domain = config.get('domain')
    timestamp = datetime.now().strftime("%m-%d-%y_%H%M%S")
    # Configure default output file name
    if config.get('output') == parser.get_default('output'):
        outfile = f"./Enumerations/dns_enum_{config.get('domain')}_{timestamp}.txt"
    else:
        outfile = f"./Enumerations/{config.get('output')}.txt"
    recordTypes = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'HINFO', 'LOC', 'RP', 'TXT']

    # Open the output file in append mode
    with open(outfile, 'a') as f:
        f.write(f'Domain: {domain}\n')

    # Execute the DNS enumeration function
    dnsEnum(domain, outfile, recordTypes)

    print("DNS enumeration completed successfully.")

# Define the DNS enumeration function
def dnsEnum(domain, outfile, recordTypes):
    print(f'Domain: {domain}')

    # Loop through each DNS record type
    for records in recordTypes:
        try:
            # Try to resolve the DNS records for the given domain
            answer = resolver.resolve(domain, records)
            print('\n',records, ':', sep='', end ='')
            
            # Loop through each server in the answer and print/write the information
            with open(outfile, 'a') as f:
                f.write(f'\n{records}: \n')
                for server in answer:
                    print(server.to_text(), end='\n')
                    f.write(server.to_text() + '\n')

        except resolver.NoAnswer:
            # Handle case when there is no answer for the DNS record type
            print(records, ':', sep='', end='')
            pass
        except resolver.NXDOMAIN:
            # Handle case when the domain does not exist
            print(f'{domain} does not exist.')
        except KeyboardInterrupt:
            # Handle case when the user interrupts the program
            print('Quitting...')
            quit()

if __name__ == "__main__":
    main()
