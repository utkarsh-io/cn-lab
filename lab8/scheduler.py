# File Name: scheduler.py

from dataclasses import dataclass
from typing import List

# -----------------------------------------------------------------
# Task 1: Packet Class
# -----------------------------------------------------------------
@dataclass
class Packet:
    """
    A simple dataclass to store packet attributes.
    Priority: 0=High, 1=Medium, 2=Low
    """
    source_ip: str
    dest_ip: str
    payload: str
    priority: int


# -----------------------------------------------------------------
# Task 2: FIFO Scheduler
# -----------------------------------------------------------------
def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:


    return packet_list[:]

# -----------------------------------------------------------------
# Task 3: Priority Scheduler
# -----------------------------------------------------------------
def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:

    return sorted(packet_list, key=lambda packet: packet.priority)


# -----------------------------------------------------------------
# Test Case (as specified in the assignment)
# -----------------------------------------------------------------
if __name__ == "__main__":
    
    print("Creating Test Packets...")
    # We add dummy IPs as they are required by the class
    p1 = Packet(source_ip="s1", dest_ip="d1", payload="Data Packet 1", priority=1)
    p2 = Packet(source_ip="s2", dest_ip="d2", payload="Data Packet 2", priority=2)
    p3 = Packet(source_ip="s3", dest_ip="d3", payload="VOIP Packet 1", priority=0)
    p4 = Packet(source_ip="s4", dest_ip="d4", payload="Video Packet 1", priority=1)
    p5 = Packet(source_ip="s5", dest_ip="d5", payload="VOIP Packet 2", priority=0)


    arrival_list = [p1, p2, p3, p4, p5]
    
    print("--- Testing FIFO Scheduler ---")
    fifo_result = fifo_scheduler(arrival_list)
    

    fifo_payloads = [p.payload for p in fifo_result]
    print(f"Payload Order: {fifo_payloads}")
    
    expected_fifo = ["Data Packet 1", "Data Packet 2", "VOIP Packet 1", "Video Packet 1", "VOIP Packet 2"]
    print(f"Matches Expected: {fifo_payloads == expected_fifo}\n")


    print("--- Testing Priority Scheduler ---")
    priority_result = priority_scheduler(arrival_list)
    
    priority_payloads = [p.payload for p in priority_result]
    print(f"Payload Order: {priority_payloads}")

    expected_priority_stable = ["VOIP Packet 1", "VOIP Packet 2", "Data Packet 1", "Video Packet 1", "Data Packet 2"]
    print(f"Stable Sort (Logical) Result: {priority_payloads == expected_priority_stable}")
    
    expected_priority_image = ["VOIP Packet 1", "VOIP Packet 2", "Video Packet 1", "Data Packet 1", "Data Packet 2"]
    print(f"Matches Image Test Case: {priority_payloads == expected_priority_image}")

