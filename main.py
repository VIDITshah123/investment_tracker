import sys
import os
import argparse
import subprocess
from pathlib import Path

def main():
    root = str(Path(__file__).resolve().parent)
    if root not in sys.path:
        sys.path.insert(0, root)

    parser = argparse.ArgumentParser(description="PB Equity Intelligence Platform (PBEIP)")
    parser.add_argument("--scheduler", action="store_true", help="Run background scheduler")
    args = parser.parse_args()

    if args.scheduler:
        print("Starting PBEIP Scheduler...")
        from modules.automation.scheduler import start_scheduler
        start_scheduler()
    else:
        print("Launching PB Equity Intelligence Terminal Dashboard...")
        env = os.environ.copy()
        env["PYTHONPATH"] = root + os.pathsep + env.get("PYTHONPATH", "")
        
        # Use active python executable to run streamlit module with PYTHONPATH set
        subprocess.run([sys.executable, "-m", "streamlit", "run", "modules/dashboard/app.py"], env=env)

if __name__ == "__main__":
    main()
