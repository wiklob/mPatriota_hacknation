
import requests

url = "https://www.gov.pl/web/premier/wykaz-prac-legislacyjnych"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)}")
    print(f"Content Preview: {response.content[:200]}")
except Exception as e:
    print(f"Error: {e}")
