import matplotlib.pyplot as plt
import random

# Adjustable parameters
ROUNDS = 50
LOSS_PROBABILITY = 0.25     # Simulated packet loss chance
INITIAL_SSTHRESH = 16      # Slow start threshold
INITIAL_CWND = 1           # Initial congestion window

def simulate_tcp_congestion_control():
    cwnd = INITIAL_CWND
    ssthresh = INITIAL_SSTHRESH
    cwnd_history = []
    
    for round in range(ROUNDS):
        # Simulate loss
        loss = random.random() < LOSS_PROBABILITY

        if loss:
            print(f"[Round {round+1}] Packet loss detected. Reducing cwnd.")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1  # Back to slow start
        else:
            if cwnd < ssthresh:
                # Slow Start: exponential growth
                cwnd *= 2
                print(f"[Round {round+1}] Slow Start: cwnd increased to {cwnd}")
            else:
                # Congestion Avoidance: linear growth
                cwnd += 1
                print(f"[Round {round+1}] Congestion Avoidance: cwnd increased to {cwnd}")

        cwnd_history.append(cwnd)

    return cwnd_history

def plot_cwnd(cwnd_history):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(cwnd_history)+1), cwnd_history, marker='o', linestyle='-', color='blue')
    plt.title('TCP Congestion Control Simulation')
    plt.xlabel('Transmission Round')
    plt.ylabel('Congestion Window (cwnd)')
    plt.grid(True)
    plt.savefig("cwnd_plot.png")
    plt.show()

if __name__ == "__main__":
    history = simulate_tcp_congestion_control()
    plot_cwnd(history)
