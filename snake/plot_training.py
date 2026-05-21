import csv
import matplotlib.pyplot as plt

episodes = []
average_scores = []

with open("training_stats.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        episodes.append(int(row["Episode"]))
        average_scores.append(float(row["Average Score"]))

plt.plot(episodes, average_scores)

plt.xlabel("Episode")
plt.ylabel("Average Score")
plt.title("Q-learning Training")
plt.grid(True)
plt.show()