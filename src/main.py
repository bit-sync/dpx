import sys
import json
import os

def install_pkg(path_to_zip):
    # Check if the script is running with root privileges
    if os.geteuid() != 0:
        print("Error: This script must be run as root (use sudo).")
        sys.exit(1)

    # Ensure the extraction directory exists
    if not os.path.exists('/var/cache/dpkg/archives'):
        os.makedirs('/var/cache/dpkg/archives')

    # Unzip the file to the specified directory
    os.system(f'unzip {path_to_zip} -d /var/cache/dpkg/archives/')

    # TEMP: Debug path for testing
    path_to_info = "/var/cache/dpkg/archives/blah.dpx/info.json"
    # End temp

    # Try to load the JSON configuration file
    try:
        with open(path_to_info, 'r', encoding='utf-8') as file:
            info = json.load(file)
    except UnicodeDecodeError:
        print(f"Failed to decode JSON from {path_to_info}. It might not be UTF-8 encoded.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: JSON file {path_to_info} not found.")
        sys.exit(1)

    # Execute each command in "steps"
    for step in info.get('steps', []):
        if step.get("type") == "command":
            print(f"Executing: {step['value']}")
            os.system(step["value"])

    # Check if "deb" key exists and has items
    if 'deb' in info and info['deb']:
        # Install packages specified in "deb"
        for item in info['deb']:
            if "name" in item:
                print(f"Installing package by name: {item['name']}")
                os.system(f"apt-get install -y {item['name']}")
            elif "path" in item:
                deb_file_path = os.path.join('/var/cache/dpkg/archives', item['path'])
                print(f"Installing package by path: {deb_file_path}")
                os.system(f"dpkg -i {deb_file_path}")
                # Use `apt-get` to fix any dependency issues after installing with `dpkg`
                os.system("apt-get install -f -y")
    else:
        print("No .deb files to install. Skipping package installation.")

argv = sys.argv

if len(argv) > 2 and argv[1] == "install":
    install_pkg(argv[2])
else:
    print("Usage: script.py install <path_to_dpx>")
