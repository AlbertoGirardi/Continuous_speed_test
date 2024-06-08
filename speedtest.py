import json
import subprocess

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
    with open(filename, 'w') as f:
        f.write(f"Ping: {ping} ms\n")
        f.write(f"Download: {download:.2f} Mbps\n")
        f.write(f"Upload: {upload:.2f} Mbps\n")

def main():
    print("in esecuzione")
    data = run_speedtest()
    print("finito")

    ping, download, upload = extract_values(data)
    print(ping, download, upload)
    # save_to_file('speedtest_results.txt', ping, download, upload)

if __name__ == "__main__":
    main()
