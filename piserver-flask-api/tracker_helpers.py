import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_positions(positions, anchor_points=None, output_file=None):
    """
    Create a 3D scatter plot of position data over time.

    Parameters:
    - positions: List of 3D position tuples (x, y, z) over time.
    - anchor_points: Optional list of anchor points as tuples (x, y, z).
    - output_file: Optional output file path. If provided, the plot will be saved to the file.

    Returns:
    - None (displays the plot or saves to a file).
    """
    # diff_anch_1_2tract x, y, z coordinates
    x, y, z = zip(*positions)

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot for device positions
    ax.scatter(x, y, z, c='r', marker='o', label='Device Positions')

    # Scatter plot for anchor points if provided
    if anchor_points:
        anchor_x, anchor_y, anchor_z = zip(*anchor_points)
        ax.scatter(anchor_x, anchor_y, anchor_z, c='b', marker='^', label='Anchor Points')

    # Set labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Set title
    ax.set_title('3D Scatter Plot of Device Positions Over Time')

    # Show legend
    ax.legend()

    # Save to a file or display the plot
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


def trilaterate_3d(anchor1, anchor2, anchor3, distance1, distance2, distance3):
    # Coordinates of the anchors
    x1, y1, z1 = anchor1
    x2, y2, z2 = anchor2
    x3, y3, z3 = anchor3

    # Calculate the differences in coordinates
    ex = [x2 - x1, y2 - y1, z2 - z1]
    ey = [x3 - x1, y3 - y1, z3 - z1]

    # Calculate the distance between anchor1 and anchor2
    d = math.sqrt(ex[0] ** 2 + ex[1] ** 2 + ex[2] ** 2)

    # Normalize ex to unit length
    ex = [ex[0] / d, ex[1] / d, ex[2] / d]

    # Calculate the component of ey parallel to ex
    i = ex[0] * ey[0] + ex[1] * ey[1] + ex[2] * ey[2]

    # Calculate the component of ey perpendicular to ex
    ey = [ey[0] - i * ex[0], ey[1] - i * ex[1], ey[2] - i * ex[2]]

    # Calculate the distance between anchor1 and the device
    j = math.sqrt(ey[0] ** 2 + ey[1] ** 2 + ey[2] ** 2)

    # Check for a valid expression inside the square root
    if d == 0 or j == 0:
        raise ValueError("Invalid input values for trilateration")

    # Calculate the coordinates of the device
    x = (distance1 ** 2 - distance2 ** 2 + d ** 2) / (2 * d)
    y = (distance1 ** 2 - distance3 ** 2 + i ** 2 + j ** 2) / (2 * j) - (i / j) * x1
    z = math.sqrt(distance1 ** 2 - x ** 2 - y ** 2)

    return x1 + x * ex[0] + y * ey[0], y1 + x * ex[1] + y * ey[1], z1 + x * ex[2] + y * ey[2]



# Function to convert RSSI values to distances
def rssi_to_distance(rssi, calibration_data):
    # Implement your calibration logic here
    # You may use linear regression or other methods
    # to map RSSI values to distances based on calibration data
    # For simplicity, this sample assumes a linear relationship
    # You need to replace this with your actual calibration function
    slope, intercept = calibration_data
    distance = slope * rssi + intercept
    return distance

# Function to calculate device coordinates from 4 RSSI values
def calculate_device_position(rssi_anchor1, rssi_anchor2, rssi_anchor3, rssi_device,
                               calibration_anchor1, calibration_anchor2, calibration_anchor3):
    # Convert RSSI values to distances
    distance_anchor1 = rssi_to_distance(rssi_anchor1, calibration_anchor1)
    distance_anchor2 = rssi_to_distance(rssi_anchor2, calibration_anchor2)
    distance_anchor3 = rssi_to_distance(rssi_anchor3, calibration_anchor3)
    
    # Provide 3D coordinates of anchor points
    anchor1 = (0, 0, 0)
    anchor2 = (5, 0, 0)
    anchor3 = (0, 5, 0)
    
    # Use trilateration to calculate device coordinates
    device_position = trilaterate_3d(anchor1, anchor2, anchor3, distance_anchor1, distance_anchor2, distance_anchor3)
    
    return device_position


if __name__=="__main__":
    # diff_anch_1_2ample usage:
    # Replace with your actual calibration data and RSSI values
    calibration_anchor1 = (0.1, 0.5)  # diff_anch_1_2ample calibration data for anchor 1
    calibration_anchor2 = (0.2, 0.6)  # diff_anch_1_2ample calibration data for anchor 2
    calibration_anchor3 = (0.15, 0.55)  # diff_anch_1_2ample calibration data for anchor 3

    rssi_anchor1 = -60  # diff_anch_1_2ample RSSI value for anchor 1
    rssi_anchor2 = -65  # diff_anch_1_2ample RSSI value for anchor 2
    rssi_anchor3 = -70  # diff_anch_1_2ample RSSI value for anchor 3
    rssi_device = -50  # diff_anch_1_2ample RSSI value for the device being tracked

    # Calculate device position
    device_position = calculate_device_position(rssi_anchor1, rssi_anchor2, rssi_anchor3, rssi_device,
                                                calibration_anchor1, calibration_anchor2, calibration_anchor3)

    print("Device Position:", device_position)

    
    # Call the function with position and anchor data, and save to a file
    # plot_3d_positions(position_data, anchor_points_data, output_file='3d_plot.png')
