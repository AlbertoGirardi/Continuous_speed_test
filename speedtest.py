import json
import subprocess
import os
import schedule 

def run_speedtest():
    # Run the speedtest-cli command and get the JSON output
    result = subprocess.run(['speedtest-cli', '--secure', '--json'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def extract_values(data):
    # Extract the required values
    ping = data['ping']
    download = data['download'] / 1_000_000  # Convert from bps to Mbps
    upload = data['upload'] / 1_000_000      # Convert from bps to Mbps
    return ping, download, upload

def save_to_file(filename, ping, download, upload):
    # Save the values to a file
    pass

def main():

    os.makedirs(data_folder_name, exist_ok=True)

    while 1:

        print("in esecuzione")
        data = run_speedtest()
        print("finito")

        ping, download, upload = extract_values(data)
        print(ping, download, upload)
        # save_to_file('speedtest_results.txt', ping, download, upload)

data_file = ""
data_folder_name = "data"

if __name__ == "__main__":
    main()
