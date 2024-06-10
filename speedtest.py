import json
import subprocess
import os
import schedule 
import time
import csv
from datetime import datetime
import plotting
import sys

max_retries = 8  # Set the maximum number of retries
retry_delay = 1  # Initial delay between retries (in seconds)

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
    print("in esecuzione  ",datetime.now().strftime("%H:%M:%S"))

    retries = 0
    retry_delay = 1
    while retries < max_retries:
        try:
            #raise RuntimeError
            data = run_speedtest()
            
            break  # Break out of the loop if successful
        except Exception as e:
            print(f"Exception occurred: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retries += 1
            retry_delay *= 2  # Exponential backoff for next retry

    if retries == max_retries:
        print("Max retries exceeded without success")
        raise RuntimeError("FAILURE: could not execute speedtest")
        
    print("finito")


    current_date = datetime.now().strftime("%d-%m-%Y")
    # Create the path for the new subfolder
    subfolder_path = os.path.join(data_folder_name, current_date)
    os.makedirs(subfolder_path, exist_ok=True)

    
    ping, download, upload = extract_values(data)
    print(ping, download, upload)

    current_time = datetime.now().strftime("%H:%M")
    filename = os.path.join(subfolder_path, data_file_name)
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the values and current time to the CSV file
        csvwriter.writerow([current_time, ping, round(download,1), round(upload,1)])


    plotting.plot_data(subfolder_path, data_file_name)

retry_delay = 1  # Initial delay between retries (in seconds)


def main():
    t = 5  # minutes
    print("STARTUP OF CONTINUOS SPEED TEST")    

    schedule.every(t).minutes.do(save_to_file)   
    os.makedirs(data_folder_name, exist_ok=True)

    while 1:
        # print('a')
        schedule.run_pending()
        time.sleep(1)
        sys.stdout.flush()

            
        current_time = datetime.now()
        if current_time.hour == time_to_send_email[0] and current_time.minute >  time_to_send_email[1]:
            
            current_date = datetime.now().strftime("%d-%m-%Y")
            # Create the path for the new subfolder
            subfolder_path = os.path.join(data_folder_name, current_date)
            file_path = os.path.join(subfolder_path, "done.txt")
            
            # Check if the file exists
            if os.path.exists(file_path):
                print("email already sent")
            else:
                plotting.send_email(subfolder_path, data_file_name, "girardi.alberto71@gmail.com")


      


        
        

data_file_name = "data.csv"
data_folder_name = "data"
time_to_send_email = [23, 50]

if __name__ == "__main__":
    main()
