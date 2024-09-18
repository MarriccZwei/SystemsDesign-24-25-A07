import numpy as np
import matplotlib.pyplot as plt

def estimate_cl_max_flapped(cl_max_clean, flap_type, c_prime_c=1.0, is_landing=True):
    """
    Estimate the CL_max for a wing with deployed flaps based on flap type.
    
    Parameters:
    cl_max_clean (float): CL_max of the clean wing.
    flap_type (str): Type of flap ('plain', 'single slotted', 'double slotted', 'fowler', etc.).
    c_prime_c (float): The ratio of extended chord to original chord (for Fowler flaps).
    is_landing (bool): Whether the configuration is for landing (True) or takeoff (False).
    
    Returns:
    cl_max_flapped (float): The new CL_max with flaps deployed.
    """
    # Define ΔCL_max based on flap type (data from the presentation)
    if flap_type == 'plain':
        dcl_max = 0.9
    elif flap_type == 'single slotted':
        dcl_max = 1.3
    elif flap_type == 'double slotted':
        dcl_max = 1.6
    elif flap_type == 'fowler':
        dcl_max = 1.3 * c_prime_c
    elif flap_type == 'double slotted fowler':
        dcl_max = 1.6 * c_prime_c
    else:
        raise ValueError("Invalid flap type. Choose 'plain', 'single slotted', 'double slotted', 'fowler', 'double slotted fowler'")
    
    # For takeoff, typically ΔCL_max is 60-80% of the landing ΔCL_max
    if not is_landing:
        dcl_max *= 0.7  # Approximate for takeoff
    
    # Calculate the new CL_max with flaps deployed
    cl_max_flapped = cl_max_clean + dcl_max
    return cl_max_flapped

def plot_lift_curve(cl_max_clean, cl_max_flapped, alpha_stall_clean, alpha_stall_flapped, cl_alpha_clean):
    """
    Plot the lift curve for clean and flapped configurations.
    
    Parameters:
    cl_max_clean (float): CL_max of the clean wing.
    cl_max_flapped (float): CL_max of the flapped wing.
    alpha_stall_clean (float): Stall angle (degrees) for clean configuration.
    alpha_stall_flapped (float): Stall angle (degrees) for flapped configuration.
    cl_alpha_clean (float): Lift curve slope for the clean wing (dCL/dα).
    """
    # Create a range of angles of attack (α)
    alpha = np.linspace(-5, alpha_stall_clean + 5, 100)
    
    # Clean wing lift curve (linear till stall)
    cl_clean = np.where(alpha <= alpha_stall_clean, cl_alpha_clean * np.radians(alpha), cl_max_clean)

    # Flapped wing lift curve (shifted and with new CL_max)
    cl_flapped = np.where(alpha <= alpha_stall_flapped, cl_alpha_clean * np.radians(alpha), cl_max_flapped)
    
    # Plotting
    plt.figure(figsize=(8,6))
    plt.plot(alpha, cl_clean, label="Clean Wing", color='b')
    plt.plot(alpha, cl_flapped, label="Flapped Wing", color='r')
    plt.axhline(y=cl_max_clean, color='b', linestyle='--')
    plt.axhline(y=cl_max_flapped, color='r', linestyle='--')
    plt.axvline(x=alpha_stall_clean, color='b', linestyle='--')
    plt.axvline(x=alpha_stall_flapped, color='r', linestyle='--')
    plt.xlabel("Angle of Attack (deg)")
    plt.ylabel("Lift Coefficient (CL)")
    plt.title("Lift Curve Comparison: Clean vs Flapped Wing")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage with variables
S = 400  # Wing area in square meters
chord = 7  # Wing chord in meters
cl_cruise = 0.6  # CL in cruise
cl_landing = 2.5  # Required CL in landing
cl_takeoff = 1.8  # Required CL in takeoff

cl_max_clean = cl_cruise  # Assume the maximum CL for clean wing equals CL in cruise
alpha_stall_clean = 15  # Stall angle for clean wing in degrees
cl_alpha_clean = 0.1  # Lift curve slope for the clean wing

# Estimate CL_max_flapped for single slotted flap during landing
cl_max_flapped_landing = estimate_cl_max_flapped(cl_max_clean, flap_type='single slotted', is_landing=True)

# Estimate CL_max_flapped for takeoff
cl_max_flapped_takeoff = estimate_cl_max_flapped(cl_max_clean, flap_type='single slotted', is_landing=False)

# Assume flaps extend the stall angle to 20 degrees during landing
alpha_stall_flapped = 20

# Plot the lift curve comparison for landing configuration
plot_lift_curve(cl_max_clean, cl_max_flapped_landing, alpha_stall_clean, alpha_stall_flapped, cl_alpha_clean)


