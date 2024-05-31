import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

## INSTRUCTIONS ##
## Adjust input parameters at the end of script under 'Input parameters'

# Input parameters
E_eV = 1.15    # Activation energy in eV
N = 1E5    # Total concentration of traps
n0 = N*(1/5)  # Initial concentration of electrons in traps
s = 5E8   # Frequency factor
beta = 7.5    # Heating rate

T0 = 1    # Starting temperature for the measurement
T_max = 1000  # Maximum temperature for the measurement

# Constants
k_J_per_K = 1.381e-23  # Boltzmann constant in J/K

# Integral function for second-order kinetics
def integral_second_order(T, T0, E_J, beta, N):
    def integrand(T_prime):
        return np.exp(-E_J / (k_J_per_K * T_prime))
    
    integral_result, _ = quad(integrand, T0, T)
    return integral_result

# Intensity function for second-order kinetics
def intensity_second_order(T, E_J, n0, s, beta, N, T0):
    integral_result = integral_second_order(T, T0, E_J, beta, N)
    numerator = n0**2 * s * np.exp(-E_J / (k_J_per_K * T))
    denominator = N * (1 + (n0 * s) / (beta * N) * integral_result)**2
    return numerator / denominator

# Function to plot I(T) against T and find T at maximum I
def plot_intensity_vs_temperature_and_find_max(E_eV, n0, s, beta, N, T0, T_max):
    # Convert E from eV to J
    E_J = E_eV * 1.602e-19
    
    # Temperature range
    T_range = np.linspace(T0, T_max, 4000)
    
    # Calculate intensity values over the temperature range
    intensity_values = [intensity_second_order(T, E_J, n0, s, beta, N, T0) for T in T_range]
    
    # Find the temperature at maximum intensity
    max_intensity_index = np.argmax(intensity_values)
    max_intensity_temperature = T_range[max_intensity_index]
    
    # Plotting
    plt.figure(figsize=(4, 3))
    plt.fill_between(T_range, intensity_values, alpha=0.5, label=f'E={E_eV} eV, s={s:.1e} s-1')
    plt.plot(T_range, intensity_values, alpha=1)


    plt.minorticks_on()
    plt.tick_params(which='major', axis='both', direction='in', 
                    length=6, labeltop=True, labelright=True, top=True, right=True, labelsize=9)
    plt.tick_params(which='minor', axis='both', direction='in', 
                    length=3, labeltop=False, labelright=False, top=True, right=True)

    plt.xlabel('Temperature, $T$ [K]')
    plt.ylabel('Intensity, $I$ [cps]')
    plt.legend(fontsize=7, loc='best')
    plt.xlim(0,800)
    plt.ylim(0,)
    plt.grid(False)
    plt.show
    
    

    # Generating the CSV file name based on the temperature, E value in eV, and s value
    filename = f"SO_PeakCalc_E{E_eV:.2f}eV_s{s:.1e}s-1_Tp{max_intensity_temperature:.1f}K"

    # Save the plot with the same naming convention
    plt.savefig(f"./calculations/{filename}.png", dpi=600, bbox_inches='tight')


    # Print the temperature of maximum intensity
    print(f'Maximum Intensity at {max_intensity_temperature:.1f} K.')
    print(f"Plot has been saved as {filename}.png")
    print(f"Data have been saved as {filename}.csv")
    
    # Create a DataFrame from the simulation data

    
    df_output_s1 = pd.DataFrame({
        'temp_K': T_range,
        'intensity': intensity_values,
    })

    # Save the DataFrame to a CSV file
    df_output_s1.to_csv(f"./calculations/{filename}.csv", index=False)

# Call the function to plot and find the maximum intensity temperature

plot_intensity_vs_temperature_and_find_max(E_eV, n0, S, beta, N, T0, T_max)