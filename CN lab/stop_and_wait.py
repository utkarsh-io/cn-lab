import random
import time

# Simulation parameters
FRAME_COUNT = 5             # Number of frames to send
LOSS_PROBABILITY = 0.3      # Probability of frame loss
TIMEOUT = 2                 # Seconds before timeout

def simulate_stop_and_wait():
    frame_number = 0

    while frame_number < FRAME_COUNT:
        print(f"Sending Frame {frame_number}")
        time.sleep(1)  # Simulate transmission delay

        # Simulate frame loss
        if random.random() < LOSS_PROBABILITY:
            print(f"Frame {frame_number} lost, retransmitting ...")
            time.sleep(TIMEOUT)
            continue  # Retransmit the same frame

        # Simulate ACK received
        print(f"ACK {frame_number} received\n")
        frame_number += 1  # Move to next frame

if __name__ == "__main__":
    simulate_stop_and_wait()
