import subprocess

def run_iperf_server():
    iperf_server_command = ["iperf3", "-s", "-p", "5201"]  # Adjust port as needed
    try:
        subprocess.run(iperf_server_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running iperf3 server: {e}")

if __name__ == "__main__":
    run_iperf_server()