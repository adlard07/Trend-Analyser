import requests

response = requests.post("http://127.0.0.1:8000/load-csv", json={"file_path": "backend/data/NVIDIA.csv"})
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Failed to load data:", response.text)
