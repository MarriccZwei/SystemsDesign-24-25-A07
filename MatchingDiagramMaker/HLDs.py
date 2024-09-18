import numpy as np
import matplotlib.pyplot as plt

def estimate_cl_max_flapped(cl_max_clean, flap_type, c_prime_c=1.0, is_landing=True):
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
        raise ValueError("Invalid flap type. Choose one of: 'plain', 'single slotted', 'double slotted', 'fowler', 'double slotted fowler'")
    
    # For takeoff, typically ΔCL_max is 60-80% of the landing ΔCL_max
    if not is_landing:
        dcl_max *= 0.7  # Approximate for takeoff

    # Calculate the new CL_max with flaps deployed
    cl_max_flapped = cl_max_clean + dcl_max
    return cl_max_flapped

def plot_lift_curve(cl_max_clean, cl_max_flapped, alpha_stall_clean, alpha_stall_flapped, cl_alpha_clean):
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

# Example usage
cl_max_clean = 1.2  # CL_max of the clean wing
alpha_stall_clean = 15  # Stall angle of clean wing in degrees
cl_alpha_clean = 0.1  # CL_alpha (lift curve slope) for the clean wing

# Estimate CL_max_flapped for single slotted flap during landing
cl_max_flapped = estimate_cl_max_flapped(cl_max_clean, flap_type='single slotted', is_landing=True)

# Assume flaps extend the stall angle to 20 degrees
alpha_stall_flapped = 20

# Plot the lift curve comparison
plot_lift_curve(cl_max_clean, cl_max_flapped, alpha_stall_clean, alpha_stall_flapped, cl_alpha_clean)


