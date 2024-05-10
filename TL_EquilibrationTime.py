from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## INSTRUCTIONS
## Adjust 'Parameters for the simulation' as desired
## The script will generate a plot and a .csv file with the kinetic parameters in the filename

# Parameters for the simulation
N = 1E12                # Total concentration of traps
R = 3.17E-9             # Dose rate in Gray per second
alpha = 1.7E-7          # Rate constant for trap filling
s = 7E14                # Frequency factor for electron escape
E_eV = 0.55             # Activation energy in eV
T = 90                  # Environment temperature in Kelvin
E = E_eV * 1.602e-19    # Activation energy converted to Joules, no input needed!

# Constants
k_B = 1.381e-23  # Boltzmann constant in J/K

# Differential equation for the dynamics of trap filling and emptying
def trap_dynamics(n, t, N, R, alpha, s, E, T):
    kT = k_B * T
    filling_rate = alpha * (N - n) * R
    emptying_rate = n * s * np.exp(-E / kT)
    return filling_rate - emptying_rate

# Time span for the simulation in seconds (100,000 years)
time_span = np.linspace(0, 4E9 * 365.25 * 24 * 3600, 100000)

# Initial condition: starting with no traps filled
initial_n = 0

# Solving the differential equation using odeint for the new time span
solution_long_term = odeint(trap_dynamics, initial_n, time_span, args=(N, R, alpha, s, E, T))

# Converting time from seconds to millions of years for plotting
time_million_of_years = time_span / (1000000 * 365.25 * 24 * 3600)

# Plotting the results for the long-term simulation
plt.figure(figsize=(10, 6))
plt.plot(time_million_of_years, solution_long_term, label='Number of Trapped Electrons')
plt.xlabel('Time (Millions of Years)')
plt.ylabel('Number of Trapped Electrons')
plt.xlim(0,250)
plt.legend()
plt.grid(True)



# Generating the CSV file name based on the temperature, E value in eV, and s value
filename = f"Trapped_Electrons_T_{int(T)}K_E_{E_eV:.2f}eV_s_{s:.1e}.csv"

# Save the plot with the same naming convention
plt.savefig(f"{filename}.png")

plt.show()

print(f"Plot has been saved as {filename}.png")

# Create a DataFrame from the simulation data
df_output = pd.DataFrame({
    'Time (Million Years)': time_million_of_years,
    'Number of Trapped Electrons': solution_long_term.flatten()
})


# Save the DataFrame to a CSV file
df_output.to_csv(filename, index=False)

print(f"Data has been saved to {filename}")