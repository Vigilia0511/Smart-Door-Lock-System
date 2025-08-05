import RPi.GPIO as GPIO
from time import sleep
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
from RPLCD.i2c import CharLCD
from pyfingerprint.pyfingerprint import PyFingerprint
import threading
from datetime import datetime
from flask import Flask, request, jsonify
import logging
from flask import Flask, Response
from picamera2 import Picamera2
import cv2
from datetime import datetime
import time
import requests
import os
import ssl
import logging
import threading
from typing import Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re




# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)


# Define the GPIO pins for rows, columns, and button
ROW_PINS = [18, 25, 8, 7]
COL_PINS = [5, 27, 17, 4]

BUTTON_PIN = 20  # Replace with the GPIO pin for the button

# Define GPIO pin for the solenoid lock
LOCK_PIN = 6  # Replace with your solenoid lock GPIO pin

# Keypad layout
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'OK']
]

# Set the correct password
PASSWORD = "1234"

def setup():
    # Set up GPIO mode
    GPIO.setmode(GPIO.BCM)
    
    # Set up rows as output and columns as input
    for row in ROW_PINS:
        GPIO.setup(row, GPIO.OUT)
        GPIO.output(row, GPIO.LOW)
    
    for col in COL_PINS:
        GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # Set up the solenoid lock pin as output
    GPIO.setup(LOCK_PIN, GPIO.OUT)
    GPIO.output(LOCK_PIN, GPIO.LOW)  # Ensure the lock is initially closed

    # Set up the button pin as input
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_keypad():
    for row_index, row_pin in enumerate(ROW_PINS):
        # Set the current row HIGH
        GPIO.output(row_pin, GPIO.HIGH)
        for col_index, col_pin in enumerate(COL_PINS):
            if GPIO.input(col_pin) == GPIO.HIGH:
                # Debounce the key press
                time.sleep(0.02)  # Short delay
                if GPIO.input(col_pin) == GPIO.HIGH:
                    key = KEYPAD[row_index][col_index]
                    # Wait for the key to be released
                    while GPIO.input(col_pin) == GPIO.HIGH:
                        pass
                    return key
        # Set the current row LOW
        GPIO.output(row_pin, GPIO.LOW)
    return None
    return input("Simulate Key Press: ").strip()  # Simulate user input

def open_lock():
    """Opens the lock for a specific duration."""
    print("Unlocking door...")
    GPIO.output(LOCK_PIN, GPIO.HIGH)  # Activate solenoid
    time.sleep(5)  # Keep the lock open for 5 seconds
    GPIO.output(LOCK_PIN, GPIO.LOW)  # Deactivate solenoid
    print("Door locked again.")

def keypad_mode():
    """Handles the keypad password input logic."""
    print("Keypad mode activated. Press 'A' to begin password entry.")
    entered_password = ""  # Initialize the password buffer
    a_pressed = False  # Flag to check if "A" is pressed before accepting the password
    a_pressed_time = 0  # Variable to store the time when "A" is pressed

def update_lcd_display(line1, line2=""):
    """
    Update the LCD display with two lines of text.
    """
    lcd.clear()
    lcd.write_string(line1[:16])  # First line
    if line2:
        lcd.cursor_pos = (1, 0)  # Move to the second line
        lcd.write_string(line2[:16])  # Second line

# Notification state management
class NotificationState:
    def __init__(self):
        self.current_notification = "System ready"
        self.lock = threading.Lock()
        self.notifications = []  # Store access denial notifications

state = NotificationState()

# Initialize the LCD
lcd = CharLCD('PCF8574', 0x27)

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pin Definitions
PINS = {
    'button1': 23,  # Record unlock command
    'button2': 24,  # Verify voice command
    'button3': 25,  # Stop listening
    'button4': 26,  # Fingerprint verification
    'button5': 16,  # Register fingerprint
    'solenoid': 6,
    'buzzer': 22,
    'button6' : 0
    }

# Setup GPIO pins
for pin in PINS.values():
    if pin in [PINS['solenoid'], PINS['buzzer']]:
        GPIO.setup(pin, GPIO.OUT)
    else:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize fingerprint sensor
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is incorrect!')
except Exception as e:
    logger.error(f'Fingerprint sensor initialization failed: {str(e)}')
    exit(1)

def update_notification(message, access_denied=False):
    """Update the current notification with timestamp."""
    with state.lock:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.current_notification = f"{message}   --------   {current_time}"
        if access_denied:
            state.notifications.append(state.current_notification)
        logger.info(f"Updated notification: {state.current_notification}")



picam2 = Picamera2()
picam2.configure(picam2.preview_configuration)  # Set up camera
picam2.start()

class UserManager:
    def __init__(self, passwords_file_path):
        """
        Initialize the UserManager with a file path for passwords
        
        Args:
            passwords_file_path (str): Path to the passwords file
        """
        self.passwords_file_path = "/tmp/passwords.txt"
        self.hardcoded_ids = {"051123", "coleen"}  # Hardcoded IDs
        self.passwords = self.load_passwords()
    
    def load_passwords(self):
        """
        Load passwords from the specified file
        
        Returns:
            dict: Dictionary of user IDs and their passwords
        """
        passwords = {}
        if os.path.exists(self.passwords_file_path):  # Corrected here
            with open(self.passwords_file_path, "r") as file:
                for line in file:
                    user_id, password = line.strip().split("=")
                    passwords[user_id] = password
        else:
            logging.warning(f"Passwords file not found: {self.passwords_file_path}")
        
        return passwords


    def verify_password(self, user_id, password):
        """
        Verify user password
        
        Args:
            user_id (str): User identifier
            password (str): User password
        
        Returns:
            dict: Authentication result
        """
        # Check if user ID is hardcoded
        if user_id not in self.hardcoded_ids:
            return {
                "status": "error",
                "message": "User ID not found"
            }
        
        # Verify password
        if self.passwords.get(user_id) == password:
            return {
                "status": "success",
                "message": "Authentication successful"
            }
        
        return {
            "status": "error",
            "message": "Invalid password"
        }

# Initialize UserManager with the file path to the passwords file
PASSWORDS_FILE_PATH = "/tpm/passwords.txt"  # Replace with the actual file path
user_manager = UserManager(PASSWORDS_FILE_PATH)

@app.route('/verify_credentials', methods=['POST'])
def verify_password():
    global current_recipient_email
    """
    Verify user password and authenticate
    """
    try:
        user_id = request.form.get("id")
        password = request.form.get("password")
        recipient_email = request.form.get("recipient_email")
        
        if not all([user_id, password]):
            return jsonify({
                "status": "error", 
                "message": "ID and password must be provided"
            }), 400
        
        result = user_manager.verify_password(user_id, password)
        
        # Validate email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, recipient_email):
            return jsonify({"status": "error", "message": "Invalid recipient email format"}), 401
        
        if result["status"] == "success":
            current_recipient_email = recipient_email
            save_recipient_email(current_recipient_email)  # Save email for later use
            logging.info(f"User {user_id} authenticated successfully")
            return jsonify(result), 200
        else:
            logging.warning(f"Authentication failed for user {user_id}")
            return jsonify(result), 402
    
    except Exception as e:
        logging.error(f"Verification error: {e}")
        return jsonify({
            "status": "error", 
            "message": "Verification failed"
        }), 500

@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Allows a user to change their password permanently.
    """
    try:
        user_id = request.form.get("id")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        
        # Check if user ID and current password and new password are provided
        if user_id is None or current_password is None or new_password is None:
            return jsonify({"status": "error", "message": "ID, current password, and new password must be provided"}), 400
        
        # Check if new password is blank
        if not new_password.strip():
            return jsonify({"status": "error", "message": "New password cannot be blank"}), 401
        
        # Check if user ID and current password are correct
        if user_manager.passwords.get(user_id) == current_password:
            # Update password in memory
            user_manager.passwords[user_id] = new_password
            # Persist changes to the file
            with open(user_manager.passwords_file_path, "w") as file:
                for uid, pwd in user_manager.passwords.items():
                    file.write(f"{uid}={pwd}\n")
            logging.info(f"Password updated successfully for user {user_id}.")
            return jsonify({"status": "success", "message": "Password changed successfully"}), 200
        else:
            logging.warning(f"Password change failed for user {user_id}: Incorrect current password.")
            return jsonify({"status": "error", "message": "Invalid ID or current password"}), 402
    except Exception as e:
        logging.error(f"Error during password change: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def generate():
    while True:
        # Capture frame from PiCamera2
        frame = picam2.capture_array()
        # Convert the frame to JPEG format for streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break
        # Yield frame as a byte stream for HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return 'Video Stream Running!'

# Configure logging
logging.basicConfig(level=logging.INFO)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable for recipient email
current_recipient_email = None

# Function to save the recipient email to a file
def save_recipient_email(email):
    """Save the recipient email to a file."""
    try:
        with open("recipient_email.txt", "w") as file:
            file.write(email)
        logger.info("Recipient email saved successfully.")
    except Exception as e:
        logger.error(f"Error saving recipient email: {str(e)}")

# Function to load the recipient email from a file
def load_recipient_email():
    """Load the recipient email from a file."""
    try:
        if os.path.exists("recipient_email.txt"):
            with open("recipient_email.txt", "r") as file:
                return file.read().strip()
        else:
            logger.warning("No recipient email found.")
            return None
    except Exception as e:
        logger.error(f"Error loading recipient email: {str(e)}")
        return None


@app.route('/get_recipient_email', methods=['GET'])
def get_recipient_email():
    """Retrieve the saved recipient email."""
    global current_recipient_email

    # Load the recipient email if not already loaded
    if current_recipient_email is None:
        current_recipient_email = load_recipient_email()

    if current_recipient_email:
        return jsonify({"status": "success", "recipient_email": current_recipient_email}), 200
    else:
        return jsonify({"status": "error", "message": "No recipient email found"}), 404

def send_email_with_attachment(sender_email, app_password, recipient_email, subject, body, image_path=None):
    """
    Send an email with an optional attachment using a simple, robust method.
    
    Args:
        sender_email (str): Sender's email address
        app_password (str): App password for authentication
        recipient_email (str): Recipient's email address
        subject (str): Email subject
        body (str): Email body text
        image_path (str, optional): Path to image to be attached
    """
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach body text
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach image if exists
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= intruder_capture.jpg")
                msg.attach(part)
            except Exception as attach_error:
                logging.error(f"Error attaching image: {attach_error}")
        
        # Attempt to send email with multiple connection strategies
        for port in [587, 465]:  # Try both TLS and SSL ports
            try:
                if port == 587:
                    # TLS connection
                    with smtplib.SMTP('smtp.gmail.com', port, timeout=10) as server:
                        server.ehlo()
                        server.starttls(context=context)
                        server.login(sender_email, app_password)
                        server.send_message(msg)
                else:
                    # SSL connection
                    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context, timeout=10) as server:
                        server.login(sender_email, app_password)
                        server.send_message(msg)
                
                logging.info(f"Email sent successfully via port {port}")
                return True
            
            except Exception as conn_error:
                logging.warning(f"Email send attempt via port {port} failed: {conn_error}")
        
        # If all attempts fail
        raise Exception("All email sending attempts failed")
    
    except Exception as e:
        logging.error(f"Final email sending error: {str(e)}")
        return False

def threaded_email_send(sender_email, app_password, recipient_email, subject, body, image_path=None):
    """
    Send email in a separate thread to prevent blocking
    """
    email_thread = threading.Thread(
        target=send_email_with_attachment,
        args=(
            sender_email, 
            app_password, 
            recipient_email, 
            subject, 
            body, 
            image_path
        )
    )
    email_thread.start()

def capture_and_email_intruder_image():
    """
    Capture an image from the PiCamera and send it via email.
    
    Returns:
        bool: True if email task was initiated successfully
    """
    try:
        # Capture an image
        picam2.capture_config = picam2.create_still_configuration()
        picam2.switch_mode(picam2.capture_config)
        
        # Take the photo
        image_path = "/tmp/intruder_capture.jpg"
        picam2.capture_file(image_path)
        
        # Email details
        sender_email = "joshuacajimatvigilia@gmail.com"
        app_password = "utfo zekm yket vxsa"  # Consider using environment variables
        
        # Load the saved recipient email
        current_recipient_email = load_recipient_email()
        
        # Validate recipient email
        if not current_recipient_email:
            logging.error("No recipient email available. Ensure the recipient email is saved.")
            return False
        
        logging.info(f"Sending email to: {current_recipient_email}")
        
        # Initiate email sending
        threaded_email_send(
            sender_email, 
            app_password, 
            current_recipient_email, 
            "Intruder Alert: Multiple Failed Access Attempts",
            "Multiple failed access attempts detected. An image of the potential intruder is attached.",
            image_path
        )
        
        return True
    
    except Exception as e:
        logging.error(f"Error in capture and email process: {str(e)}")
        return False

    
    
@app.route('/get_notification', methods=['GET'])
def get_notification():
    """Endpoint to get current notification and handle alert status based on buzzer activation."""
    global buzzer_activated

    try:
        with state.lock:
            # Retrieve the current notification from state
            notification = state.current_notification

            # Check if the buzzer is activated, indicating an alert
            if buzzer_activated:
                # Override notification for an alert and start 10-second reset timer
                notification = "Three failed attempts detected!"
                threading.Timer(10, reset_buzzer_status).start()
                status = "alert"
            else:
                status = "success"

        return jsonify({
            "status": status,
            "notification": notification,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error getting notification: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

def reset_buzzer_status():
    """Reset the buzzer activated status after a delay."""
    global buzzer_activated
    with state.lock:
        buzzer_activated = False  # Reset to normal after 10 seconds
@app.route('/control_solenoid', methods=['POST'])
def control_solenoid():
    try:
        # Try to get form data
        if request.form:
            switch_state = request.form.get("switch")
        else:
            # If form data is not present, return an error
            return jsonify({"status": "error", "message": "No form data provided"}), 400

        if switch_state == "on":
            # Activate solenoid
            GPIO.output(PINS['solenoid'], GPIO.HIGH)
            return jsonify({"status": "success", "message": "Solenoid activated"}), 200
        elif switch_state == "off":
            # Deactivate solenoid
            GPIO.output(PINS['solenoid'], GPIO.LOW)
            return jsonify({"status": "success", "message": "Solenoid deactivated"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid switch state"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def speak(message):
    """Text-to-speech function."""
    try:
        tts = gTTS(text=message, lang='en')
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
            tts.save(fp.name)
            os.system(f"mpg321 {fp.name}")
    except Exception as e:
        logger.error(f"Speech error: {str(e)}")

# Function to save the registered voice command
def save_voice_command(command):
    """Save the registered voice command to a file."""
    try:
        with open("voice_command.txt", "w") as file:
            file.write(command)
        logger.info("Voice command saved successfully.")
    except Exception as e:
        logger.error(f"Error saving voice command: {str(e)}")

# Function to load the saved voice command
def load_voice_command():
    """Load the registered voice command from a file."""
    try:
        if os.path.exists("voice_command.txt"):
            with open("voice_command.txt", "r") as file:
                return file.read().strip()
        else:
            logger.warning("No registered voice command found.")
            return None
    except Exception as e:
        logger.error(f"Error loading voice command: {str(e)}")
        return None

# Function to display a message on the LCD in a continuous loop with scrolling effect
def display_message(message, stop_event):
    max_length = 16  # 16 characters for a 2x16 LCD

    # Ensure the message fits within the display
    if len(message) <= max_length:
        lcd.clear()
        lcd.write_string(message)
        sleep(2)
        return

    # Prepare to scroll the message
    message = message + "  "  # Add space for scrolling effect
    scroll_length = len(message)

    # Loop to display the message continuously
    while not stop_event.is_set():  # Check the stop event
        for i in range(scroll_length - max_length + 1):
            if stop_event.is_set():  # Check if we should stop
                break
            lcd.clear()
            lcd.write_string(message[i:i + max_length])
            sleep(0.5)  # Adjust the scroll speed as needed

def listen_for_command():
    """Listen for voice command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Listening for voice command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            logger.info(f"Voice command detected: {command}")
            return command
        except sr.UnknownValueError:
            logger.warning("Could not understand the audio")
            return None
        except sr.RequestError:
            logger.error("Could not request results; check internet connection")
            return None

# Add a global flag for buzzer activation
buzzer_activated = False

def sound_buzzer(duration=10):
    """Sound the buzzer for specified duration and set buzzer_activated to True."""
    global buzzer_activated
    buzzer_activated = True  # Set flag when buzzer is activated
    GPIO.output(PINS['buzzer'], GPIO.HIGH)
    sleep(duration)
    GPIO.output(PINS['buzzer'], GPIO.LOW)

# Function to handle fingerprint registration (enrollment)
def enroll_fingerprint():
    try:
        print('Waiting for finger for enrollment...')
        speak("Please place your finger on the sensor.")
        
        for _ in range(5):  # Max 5 attempts
            while not f.readImage():
                sleep(1)  # Delay for easier finger placement
                print("Place your finger on the sensor...")
            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]

            if positionNumber >= 0:
                print(f'Template already exists at position #{positionNumber}')
                speak('Fingerprint already registered.')
                return False

            print('Remove your finger.')
            speak('Remove your finger.')
            sleep(2)

            print('Place the same finger again...')
            speak('Place the same finger again.')

            for _ in range(5):  # Max 5 attempts
                while not f.readImage():
                    sleep(1)  # Delay for easier finger placement
                    print("Place your finger on the sensor...")
                f.convertImage(0x02)
                
                if f.compareCharacteristics() == 0:
                    raise Exception('Fingers do not match.')

                f.createTemplate()
                positionNumber = f.storeTemplate()
                print(f'Finger enrolled successfully at position #{positionNumber}')
                speak(f'Finger enrolled successfully at position {positionNumber}')
                return True
    except Exception as e:
        print('Error enrolling fingerprint!')
        print('Exception message: ' + str(e))
        speak('Error enrolling fingerprint.')
        return False

# Function to handle fingerprint verification
def verify_fingerprint():
    try:
        print('Waiting for finger...')
        while not f.readImage():
            sleep(0.5)
            print("Place your finger on the sensor...")

        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            print(f'Fingerprint recognized at position #{positionNumber}')
            return True
        else:
            print('Fingerprint not recognized.')
            return False
    except Exception as e:
        print('Error verifying fingerprint!')
        print('Exception message: ' + str(e))
        return False

# Update the main loop to include saving and verifying the voice command
def main_loop():
    """Main program loop."""
    stop_event = threading.Event()
    voice_fail_count = 0
    fingerprint_fail_count = 0
    pin_fail_count = 0
    total_fail_count = 0
    


    # Initialize global variables
    global a_pressed, a_pressed_time
    a_pressed = False  # Flag for "A" press
    a_pressed_time = 0  # Time when "A" was pressed
    entered_password = ""  # Buffer for password input

    while True:
        # Check keypad
        key = read_keypad()
        if key:  # Check if a key is pressed
            if key == "A" and not a_pressed:
                message = "Hello, enter your PIN."
                speak(message)
            if a_pressed:
                if key == "OK":
                    # Check if the entered password matches
                    if entered_password == PASSWORD:
                        message = "Access granted!, Welcome!"
                        speak(message)
                        print("Access granted!")
                        update_lcd_display("Access granted!", "Welcome!")
                        open_lock()
                        update_notification("PIN access granted")
                        pin_fail_count = 0
                    else:
                        message = "Incorrect PIN!,Try again."
                        speak(message)
                        print("Incorrect PIN.")
                        update_lcd_display("Incorrect PIN!", "Try again.")
                        entered_password = ""  # Reset after checking
                        a_pressed = False
                        pin_fail_count += 1
                        update_notification("PIN access denied", True)
                        total_fail_count = voice_fail_count + fingerprint_fail_count + pin_fail_count
                        if total_fail_count >= 3:
                            sound_buzzer()
                            capture_and_email_intruder_image()
                        
                elif key == "*":
                    message = "Password cleared"
                    speak(message)
                    # Clear the entered password
                    entered_password = ""
                    print("Password cleared.")
                    update_lcd_display("PIN Cleared!", "")
                else:
                    # Append the key to the entered password
                    entered_password += key
                    print(f"Password so far: {entered_password}")
                    # Display the PIN on the LCD as it's being entered
                    update_lcd_display("Enter PIN:", "*" * len(entered_password))
            else:
                if key == "A":
                    # Activate PIN entry mode
                    a_pressed = True
                    entered_password = ""  # Reset PIN entry
                    print("A pressed. Enter your PIN.")
                    update_lcd_display("Enter your PIN", "")                                                                                                                                                                

        # Button 1: Register voice command
        if GPIO.input(PINS['button1']) == GPIO.LOW:
            message = "Hello, please register your voice password."
            speak(message)
            stop_event.clear()
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()

            recorded_command = listen_for_command()
            if recorded_command:
                save_voice_command(recorded_command)  # Save the registered voice command
                stop_event.set()
                speak("Voice registered.")
                message = "Voice registered."
                update_notification("Voice registered")
                voice_fail_count = 0
            else:
                update_notification("Voice registration failed", True)
                stop_event.set()
                speak("Voice not clear, try again.")
                message = "Repeat and try again."

            stop_event.clear()
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()


        # Button 2: Voice verification
        if GPIO.input(PINS['button2']) == GPIO.LOW:
            message = "Listening for voice verification."
            speak(message)
            stop_event.clear()
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()

            registered_command = load_voice_command()  # Load the saved voice command
            if not registered_command:
                stop_event.set()
                speak("No voice command registered.")
                message = "No voice command registered."
                stop_event.clear()
                display_thread = threading.Thread(target=display_message, args=(message, stop_event))
                display_thread.start()
                continue

            command = listen_for_command()
            if command == registered_command:
                stop_event.set()
                speak("Access granted.")
                message = "Access granted."
                update_notification("Voice access granted")
                GPIO.output(PINS['solenoid'], GPIO.HIGH)
                sleep(5)
                GPIO.output(PINS['solenoid'], GPIO.LOW)
                voice_fail_count = 0
            else:
                stop_event.set()  # Stop the display
                speak("Access denied.")
                message = "Access denied."
                stop_event.clear()
                display_thread = threading.Thread(target=display_message, args=(message, stop_event))
                display_thread.start()
                voice_fail_count += 1
                update_notification("Voice access denied", True)
                total_fail_count = voice_fail_count + fingerprint_fail_count + pin_fail_count
                if total_fail_count >= 3:
                    sound_buzzer()
                    capture_and_email_intruder_image()

            stop_event.clear()
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()

        sleep(0.1)  # Prevent CPU overuse

        # Button 4: Fingerprint verification
        if GPIO.input(PINS['button4']) == GPIO.LOW:
            message = "Please place your finger on the sensor."
            speak(message)
            stop_event.clear()  # Clear any previous stop event
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()  # Start displaying message in a separate thread

            if verify_fingerprint():
                stop_event.set()  # Stop the display
                speak("Fingerprint recognized. Access granted.")
                message = "Access granted."
                stop_event.clear()
                display_thread = threading.Thread(target=display_message, args=(message, stop_event))
                display_thread.start()
                update_notification("Fingerprint access granted")
                GPIO.output(PINS['solenoid'], GPIO.HIGH)
                sleep(5)
                GPIO.output(PINS['solenoid'], GPIO.LOW)
                fingerprint_fail_count = 0
            else:
                stop_event.set()  # Stop the display
                speak("Fingerprint not recognized. access denied")
                message = "Access denied."
                stop_event.clear()
                display_thread = threading.Thread(target=display_message, args=(message, stop_event))
                display_thread.start()
                fingerprint_fail_count += 1
                update_notification("Fingerprint access denied", True)
                total_fail_count = voice_fail_count + fingerprint_fail_count + pin_fail_count
                if total_fail_count >= 3:
                    sound_buzzer()
                    capture_and_email_intruder_image()

        # Button 5: Enroll fingerprint
        if GPIO.input(PINS['button5']) == GPIO.LOW:
            message = "Place your finger for enrollment."
            speak(message)
            stop_event.clear()  # Clear any previous stop event
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()  # Start displaying message in a separate thread
            
            if enroll_fingerprint():
                stop_event.set()  # Stop the display
                speak("Fingerprint enrolled successfully.")
                message = "Enroll successful"
                update_notification("Fingerprint enrolled successfully")
            else:
                update_notification("Fingerprint enrollment failed", True)
                stop_event.set()  # Stop the display
                speak("Fingerprint enrollment failed.")
                message = "Enroll failed."

            stop_event.clear()
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()
            stop_event.set()  # Stop the display

        sleep(0.1)  # Prevent CPU overuse
        # Button 6: Open the lock
        if GPIO.input(PINS['button6']) == GPIO.LOW:
            message = "Lock is open."
            speak(message)
            stop_event.clear()
            display_thread = threading.Thread(target=display_message, args=(message, stop_event))
            display_thread.start()
            open_lock()


if __name__ == '__main__':
    try:
        setup()  # Ensure GPIO is set up before starting other components
        # Start Flask server in a separate thread
        server_thread = threading.Thread(
            target=lambda: app.run(host='0.0.0.0', port=5000, debug=False),
            daemon=True
        )
        server_thread.start()

        # Start main loop
        main_loop()

    except KeyboardInterrupt:
        GPIO.cleanup()
        logger.info("Program terminated.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        GPIO.cleanup()



