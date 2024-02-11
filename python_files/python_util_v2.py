import subprocess
import re

def ping_con(ip_address):
    #while True:
    print("ping")
    rtt_values = []  # Initialize rtt_values as an empty list
    packet_size = ""  # Initialize packet_size as an empty string  
    
    try:
        output = subprocess.check_output(['ping', '-c', '1', ip_address])  # Change the value '4' to adjust the number of pings
        output = output.decode('utf-8')  # Convert bytes to string
        print(output)
        rtt_matches = re.findall(r'time=([\d.]+)', output)
        packet_size_match = re.search(r'(\d+)\(\d+\) bytes of data', output)                
        if rtt_matches and packet_size_match:
            rtt_values = [float(rtt) for rtt in rtt_matches]
            packet_size = str(packet_size_match.group(1))
            print(rtt_values[0])
            print(packet_size)
        else:
            print("error")

    except subprocess.CalledProcessError as e:
        # Print the details of the exception
        print("CalledProcessError occurred:")
        print("Command:", e.cmd)
        print("Return Code:", e.returncode)
        print("Output:", e.output)
        print("Exception:", e)
        pass
        
    return rtt_values, packet_size
        

def ping_parameter(ip_address,packet_size1):
    rtt_values= []
    packet_size = ""
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-s', str(packet_size1), ip_address])
        output = output.decode('utf-8')
        rtt_matches = re.findall(r'time=([\d.]+)', output)
        packet_size_match = re.search(r'(\d+)\(\d+\) bytes of data', output)        
        if rtt_matches and packet_size_match:
            rtt_values = [float(rtt) for rtt in rtt_matches]
            packet_size=str(packet_size_match.group(1))
            print(rtt_values)
            
            
    except subprocess.CalledProcessError:
        pass
    return rtt_values,packet_size
   


"""def ping_choice(ip_address,choice_ping):
    if (choice_ping=="1"):
        print("11")
        ping_con(ip_address)
    elif (choice_ping=="2"):
        count=input("How many ping do you want :")
        packet_size=input("Insert packet size of ping:")
        ping_parameter(ip_address,count,packet_size)
    else:
        print("fail")"""


# Example usage
