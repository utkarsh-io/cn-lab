import random
import time

# Adjustable parameters
TOTAL_FRAMES = 10
WINDOW_SIZE = 4
LOSS_PROBABILITY = 0.2  # Probability that a frame is lost

def simulate_go_back_n(total_frames, window_size, loss_prob):
    base = 0
    next_seq_num = 0

    while base < total_frames:
        # Send frames in window
        end = min(base + window_size, total_frames)
        print(f"Sending frames {base} to {end - 1}")
        time.sleep(1)

        # Simulate sending and receiving ACKs
        loss_index = -1  # No loss initially

        for i in range(base, end):
            if random.random() < loss_prob:
                print(f"Frame {i} lost, retransmitting frames {i} to {end - 1}\n")
                loss_index = i
                break  # Simulate Go-Back-N: stop and go back

        if loss_index != -1:
            # Retransmit from the lost frame
            time.sleep(1)
            continue  # base stays the same, resend window

        # All frames received successfully
        print(f"ACK {end - 1} received\n")
        base = end  # Slide window

if __name__ == "__main__":
    # You can customize these values if needed
    simulate_go_back_n(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY)
