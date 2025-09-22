import random
import matplotlib.pyplot as plt

# Parameters
num_flips = 10000

# Simulate coin flips: +1 for heads, -1 for tails
outcomes = [1 if random.random() < 0.5 else -1 for _ in range(num_flips)]

# Cumulative sum to track the path
position = [0]  # start at 0
for outcome in outcomes:
    position.append(position[-1] + outcome)

# Plotting the graph
plt.figure(figsize=(12, 6))
plt.plot(position, label='Coin Flip Path', color='blue')
plt.title('Random Walk: 10,000 Coin Flips')
plt.xlabel('Number of Flips')
plt.ylabel('Position')
plt.grid(True)
plt.legend()
plt.show()
