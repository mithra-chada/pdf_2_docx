import requests
import time
import sys

def test_api():
    url = "http://localhost:8000"
    file_path = "test_layout.pdf"
    
    print(f"Uploading {file_path}...")
    with open(file_path, "rb") as f:
        response = requests.post(f"{url}/upload", files={"file": f})
    
    if response.status_code != 200:
        print(f"Upload failed: {response.text}")
        sys.exit(1)
        
    task_id = response.json()["task_id"]
    print(f"Task ID: {task_id}")
    
    while True:
        response = requests.get(f"{url}/status/{task_id}")
        status = response.json()
        print(f"Status: {status['status']}")
        
        if status['status'] == 'completed':
            break
        elif status['status'] == 'failed':
            print(f"Conversion failed: {status.get('message')}")
            sys.exit(1)
            
        time.sleep(1)
        
    print("Downloading file...")
    response = requests.get(f"{url}/download/{task_id}")
    if response.status_code == 200:
        with open("converted_test.docx", "wb") as f:
            f.write(response.content)
        print("Download successful: converted_test.docx")
    else:
        print(f"Download failed: {response.text}")

if __name__ == "__main__":
    test_api()
