import matplotlib.pyplot as plt
import csv

values = []
iterations = []
counter = 0

with open('Shotdeck2.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        try:
            # Adjust the column index as needed
            value = float(row[1])  # assuming column 1 contains the numeric values
            values.append(value)
            counter += 1
            iterations.append(counter)
            print(row)
            if counter > 32:
                break
        except (ValueError, IndexError):
            # Skip rows where conversion fails or where the column doesn't exist
            continue

# Create the bar chart using the iterations as the x-axis values
plt.bar(iterations, values)

# Add title and axis labels
plt.title("exterior, woods, night, forest")
plt.xlabel("Iteration")
plt.ylabel("Values")

# Display the plot
plt.show()
