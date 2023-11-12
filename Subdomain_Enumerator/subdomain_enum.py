#! /usr/bin/python3
AUTHOR = 'acorley094'
PROJECT = 'Subdomain Enumeration Tool'

import argparse
from dns import resolver
from concurrent.futures import ThreadPoolExecutor

# Function to resolve subdomains
def resolve_subdomain(subdomain, domain, outfile):
    try:
        # Attempt to resolve the subdomain using DNS query
        ipValue = resolver.resolve(f'{subdomain}.{domain}', 'A')
        if ipValue:
            foundDomain = f'{subdomain}.{domain}'
            print(foundDomain + ' found')
            
            # Append the found subdomain to the output file
            with open(outfile, 'a') as of:
                of.write(foundDomain + '\n')
    
    # Handle various DNS resolution exceptions
    except (resolver.NoNameservers, resolver.NXDOMAIN, resolver.NoAnswer, resolver.LifetimeTimeout):
        pass

def main():
    # Configure command line argument parser
    parser = argparse.ArgumentParser(description=f"{PROJECT} written by {AUTHOR}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('domain', help='domain to enumerate')
    parser.add_argument('-o', '--output', default='./Caps/subDomainEnum.txt', help='name of the output file')
    parser.add_argument('-w', '--wordlist', default='./Wordlists/subdomains.txt', help='path to wordlist')
    parser.add_argument('-t', '--threads', default=2, type=int, help='number of threads to use.')
    args = parser.parse_args()
    config = vars(args)

    # Get user values from config
    domain = config.get('domain')
    wordlist = config.get('wordlist')
    outfile = ('./Caps/'+config.get('output'))

    # Open the wordlist file for reading
    wl = open(wordlist, 'r')

    # Use ThreadPoolExecutor for concurrent subdomain resolution
    with ThreadPoolExecutor(max_workers=int(config.get('threads'))) as executor:  # Set the maximum number of threads here
        for sd in wl:
            subD = sd.strip()
            # Submit subdomain resolution tasks to the thread pool
            executor.submit(resolve_subdomain, subD, domain, outfile)

    # Close the wordlist file
    wl.close()

if __name__ == "__main__":
    main()
