# File Name: ip_utils.py

def ip_to_binary(ip_address: str) -> str:

    octets = ip_address.split('.')
    
    binary_octets = []
    for octet in octets:
        
        int_octet = int(octet)
        
       
        binary_str = bin(int_octet)[2:]
        
        
        padded_binary_str = binary_str.zfill(8)
        

        binary_octets.append(padded_binary_str)
        

    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
   
    try:
        ip_address, prefix_length_str = ip_cidr.split('/')
    except ValueError:
        return "Error: Invalid CIDR format. Expected 'ip/prefix'."
  
    prefix_length = int(prefix_length_str)
    

    full_binary_ip = ip_to_binary(ip_address)

    network_prefix = full_binary_ip[:prefix_length]
    
    return network_prefix



ip1 = "192.168.1.1"
binary_ip1 = ip_to_binary(ip1)
print(f"IP Address: {ip1}")
print(f"Binary:     {binary_ip1}")


print("-" * 20)

cidr1 = "200.23.16.0/23"
prefix1 = get_network_prefix(cidr1)
print(f"CIDR:   {cidr1}")
print(f"Prefix: {prefix1}")
