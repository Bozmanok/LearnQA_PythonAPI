import requests
import time

response_run = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
token = response_run.json()["token"]
time_ = response_run.json()["seconds"]
token_params = {"token": token}

response_start = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token_params)
assert response_start.json()["status"] == "Job is NOT ready"

time.sleep(time_)

response_finish = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token_params)
assert response_finish.json()["result"] is not None
assert response_finish.json()["status"] == "Job is ready"
