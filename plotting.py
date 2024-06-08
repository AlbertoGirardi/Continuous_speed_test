import os
import pandas as pd
import matplotlib.pyplot as plt

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
    plt.show()

# Example usage:
subfolder_path = "data\\08-06-2024"
data_file_name = "data.csv"  # Adjust as needed
plot_data(subfolder_path, data_file_name)
