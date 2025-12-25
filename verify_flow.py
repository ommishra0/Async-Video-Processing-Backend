import requests
import time
import os

API_URL = "http://localhost:8000"

def test_flow():
    # 1. Check root
    try:
        response = requests.get(f"{API_URL}/")
        print(f"API Health Check: {response.json()}")
    except Exception as e:
        print(f"API not reachable: {e}")
        return

    # 2. Create a dummy video file if it doesn't exist (for testing)
    # Note: In a real scenario, you'd upload a real video. 
    # For verification purpose in this environment, we just need a file.
    test_video = "test_video.mp4"
    if not os.path.exists(test_video):
        with open(test_video, "wb") as f:
            f.write(b"dummy video content")

    # 3. Upload
    print(f"Uploading {test_video}...")
    with open(test_video, "rb") as f:
        files = {"file": (test_video, f, "video/mp4")}
        response = requests.post(f"{API_URL}/upload", files=files)
    
    if response.status_code != 200:
        print(f"Upload failed: {response.text}")
        return

    job_data = response.json()
    job_id = job_data["job_id"]
    print(f"Upload successful. Job ID: {job_id}")

    # 4. Poll status
    print("Polling status...")
    for _ in range(30):
        response = requests.get(f"{API_URL}/status/{job_id}")
        status_data = response.json()
        print(f"Current Status: {status_data['status']}")
        
        if status_data["status"] == "Completed":
            print("Video processing COMPLETED!")
            print(f"Output path: {status_data['output_path']}")
            return
        elif status_data["status"] == "Failed":
            print("Video processing FAILED!")
            return
        
        time.sleep(2)
    
    print("Polling timed out.")

if __name__ == "__main__":
    test_flow()
