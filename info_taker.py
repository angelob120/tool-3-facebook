import requests
from bs4 import BeautifulSoup
import csv
import re
import datetime

def find_business_name(soup):
    # Trying to find the element with all specified classes
    business_name_tag = soup.find_all(class_=["x1heor9g", "x1qlqyl8", "x1pd3egz", "x1a2a7pz"])
    for tag in business_name_tag:
        if tag:
            return tag.get_text(strip=True)
    return ''




def find_email(soup):
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    for text in soup.stripped_strings:
        match = email_regex.search(text)
        if match:
            return match.group(0)
    return ''

def find_phone(soup):
    phone_regex = re.compile(r'\(\d{3}\)\s\d{3}-\d{4}')
    for text in soup.stripped_strings:
        match = phone_regex.search(text)
        if match:
            return match.group(0)
    return ''


def find_website(soup):
    website_regex = re.compile(r'https?://[www\.]?[a-zA-Z0-9-\.]+\.[a-z]{2,}')
    for text in soup.stripped_strings:
        match = website_regex.search(text)
        if match:
            return match.group(0)
    for link in soup.find_all('a', href=True):
        match = website_regex.search(link['href'])
        if match:
            return match.group(0)
    return ''

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        email = find_email(soup)
        phone = find_phone(soup)
        website = find_website(soup)

        return {
            'Business Name': '',  # Requires specific selectors
            'Owner\'s Name': '',  # Requires specific selectors
            'Email': email,
            'Phone': phone,
            'City': '',  # Requires specific selectors
            'Website': website,
            'Source of Info Link': url
        }
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def main():
    url = input("Enter the URL to scrape: ")
    data = scrape_website(url)
    
    if data:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'scrape_{timestamp}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        print(f"Data saved to {filename}")
    else:
        print("No data found or error in scraping.")

if __name__ == "__main__":
    main()