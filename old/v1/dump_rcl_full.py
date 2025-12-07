
import requests

url = "https://www.gov.pl/web/premier/wykaz-prac-legislacyjnych"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
}

try:
    response = requests.get(url, headers=headers)
    with open("rcl_full.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Size: {len(response.text)} bytes")
except Exception as e:
    print(f"Error: {e}")
