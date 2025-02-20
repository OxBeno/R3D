#!/usr/bin/env python3


import requests
import argparse

def logo():
    logo = """

_______      _______         _____
|      |            |       |     \\
|      |            |       |      \\
|  ____|     _______|       |       |
|  \                |       |       |
|   \               |       |      /
|    \       _______|       |_____/


"""
    return logo

print(logo())

def ensure_scheme(domain):
    """
    Ensures the domain has a valid scheme (http:// or https://).
    If no scheme is present, defaults to https://.
    """
    if not domain.startswith(('http://', 'https://')):
        domain = f"https://{domain}"
    return domain

def send_requests(domains):
    results = {}
    for domain in domains:
        try:
            # Ensure the domain has a valid scheme
            domain = ensure_scheme(domain)
            
            # Send a GET request to the domain
            response = requests.get(domain, timeout=5)
            status_code = response.status_code
            results[domain] = status_code
            print(f"Domain: {domain} | Status Code: {status_code}")
        except requests.exceptions.RequestException as e:
            # Handle exceptions (e.g., connection errors, timeouts)
            results[domain] = str(e)
            print(f"Domain: {domain} | Error: {e}")
    return results

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]
    return domains

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Send HTTP requests to multiple domains and retrieve status codes.")
    parser.add_argument("-f", "--file", required=True, help="Path to the file containing domains (one per line).")
    parser.add_argument("-o", "--output", help="Path to the output file to save results.")
    args = parser.parse_args()

    # Read domains from the file
    domains = read_domains_from_file(args.file)
    
    # Send requests and get status codes
    results = send_requests(domains)
    
    # Save results to the output file if specified
    if args.output:
        with open(args.output, "w") as output_file:
            for domain, status in results.items():
                output_file.write(f"{domain}: {status}\n")
        print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
