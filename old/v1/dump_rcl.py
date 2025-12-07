
import requests

url = "https://www.gov.pl/web/premier/wykaz-prac-legislacyjnych"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    with open("rcl_dump.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Dumped to rcl_dump.html")
except Exception as e:
    print(f"Error: {e}")
