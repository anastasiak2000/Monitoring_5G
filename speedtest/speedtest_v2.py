from prometheus_client import start_http_server, Gauge
import json
import time
import speedtest

Download_Speed = Gauge('download_speed', 'download_speed')
Upload_Speed = Gauge('upload_speed', 'upload_speed')

output_file = "speedtest_output.json"


def read_speedtest_metrics_from_json(file_path):
    with open(file_path, 'r') as log_file:
        log_content = log_file.read()

        # Search for lines containing download and upload speeds
        download_line = next((line for line in log_content.split('\n') if 'Download:' in line), None)
        upload_line = next((line for line in log_content.split('\n') if 'Upload:' in line), None)

        # Extract speeds from the lines
        download_speed = float(download_line.split(':')[-1].strip().split()[0]) if download_line else 0
        upload_speed = float(upload_line.split(':')[-1].strip().split()[0]) if upload_line else 0

        print(download_speed)

        return download_speed, upload_speed


def update_prometheus_speedtest_metrics(st):
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps

    Download_Speed.set(download_speed)
    Upload_Speed.set(upload_speed)
    time.sleep(15)


def main():
    try:
        st = speedtest.Speedtest()

        # Write the output to a JSON file
        with open(output_file, 'w') as file:
            json.dump(st.results.dict(), file)

        print("Output written to", output_file)

        # Update Prometheus metrics
        update_prometheus_speedtest_metrics(st)

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    # Start Prometheus HTTP server
    start_http_server(8011)

    # Run the main function
    main()
