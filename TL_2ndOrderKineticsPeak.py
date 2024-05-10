import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

## INSTRUCTIONS ##
## Adjust input parameters at the end of script under 'Input parameters'


# Constants
k_J_per_K = 1.381e-23  # Boltzmann constant in J/K

# Integral function for second-order kinetics
def integral_second_order(T, T0, E_J, beta, N):
    def integrand(T_prime):
        return np.exp(-E_J / (k_J_per_K * T_prime))
    
    integral_result, _ = quad(integrand, T0, T)
    return integral_result

# Intensity function for second-order kinetics
def intensity_second_order(T, E_J, n0, S, beta, N, T0):
    integral_result = integral_second_order(T, T0, E_J, beta, N)
    numerator = n0**2 * S * np.exp(-E_J / (k_J_per_K * T))
    denominator = N * (1 + (n0 * S) / (beta * N) * integral_result)**2
    return numerator / denominator

# Function to plot I(T) against T and find T at maximum I
def plot_intensity_vs_temperature_and_find_max(E_eV, n0, S, beta, N, T0, T_max):
    # Convert E from eV to J
    E_J = E_eV * 1.602e-19
    
    # Temperature range
    T_range = np.linspace(T0, T_max, 500)
    
    # Calculate intensity values over the temperature range
    intensity_values = [intensity_second_order(T, E_J, n0, S, beta, N, T0) for T in T_range]
    
    # Find the temperature at maximum intensity
    max_intensity_index = np.argmax(intensity_values)
    max_intensity_temperature = T_range[max_intensity_index]
    
    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(T_range, intensity_values, label=f'Second-order kinetics (E={E_eV} eV)')
    #plt.scatter(max_intensity_temperature, intensity_values[max_intensity_index], color='red')  # Mark the max point
    plt.xlabel('Temperature (K)')
    plt.ylabel('Intensity')
    plt.title('Intensity vs Temperature for Second-order Kinetics')
    plt.legend()
    plt.grid(True)
    #plt.xlim(300,580)
    plt.show
    
    # Print the temperature of maximum intensity
    print(f'The maximum intensity occurs at {max_intensity_temperature:.1f} K.')

# Input parameters
E_eV = 0.7    # Activation energy in eV
N = 2.06E7    # Total concentration of traps
n0 = N*(1/5)  # Initial concentration of electrons in traps
S = 4.89E14   # Frequency factor
beta = 7.5    # Heating rate

T0 = 1    # Starting temperature for the measurement
T_max = 1000  # Maximum temperature for the measurement

# Call the function to plot and find the maximum intensity temperature

plot_intensity_vs_temperature_and_find_max(E_eV, n0, S, beta, N, T0, T_max)
