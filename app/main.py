import subprocess
import webbrowser
import time
import threading

def run_prep():
    print("Running data preparation (prep.py)...")
    subprocess.run(['python', 'app/prep.py'])

def run_api():
    print("Running API (api.py)...")
    subprocess.run(['python', 'app/api.py'])

def open_browser():
    time.sleep(2)
    print("Opening the API in your default browser...")
    webbrowser.open("http://127.0.0.1:5000")

def main():
    # Step 1: Run data preparation
    run_prep()

    # Step 2: Ask user if they want to run the API
    user_input = input("Do you want to run the API now? (y/n): ").strip().lower()

    if user_input == 'y':
        api_thread = threading.Thread(target=run_api)
        api_thread.start()

        # Open the API in the browser
        open_browser()
    else:
        print("Skipping API. You can run it later.")

if __name__ == '__main__':
    main()