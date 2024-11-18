import numpy as np

# File path
file_path = "Loads\MainWing_a=0.00_v=10.00ms.txt"

# Load data, skipping the header and footer lines to extract the table
data = np.genfromtxt(
    file_path,
    skip_header=40,  # Skip the first 20 lines to start at line 21
    max_rows=19,     # max rows
    usecols=(0, 3, 5, 6)  # Columns: y, Cl, Cd, Cm
)

print(data)

# Extract individual columns into lists
ylst = data[:, 0].tolist()
Cllst = data[:, 1].tolist()
Cdlst = data[:, 2].tolist()
Cmlst = data[:, 3].tolist()

# Output for verification
print("Y-coordinates:", ylst)
print("Lift Coefficients:", Cllst)
print("Drag Coefficients:", Cdlst)
print("Pitching Moment Coefficients:", Cmlst)