import serial 
import time
import serial.tools.list_ports

arduino = None
arduino_connected = False 

def check_arduino_connection():
    global arduino, arduino_connected
    try:
        # Replace 'COM' value with your actual port!
        arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
        time.sleep(2)  # Allow Arduino to initialize
        arduino_connected = True
        print("Arduino connected successfully.")
    except Exception as e:
        print(f"Arduino not connected: {e}")
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p.device)
            
def send_to_arduino(signal):
    global arduino, arduino_connected
    if arduino_connected and arduino is not None:
        try:
            if arduino.is_open:
                # print(f"Sending signal to Arduino: {signal}") # Uncomment to debug
                arduino.write(signal.encode())
        except Exception as e:
            print(f"Warning: Failed to send data to Arduino. {e}")
