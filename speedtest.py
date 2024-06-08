import json
import subprocess
import os
import schedule 
import time
import csv
from datetime import datetime

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

def save_to_file():
    # Save the values to a file
    print("in esecuzione")
    data = run_speedtest()
    print("finito")


    current_date = datetime.now().strftime("%d-%m-%Y")
    # Create the path for the new subfolder
    subfolder_path = os.path.join(data_folder_name, current_date)
    os.makedirs(subfolder_path, exist_ok=True)

    
    ping, download, upload = extract_values(data)
    print(ping, download, upload)

    current_time = datetime.now().strftime("%H:%M:%S")
    filename = os.path.join(subfolder_path, data_file_name)
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the values and current time to the CSV file
        csvwriter.writerow([current_time, ping, download, upload])




def main():
    t = 1  # minutes

    schedule.every(t).minutes.do(save_to_file)   
    os.makedirs(data_folder_name, exist_ok=True)

    while 1:
        # print('a')
        schedule.run_pending()
        time.sleep(1)
        print(datetime.now().strftime("%H:%M:%S"))


        
        

data_file_name = "data.csv"
data_folder_name = "data"

if __name__ == "__main__":
    main()
