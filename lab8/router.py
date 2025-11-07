
from ip_utils import ip_to_binary, get_network_prefix

class Router:


    def __init__(self, routes: list):

        self.forwarding_table = self._build_forwarding_table(routes)

    def _build_forwarding_table(self, routes: list) -> list:

        internal_table = []
        for cidr_str, output_link in routes:
            try:

                binary_prefix = get_network_prefix(cidr_str)
                
              
                prefix_length = int(cidr_str.split('/')[1])
                
                
                internal_table.append((binary_prefix, prefix_length, output_link))
            except (ValueError, IndexError):
                print(f"Warning: Skipping invalid route format: {cidr_str}")
        

        internal_table.sort(key=lambda route_entry: route_entry[1], reverse=True)
        
        return internal_table

    def route_packet(self, dest_ip: str) -> str:

        try:
            binary_dest_ip = ip_to_binary(dest_ip)
        except ValueError:
            return f"Error: Invalid destination IP format: {dest_ip}"

      
        for binary_prefix, prefix_length, output_link in self.forwarding_table:
            
           
            if binary_dest_ip.startswith(binary_prefix):
               
                return output_link
    
        return "Default Gateway"

if __name__ == "__main__":
    
    
    test_routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    print("Initializing Router...")
    router = Router(test_routes)
    
    print("\n--- Internal Forwarding Table (Sorted by LPM) ---")
    for prefix, length, link in router.forwarding_table:
       
        print(f"  Prefix: {prefix.ljust(24)} (/{length}), Link: {link}")
    
    print("\n--- Running Packet Routing Tests ---")
    
    # Test 1
    ip_test_1 = "223.1.1.100"
    link_1 = router.route_packet(ip_test_1)
    print(f"Packet to {ip_test_1.ljust(15)} -> {link_1.ljust(15)} (Expected: Link 0)")
    
    # Test 2
    ip_test_2 = "223.1.2.5"
    link_2 = router.route_packet(ip_test_2)
    print(f"Packet to {ip_test_2.ljust(15)} -> {link_2.ljust(15)} (Expected: Link 1)")
    
    # Test 3
    ip_test_3 = "223.1.250.1"
    link_3 = router.route_packet(ip_test_3)
    print(f"Packet to {ip_test_3.ljust(15)} -> {link_3.ljust(15)} (Expected: Link 4 (ISP))")
    
    # Test 4
    ip_test_4 = "198.51.100.1"
    link_4 = router.route_packet(ip_test_4)
    print(f"Packet to {ip_test_4.ljust(15)} -> {link_4.ljust(15)} (Expected: Default Gateway)")