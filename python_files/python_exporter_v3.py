from prometheus_client import start_http_server, Gauge
import time
import queue
import python_util_v2
import json



in_q = queue.Queue()
out_q = queue.Queue()

ping_time_output = {}
ping_packet = {}


def create_metrics(ip_address):
    
    metric_name = f'rtt_values_{ip_address.replace(".", "_")}'
    packet_output=f'packet_size__{ip_address.replace(".", "_")}'
    print(metric_name)
    if ip_address not in ping_time_output:
        ping_time_output[ip_address] = Gauge(metric_name, 'Round Trip Time (RTT) values', ['ip_address', 'timestamp'])
        print(ping_time_output[ip_address])
        ping_packet[ip_address] = Gauge(packet_output, 'Output Packet Size', ['ip_address', 'timestamp'])

def set_metrics(ip_address, rtt_values, out_packet_size, timestamp):
    if rtt_values:
        ping_time_output[ip_address].labels(ip_address=ip_address, timestamp=timestamp).set(rtt_values)

    if out_packet_size:
        ping_packet[ip_address].labels(ip_address=ip_address, timestamp=timestamp).set(out_packet_size)

def get_time(): 
    result=in_q.get()
    rtt_values1=[]
      
    while True:
        rtt_values1, output_packet_size1 = python_util_v2.ping_con(result[1])
        timestamp = int(time.time())

        set_metrics(result[1], rtt_values, output_packet_size1, timestamp)
        if rtt_values1:
            rtt_values = rtt_values1[0]
            print(f"RTT for {result[1]}: {rtt_values}")
        else:
            print(f"No RTT values received for {result[1]}")
        
        time.sleep(5)   

        

    

def parameter_ping():
    i=0 
    result=in_q.get()  
    rtt_values1=0
    while(i<int(result[2])):
        rtt_values1,out_packet_size1=python_util_v2.ping_parameter(result[1],result[3])
        timestamp = int(time.time())

        set_metrics(result[1], rtt_values1[0], out_packet_size1, timestamp)

        if rtt_values1:
            rtt_values = rtt_values1[0]
            print(f"RTT for {result[1]}: {rtt_values}")
        else:
            print(f"No RTT values received for {result[1]}")
    
        time.sleep(5)
        i=i+1
    return rtt_values

def repeat_ping():
    i=0
    result=in_q.get() 
 
    while(i<int(result[2])):
        rtt_values1,out_packet_size1=python_util_v2.ping_parameter(result[1],result[3])

        timestamp = int(time.time())

        set_metrics(result[1], rtt_values, out_packet_size1, timestamp)
        if rtt_values1:
            rtt_values = rtt_values1[0]
            print(f"RTT for {result[1]}: {rtt_values}")
        else:
            print(f"No RTT values received for {result[1]}")
    
        time.sleep(int(result[4]))
        i=i+1
    return rtt_values



  
def main():
    with open("/app/data/data.json", "r") as file:
        data = json.load(file)
        
        start_http_server(8011)
        print("Prometheus server started on port 8011")    
        ping_mode = data['ping_mode']      
        
        if (ping_mode==1):         
            ip_address=data['ip_address']
            create_metrics(ip_address)
            in_q.put(ping_mode,ip_address)                      
            get_time()             
           
            
        
        elif (ping_mode==2):            
            ip_address=data['ip_address'] 
            count=data['count']
            packet_size=data['packet_size']
            create_metrics(ip_address)
            in_q.put((ping_mode,ip_address,count,packet_size))          
            parameter_ping()
            
           
           

        elif (ping_mode==3):            
            ip_address=data['ip_address']
            count=data['count'] 
            packet_size=data['packet_size']
            sleep_time=data['sleep_time']
            create_metrics(ip_address)
            in_q.put((ping_mode,ip_address,count,packet_size,sleep_time))          
            repeat_ping()
          

        else:
            print("error")
    

if __name__ == '__main__':
    main()


