import subprocess
import threading

from api import app

def run_prep():
    subprocess.run(['python', 'app/prep.py'])

def run_api():
    print("Running API (api.py)...")
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)

def main():
    # Step 1: Run data preparation
    run_prep()

    # Step 2: Run API in a separate thread
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

if __name__ == '__main__':
    main()