#$! 

import os
import sys
def __get_info_template__(name):
    with open("/usr/share/dpx/templates/info.json", "r") as f:
        template = f.read()
    return template



def create_dpx(name):
    if not name:
        print("Error: Project name cannot be empty.")
        return 1

    # Create directory for DPX project
    os.makedirs(name, exist_ok=True)

    # Create info.json file
    with open(f"{name}/info.json", "w") as file:
        file.write(__get_info_template__(name))
    print(f"DPX project '{name}' created successfully.")
    print(f"Make sure to customize the info.json file in your project directory!")

def build_dpx(name):
    if not name:
        print("Error: Project name cannot be empty.")
        return

    # Ensure project directory exists
    if not os.path.exists(name):
        print(f"DPX project '{name}' does not exist.")
        return

    # Build the DPX project
    print(f"Building DPX project '{name}'...")
    try:
        os.system(f"zip -r '{name}.dpx' '{name}/'")
        print(f"DPX project '{name}' built successfully.")
    except Exception as e:
        print(f"Error during project build: {e}")

# Ensure the right number of arguments
if len(sys.argv) < 3:
    print("Usage: python script.py <command> <project_name>")
    sys.exit(1)

argv = sys.argv

command = argv[1].lower()
project_name = argv[2]

if command == "create":
    if project_name == "(null)" or not project_name:
        print("Error: Invalid project name.")
        sys.exit(1)
    create_dpx(project_name)

elif command == "build":
    if project_name == "(null)" or not project_name:
        print("Error: Invalid project name.")
        sys.exit(1)
    build_dpx(project_name)

else:
    print(f"Error: Unknown command '{command}'.")
    sys.exit(1)