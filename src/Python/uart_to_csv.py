import serial
import csv

# Initialize the serial port (change the port and baud rate as needed)
ser = serial.Serial('/dev/tty.usbmodem103', 115200)  # Replace 'COM1' with your UART port

# Create a list to store the data
uart_data = []

# Function to read data from UART and save it to the list
def read_and_save_uart_data():
    try:
        line_count = 0  # Initialize a variable to count lines
        while True:
            line = ser.readline().decode().strip()
            
            # Increment the line count
            line_count += 1
            
            # Ignore the first eight lines
            if line_count <= 8:
                continue
            
            values = line.split()  # Split the line into individual values
            for value in values:
                try:
                    data = int(value)  # Convert to integers if needed
                    uart_data.append(data)
                except ValueError:
                    pass  # Ignore non-integer values
    except KeyboardInterrupt:
        ser.close()

if __name__ == "__main__":
    read_and_save_uart_data()

    # Save the data as a regular list
    with open('uart_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for data in uart_data:
            csv_writer.writerow([data])

    print("Data has been saved to uart_data.csv.")

