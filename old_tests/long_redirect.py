import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

count_redirect = len(response.history)
last_url = response.url

print(f"Number of redirects: {count_redirect}")
print(f"Final url: {last_url}")
