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
                    line = raw_data.decode('ascii').strip()  # Use ASCII to avoid UTF-8 issues
                    if line:
                        print(line)
                except UnicodeDecodeError:
                    continue  # Skip non-decodable bytes
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            PORTS[port]['ser'] = None

def validate_positions(positions):
    """Validate that all positions are within the acceptable range."""
    try:
        positions = [int(pos) for pos in positions]
        if len(positions) != 3:
            return False, "Please enter exactly three numbers."
        for pos in positions:
            if not (MIN_POS <= pos <= MAX_POS):
                return False, f"Positions must be between {MIN_POS} and {MAX_POS}."
        return True, positions
    except ValueError:
        return False, "Invalid input. Please enter three integers."

def send_to_port(port, position):
    """Send position to a single Arduino port."""
    if PORTS[port]['ser'] is not None:
        try:
            # Send position as string followed by newline
            pos_str = f"{position}\n"
            PORTS[port]['ser'].write(pos_str.encode('ascii'))  # Use ASCII encoding
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

def send_positions(positions):
    """Send position values to each Arduino in parallel."""
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
            user_input = input("Enter three positions (0-1023) for motors (ID3, ID4, ID6) separated by spaces (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
            
            # Split and validate input
            positions = user_input.strip().split()
            is_valid, result = validate_positions(positions)
            
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