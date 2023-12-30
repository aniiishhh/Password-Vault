import subprocess
import os
import sys


def run_config():
    config_script = os.path.join("src", "config.py")
    subprocess.run([sys.executable, config_script], check=True)


def run_main():
    main_script = os.path.join("src", "FINALMasterMenu2.py")
    subprocess.run([sys.executable, main_script], check=True)


if __name__ == "__main__":
    run_config()
    run_main()
