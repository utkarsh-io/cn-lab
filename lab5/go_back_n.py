import random
import time

# Adjustable parameters
TOTAL_FRAMES = 10
WINDOW_SIZE = 4
LOSS_PROBABILITY = 0.2  # Probability that a frame is lost

def simulate_go_back_n(total_frames, window_size, loss_prob):
    base = 0

    while base < total_frames:
        end = min(base + window_size, total_frames)
        print(f"Sending frames {base} to {end - 1}")
        time.sleep(1)

        loss_index = -1  # Assume no loss initially

        # Simulate frame transmission
        for i in range(base, end):
            if random.random() < loss_prob:
                print(f"❌ Frame {i} lost! Retransmitting from frame {i}...\n")
                loss_index = i
                break

        if loss_index != -1:
            # Retransmit only from the lost frame onward
            base = loss_index
            time.sleep(1)
            continue  # resend from lost frame

        # All frames received successfully
        print(f"✅ ACK {end - 1} received. Sliding window.\n")
        base = end  # Move window forward

if __name__ == "__main__":
    simulate_go_back_n(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY)
