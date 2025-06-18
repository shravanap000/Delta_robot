import serial
import time
import threading

# Define COM ports and their corresponding motor IDs
PORTS = {
    'COM11': {'id': 4, 'ser': None},
    'COM12': {'id': 3, 'ser': None},
    'COM15': {'id': 6, 'ser': None}
}
BAUD_RATE = 9600
MIN_POS = 0
MAX_POS = 1023
MIN_ANGLE = -90
MAX_ANGLE = 90

# Calibration data: {motor_id: (slope, intercept)} for position = slope * angle + intercept
CALIBRATION = {
    4: (-3.2778, 500),  # Motor ID 4: 0° = 500, 90° = 205
    3: (-3.0556, 500),  # Motor ID 3: 0° = 500, 90° = 225
    6: (3.3333, 500)    # Motor ID 6: 0° = 500, 90° = 800
}

def initialize_serial_ports():
    """Initialize serial connections for all COM ports."""
    for port in PORTS:
        try:
            PORTS[port]['ser'] = serial.Serial(port, BAUD_RATE, timeout=1)
            time.sleep(3)  # Increased delay for Arduino reset
            PORTS[port]['ser'].flushInput()  # Clear input buffer
            print(f"Connected to {port} for motor ID {PORTS[port]['id']}")
            # Attempt to read initial messages safely
            start_time = time.time()
            while PORTS[port]['ser'].in_waiting and time.time() - start_time < 1:
                raw_data = PORTS[port]['ser'].readline()
                try:
                    line = raw_data.decode('ascii').strip()
                    if line:
                        print(line)
                except UnicodeDecodeError:
                    continue  # Skip non-decodable bytes
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            PORTS[port]['ser'] = None

def angle_to_position(angle, motor_id):
    """Convert angle in degrees to motor position using calibration."""
    slope, intercept = CALIBRATION[motor_id]
    position = slope * angle + intercept
    # Round to integer and clamp to valid range
    position = int(round(position))
    return max(MIN_POS, min(MAX_POS, position))

def validate_angles(angles):
    """Validate that all angles are within the acceptable range."""
    try:
        angles = [float(angle) for angle in angles]
        if len(angles) != 3:
            return False, "Please enter exactly three angles."
        for angle in angles:
            if not (MIN_ANGLE <= angle <= MAX_ANGLE):
                return False, f"Angles must be between {MIN_ANGLE} and {MAX_ANGLE} degrees."
        return True, angles
    except ValueError:
        return False, "Invalid input. Please enter three numbers (e.g., 45.0 -30.0 90.0)."

def send_to_port(port, position):
    """Send position to a single Arduino port."""
    if PORTS[port]['ser'] is not None:
        try:
            # Send position as string followed by newline
            pos_str = f"{position}\n"
            PORTS[port]['ser'].write(pos_str.encode('ascii'))
            print(f"Sent {position} to {port} (Motor ID {PORTS[port]['id']})")
            # Read response
            time.sleep(0.1)  # Small delay to allow response
            while PORTS[port]['ser'].in_waiting:
                raw_data = PORTS[port]['ser'].readline()
                try:
                    line = raw_data.decode('ascii').strip()
                    if line:
                        print(line)
                except UnicodeDecodeError:
                    continue  # Skip non-decodable bytes
        except serial.SerialException as e:
            print(f"Error sending to {port}: {e}")
    else:
        print(f"No connection to {port}. Skipping.")

def send_positions(angles):
    """Send position values to each Arduino in parallel."""
    # Convert angles to positions
    positions = [
        angle_to_position(angles[1], 4),  # COM11 (ID 4)
        angle_to_position(angles[0], 3),  # COM12 (ID 3)
        angle_to_position(angles[2], 6)   # COM15 (ID 6)
    ]
    threads = []
    port_list = ['COM11', 'COM12', 'COM15']
    for i, port in enumerate(port_list):
        thread = threading.Thread(target=send_to_port, args=(port, positions[i]))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def close_serial_ports():
    """Close all serial connections."""
    for port in PORTS:
        if PORTS[port]['ser'] is not None:
            PORTS[port]['ser'].close()
            print(f"Closed connection to {port}")

def main():
    """Main function to get input and control Arduinos."""
    initialize_serial_ports()
    try:
        while True:
            # Get input from user
            user_input = input("Enter three angles (0 to 90) for motors (ID3, ID4, ID6) separated by spaces (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
            
            # Split and validate input
            angles = user_input.strip().split()
            is_valid, result = validate_angles(angles)
            
            if is_valid:
                send_positions(result)
            else:
                print(result)
                continue
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        close_serial_ports()

if __name__ == "__main__":
    main()