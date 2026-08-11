import argparse
import requests
import json
import os
import subprocess

my_dir = os.path.dirname(os.path.abspath(__file__))

def write_files(base = my_dir, datas = []):
    for data in datas:
        path = os.path.join(base, data['path'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(data['content'])

def remove_files(base = my_dir, datas = []):
    for data in datas:
        path = os.path.join(base, data)
        if os.path.exists(path):
            os.remove(path)


def download_files(base = my_dir, datas = []):
    for data in datas:
        path = os.path.join(base, data['path'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            try:
                data_content = requests.get(data['url']).content
                f.write(data_content)
            except Exception as e:
                print(f"Failed to download {data['url']}")
                print(f"error: {e}")


def main():
    parser = argparse.ArgumentParser(description='Download and process files from a given URL.')
    parser.add_argument('--json',"-j", type=str, required=True, help='Path to the JSON file containing the data.')
    parser.add_argument('--base',"-b", type=str, default=my_dir, help='Base directory to save the files.')
    args = parser.parse_args()

    with open(args.json, 'r') as f:
        data = json.load(f)

    write_files(base = args.base, datas = data["commit"]["addFiles"])
    remove_files(base = my_dir, datas = data["commit"]["removeFiles"])
    download_files(base = my_dir, datas = data["commit"]["downloads"])

    os.chdir(args.base)
    cmd = ["git", "add", "."]
    subprocess.run(cmd)
    cmd = ["git", "commit", "-m", f"\"{data["Author"]}: {data['description']}\""]
    subprocess.run(cmd)
    


if __name__ == "__main__":
    main()