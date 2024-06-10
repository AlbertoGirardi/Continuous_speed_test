import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

colum_labels = ["Ping [ms]", 'Download [MB/s]', 'Upload [MB/s]']

def plot_data(subfolder_path, data_file_name):
    # Step 1: Traverse the folder and locate the file
    file_path = os.path.join(subfolder_path, data_file_name)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{data_file_name}' not found in folder '{subfolder_path}'.")
        return
    
    # Step 2: Read the data file and select the columns
    try:
        df = pd.read_csv(file_path)  # Assuming it's a CSV file, adjust if needed
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Assuming the first column is time and the last three are the ones to plot
    time_column = df.columns[0]
    data_columns = df.columns[-3:]
    
    # Step 3: Plot the data
    plt.figure(figsize=(10, 6))
    
    for i, column in enumerate(data_columns):
        plt.plot(df[time_column], df[column], label=colum_labels[i])
    
    plt.xlabel("Time")

    plt.title(f"HOME CONNECTION PERFORMANCE - {subfolder_path.split(os.path.sep)[-1]}")
    plt.legend()
    plt.grid(True)

    # plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))  # Assuming datetime format, adjust if needed
    plt.xticks(rotation=45)  # Rotate the labels to avoid overlapping
    plt.tick_params(axis='x', labelsize=6)  # Set the font size of x-axis labels
    # Display only 1 out of 5 labels on the x-axis
    x_values = df[time_column]
    num_labels = len(x_values)
    step = (num_labels // 5)+1  # Select one out of five

    xticks = x_values[::step]  # Select every 'step' label
    xticklabels = [str(label) for label in xticks]  # Convert to strings for labels

    plt.gca().set_xticks(xticks)
    plt.gca().set_xticklabels(xticklabels)

    plt.savefig(os.path.join(subfolder_path, "connectivity_graph.png"))
    # plt.show()
    plt.close()
    



def send_email(subfolder_path, data_file_name,  recipient_email):
    # Step 1: Traverse the folder and locate the file
    file_path = os.path.join(subfolder_path, data_file_name)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{data_file_name}' not found in folder '{subfolder_path}'.")
        return
    
    # Step 2: Read the data file and select the columns
    try:
        df = pd.read_csv(file_path)  # Assuming it's a CSV file, adjust if needed
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Calculate average, maximum, and minimum of the last three columns
    last_three_columns = df.iloc[:, -3:]
    average_values = last_three_columns.mean()
    max_values = last_three_columns.max()
    min_values = last_three_columns.min()


     
    # Step 6: Prepare email content
    email_text = f"""
  
PING[ms]:      \t avg:{round(average_values[0],1)}\tmax:{round(max_values[0],1)}\tmin:{round(min_values[0],1)}
DOWNLOAD[MB/s]:\t avg:{round(average_values[1],1)}\tmax:{round(max_values[1],1)}\tmin:{round(min_values[1],1)}
UPLOAD[MB/s]:   \tavg:{round(average_values[2],1)}\tmax:{round(max_values[2],1)}\tmin:{round(min_values[2],1)}
    
   """         
    
    # Step 7: Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = "your_email@example.com"  # Sender's email address
    msg['To'] = recipient_email
    msg['Subject'] = 'Home connectivity performance for '+subfolder_path.split(os.path.sep)[-1]
    
    # Attach email text
    msg.attach(MIMEText(email_text, 'plain'))
    
    # Attach data file
    data_attachment = open(file_path, "rb")
    data_part = MIMEBase('application', 'octet-stream')
    data_part.set_payload(data_attachment.read())
    encoders.encode_base64(data_part)
    data_part.add_header('Content-Disposition', f"attachment; filename= {data_file_name}")
    msg.attach(data_part)
    
    # Attach plot image
    plot_attachment = open(os.path.join(subfolder_path, "connectivity_graph.png"), "rb")
    plot_part = MIMEBase('application', 'octet-stream')
    plot_part.set_payload(plot_attachment.read())
    encoders.encode_base64(plot_part)
    plot_part.add_header('Content-Disposition', f"attachment; filename= plot.png")
    msg.attach(plot_part)
    
    # Step 8: Send the email
    smtp_server = "smtp.libero.it"  # SMTP server address
    smtp_port = 587  # SMTP port (587 for TLS)
    sender_email = "motore1234567@libero.it"  # Your email address

    with open("password.txt", 'r') as file:
        sender_password = file.read().strip()
    

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print("Email sent successfully!")
    file_path = os.path.join(subfolder_path, "done.txt")
    with open(file_path, 'w'):
        pass

if __name__ == "__main__":
        
    # Example usage:
    subfolder_path = "data\\09-06-2024"
    data_file_name = "data.csv"  # Adjust as needed
    plot_data(subfolder_path, data_file_name)
    #send_email(subfolder_path, data_file_name, "girardi.alberto71@gmail.com")
