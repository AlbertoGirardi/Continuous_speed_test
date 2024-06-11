import json
import subprocess
import os
import schedule 
import time
import csv
from datetime import datetime
import plotting
import sys

class bcolors:  #colors for output
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


max_retries =  9 # Set the maximum number of retries
retry_delay = 1  # Initial delay between retries (in seconds)

def run_speedtest():
    # Run the speedtest-cli command and get the JSON output
    result = subprocess.run(['speedtest-cli', '--secure', '--json'], stdout=subprocess.PIPE)
    return json.loads(result.stdout)

def extract_values(data):
    # Extract the required values from the speedtest result
    ping = data['ping']
    download = data['download'] / 1_000_000  # Convert from bps to Mbps
    upload = data['upload'] / 1_000_000      # Convert from bps to Mbps
    return ping, download, upload

def save_to_file():
    # executes and then saves the values of the speed test
    print("in esecuzione  ",datetime.now().strftime("%H:%M:%S"))

    #handles potential erros of the speedtest
    #if an error is detected the program waits and retries until a max amount of times
    retries = 0
    retry_delay = 1
    while retries < max_retries:
        try:
            
            data = run_speedtest()   #runs the speedtest
            break  # Break out of the loop if successful


        except Exception as e:
            #if there is a failure
            print(f"{bcolors.FAIL}failure{bcolors.ENDC}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retries += 1
            retry_delay *= 2  # Exponential backoff for next retry

    if retries == max_retries:
        print("Max retries exceeded without success")
        raise RuntimeError("FAILURE: could not execute speedtest")
        
    print(f"{bcolors.OKGREEN}finito{bcolors.ENDC}")


    current_date = datetime.now().strftime("%d-%m-%Y")
    # Create the path for the new subfolder, where to store the results
    subfolder_path = os.path.join(data_folder_name, current_date)
    os.makedirs(subfolder_path, exist_ok=True)

    
    ping, download, upload = extract_values(data)       #extracts the values 
    print(bcolors.OKBLUE,ping,' ',round(download,1),' ', round(upload,1),' ', bcolors.ENDC, sep='')

    current_time = datetime.now().strftime("%H:%M")
    filename = os.path.join(subfolder_path, data_file_name)
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the values and current time to the CSV file
        csvwriter.writerow([current_time, ping, round(download,1), round(upload,1)])


    plotting.plot_data(subfolder_path, data_file_name)   #call the function to plot the data

retry_delay = 1  # Initial delay between retries (in seconds)




def main():

    #opens the settings file to retrieve parameters
    with open('settings.json', 'r') as file:
        settings = json.load(file)

    t = settings['t']
    time_to_send_email = settings['time']

    print(f"Speedtest will be executed every: {t} minutes")
    print(f"time at which daily email is going to be sent: {time_to_send_email}")
    
    print("STARTUP OF CONTINUOS SPEED TEST")    

    #sets up the recurrent task of executing the speed test
    schedule.every(t).minutes.do(save_to_file)   
    os.makedirs(data_folder_name, exist_ok=True)

    #forever looo
    while 1:
        # print('a')
        schedule.run_pending()
        time.sleep(1)
        sys.stdout.flush()

        #checks if to send the email, after the given hour
        current_time = datetime.now()
        if current_time.hour == time_to_send_email[0] and current_time.minute >  time_to_send_email[1]:
            
            current_date = datetime.now().strftime("%d-%m-%Y")
            # Create the path for the new subfolder
            subfolder_path = os.path.join(data_folder_name, current_date)
            file_path = os.path.join(subfolder_path, "done.txt")
            
            # Check if the file exists, meaning that the email has already being sent
            if os.path.exists(file_path):
                print("email already sent")
            else:
                #otherwise sends the email to the required address
                plotting.send_email(subfolder_path, data_file_name, "girardi.alberto71@gmail.com")


      


data_file_name = "data.csv"
data_folder_name = "data"


if __name__ == "__main__":   #executable guard
    main()
