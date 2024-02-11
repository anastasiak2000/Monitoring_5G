
import time
import subprocess
from prometheus_client import start_http_server, Gauge
import json
import re

sent_Mbps = Gauge('sent_Mbps', 'sent_Mbps')
received_Mbps = Gauge('received_Mbps', 'received_Mbps')


# Store results for each second in a list
received_results = []

def read_metrics_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data.get('sent_Mbps', 0), data.get('received_Mbps', 0)

def update_prometheus_metrics():
    sent, received = read_metrics_from_json('/vscode/iperf/iperf_results.json')
    sent_Mbps.set(sent)
    for value in received:
        received_Mbps.set(value)
        time.sleep(5)
        

def run_iperf_client(server, protocol, duration=10, bandwidth='100M', interval=1):

    # Construct the iPerf3 command
    iperf_command = [
        "iperf3",
        "-c", server,
        "-i", str(interval),
        "-t", str(duration),
        "-b", bandwidth,
    ]

    if protocol == 'tcp':
        print("tcp")
    elif protocol == 'udp':
        iperf_command += ["-u"]

    # Run the iPerf3 command and capture output
    result = subprocess.run(iperf_command, capture_output=True, text=True)
    
    # Parse the iPerf3 result
    try:
        
        bitrate_line_sender =str( [line for line in result.stdout.splitlines() if "sender" in line])
        match = re.search(r'(\d+(\.\d+)?)\s*Mbits/sec', bitrate_line_sender)
           
        sender_bitrate = float(match.group(1))
        print(sender_bitrate)
        # Extract the sender and receiver bitrates for each second
        bitrate_lines = [line for line in result.stdout.splitlines() if "Mbits/sec" in line]
        for line in bitrate_lines:
            match = re.search(r'(\d+(\.\d+)?)\s*Mbits/sec', line)
            receiver_bitrate = float(match.group(1))
            received_results.append(receiver_bitrate)
        print(receiver_bitrate)
    except (IndexError, ValueError) as e:
        print(f"Error parsing iPerf result: {e}")
        print(result.stdout)

    # Save results to JSON file
    with open("/vscode/iperf/iperf_results.json", 'w') as json_file:
        json.dump({"sent_Mbps": sender_bitrate, "received_Mbps": received_results}, json_file, indent=2)

    print("Results:")
    update_prometheus_metrics()
    print(f"  Sent   {sender_bitrate} Mbps")
    print(f"  Received {received_results} Mbps")

if __name__ == "__main__":
    server_address = "172.21.199.108"
    server_port = 5202
    output_file = "/vscode/iperf/iperf_results.json"
    start_http_server(8011)
    print("Connected to 8011")
    protocol = 'tcp'
    run_iperf_client(server_address, protocol)
