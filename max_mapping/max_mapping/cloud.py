import os
import requests

BACKEND_URL = "https://backend.michaelmachohi.com"
USER_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
CLOUDFLARE_R2_BUCKET = "MEDIA_BUCKET"
CLOUDFLARE_R2_PUBLIC_URL = "https://files.michaelmachohi.com"

MAPS_DIR = "/home/sierra-95/Documents/agv/max_ws/src/Max/max_mapping/maps"

def get_cloud_files():
    """Fetch existing files for the user from R2"""
    resp = requests.get(f"{BACKEND_URL}/media/get", params={"user_id": USER_ID})
    resp.raise_for_status()
    data = resp.json()

    # Collect original names from Images and Others
    cloud_files = set()
    for category in ["Images", "Others"]:
        for item in data.get(category, []):
            cloud_files.add(item["original_name"])
    return cloud_files

def find_local_files():
    """Walk maps dir and collect .pgm and .yaml files"""
    local_files = []
    for folder in os.listdir(MAPS_DIR):
        folder_path = os.path.join(MAPS_DIR, folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".pgm") or file_name.endswith(".yaml"):
                    local_files.append(os.path.join(folder_path, file_name))
    return local_files

def upload_file(file_path):
    """Upload a single file to R2"""
    file_name = os.path.basename(file_path)
    category = "Images" if file_name.endswith(".pgm") else "Others"
    r2_key = f"project/{USER_ID}"

    files = {'files': open(file_path, 'rb')}
    data = {
        'user_id': USER_ID,
        'bucket': CLOUDFLARE_R2_BUCKET,
        'bucket_url': CLOUDFLARE_R2_PUBLIC_URL,
        'r2_key': r2_key
    }

    resp = requests.post(f"{BACKEND_URL}/media/upload", files=files, data=data)
    resp.raise_for_status()
    print(f"Uploaded {file_name} to {category}")

def sync_maps():
    cloud_files = get_cloud_files()
    local_files = find_local_files()

    for file_path in local_files:
        file_name = os.path.basename(file_path)
        if file_name not in cloud_files:
            upload_file(file_path)

if __name__ == "__main__":
    sync_maps()
