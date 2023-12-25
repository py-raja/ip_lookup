import requests
from ipaddress import ip_address
from datetime import datetime
# Functions for fetching IP details and AS details
def format_date(date_string):
    if date_string:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y, at %H:%M:%S UTC")
    return "N/A"
    
def get_ip_details(ip_address):
    url = f"https://rdap.apnic.net/ip/{ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch IP address data. Status code: {response.status_code}")
        return None

def get_as_details(as_number):
    url = f"https://rdap.apnic.net/autnum/{as_number}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch AS number data. Status code: {response.status_code}")
        return None

# Function to display IP details
def display_ip_details(ip_details):
    if ip_details:
        print("IP Address Range Details:")
        print(f"IP Version: {ip_details['ipVersion']}")
        print(f"Type: {ip_details['type']}")
        print(f"Start Address: {ip_details['startAddress']}")
        print(f"End Address: {ip_details['endAddress']}")
        print(f"Status: {', '.join(ip_details['status'])}")
        print(f"Country: {ip_details['country']} ({ip_details.get('countryName', 'Unknown')})")
        print(f"Name: {ip_details.get('name', 'N/A')}")
        print("Events:")
        for event in ip_details.get('events', []):
            print(f"{event['eventAction'].title()}: {format_date(event['eventDate'])}")
        print("Remarks:")
        for remark in ip_details.get('remarks', []):
            print(f"Description:")
            for desc in remark.get('description', []):
                print(desc)
        print("Entities:")
        for entity in ip_details.get('entities', []):
            print(f"{entity['handle']} ({', '.join(entity['roles'])} Role):")
            print(f"Roles: {', '.join(entity['roles'])}")
            print("Events:")
            for event in entity.get('events', []):
                print(f"{event['eventAction'].title()}: {format_date(event['eventDate'])}")
            if 'remarks' in entity:
                print("Remarks:")
                for remark in entity['remarks']:
                    for desc in remark['description']:
                        print(desc)
            print(f"Handle: {entity['handle']}")
            print(f"Links: {entity['links'][0]['href']}")
        print("Notices:")
        for notice in ip_details.get('notices', []):
            print(f"{notice['title']}:")
            for desc in notice.get('description', []):
                print(desc)
            if 'links' in notice:
                for link in notice['links']:
                    print(f"{link['rel'].title().replace('-', ' ')}: {link['href']}")
        print("Links:")
        for link in ip_details.get('links', []):
            print(f"{link['rel'].title().replace('-', ' ')}: {link['href']}")
            
# Function to display AS details
def display_as_details(as_details):
    print("IP Address Range Details:")
    print(f"Start Autnum: {as_details['startAutnum']}")
    print(f"End Autnum: {as_details['endAutnum']}")
    print(f"Status: {', '.join(as_details['status'])}")
    print(f"Country: {as_details['country']} ({as_details.get('countryName', 'Unknown')})")
    print(f"Name: {as_details.get('name', 'N/A')}")
    print("Events:")
    for event in as_details.get('events', []):
        print(f"{event['eventAction'].title()}: {format_date(event['eventDate'])}")
    print("Remarks:")
    for remark in as_details.get('remarks', []):
        print(f"Description:")
        for desc in remark.get('description', []):
            print(desc)
    print("Entities:")
    for entity in as_details.get('entities', []):
        print(f"{entity['handle']} ({', '.join(entity['roles'])} Role):")
        print(f"Roles: {', '.join(entity['roles'])}")
        print("Events:")
        for event in entity.get('events', []):
            print(f"{event['eventAction'].title()}: {format_date(event['eventDate'])}")
        if 'remarks' in entity:
            print("Remarks:")
            for remark in entity['remarks']:
                for desc in remark['description']:
                    print(desc)
        print(f"Handle: {entity['handle']}")
        print(f"Links: {entity['links'][0]['href']}")
    print("Notices:")
    for notice in as_details.get('notices', []):
        print(f"{notice['title']}:")
        for desc in notice.get('description', []):
            print(desc)
        if 'links' in notice:
            for link in notice['links']:
                print(f"{link['rel'].title().replace('-', ' ')}: {link['href']}")
    print("Links:")
    for link in as_details.get('links', []):
        print(f"{link['rel'].title().replace('-', ' ')}: {link['href']}")
        
# Main function

def main():
    user_input = input("Enter an IP address or an Autonomous System (AS) number: ")

    try:
        # Validate if the input is an IP address
        ip = ip_address(user_input)
        ip_details = get_ip_details(user_input)

        if ip_details:
            # If it's an IP address, display IP details
            display_ip_details(ip_details)
    except ValueError:
        # If input is not an IP address, assume it's an AS number
        as_details = get_as_details(user_input)

        if as_details:
            # If it's an AS number, display AS details
            display_as_details(as_details)

if __name__ == "__main__":
    main()