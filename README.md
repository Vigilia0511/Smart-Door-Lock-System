# Smart Door Lock System

A comprehensive smart door lock system featuring multiple authentication methods, real-time monitoring, and remote access capabilities.

## Features

###  Multiple Authentication Methods
- **PIN Code**: 4x4 keypad for numeric password entry
- **Fingerprint Recognition**: Biometric authentication using fingerprint sensor
- **Voice Recognition**: Voice command authentication with speech recognition
- **Remote Web Access**: Web-based login interface with IP blocking security

###  Control Interfaces
- **Hardware Interface**: Physical keypad, buttons, and LCD display on Raspberry Pi
- **Web Interface**: Remote control via web browser with live camera feed
- **Mobile App**: Planned mobile application interface (framework ready)

###  Security & Monitoring
- **Access Logging**: Comprehensive logging of all access attempts (granted/denied)
- **Email Notifications**: Automatic email alerts for security events
- **IP Blocking**: Automatic IP blocking after multiple failed login attempts
- **Real-time Notifications**: Live status updates and security alerts

###  Live Monitoring
- **Camera Integration**: Live video feed from Raspberry Pi camera
- **Door Status Control**: Remote lock/unlock functionality
- **System Status Display**: LCD display showing current system state

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Mobile App    │    │   Hardware      │
│   (PHP)         │    │   (Planned)     │    │   (Raspberry Pi)│
│                 │    │                 │    │                 │
│ • Login Portal  │    │ • Remote Access │    │ • Keypad Input  │
│ • Door Control  │    │ • Notifications │    │ • Fingerprint   │
│ • Live View     │    │ • Camera Feed   │    │ • Voice Commands│
│ • Notifications │    │                 │    │ • LCD Display   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │   (MySQL)       │
                    │                 │
                    │ • Access Logs   │
                    │ • Notifications │
                    │ • User Data     │
                    └─────────────────┘
```

## Hardware Requirements

### Raspberry Pi Setup
- Raspberry Pi (any model with GPIO pins)
- 4x4 Matrix Keypad
- Fingerprint Sensor (compatible with PyFingerprint)
- LCD Display (I2C interface)
- Solenoid Lock Mechanism
- Camera Module (Pi Camera)
- Speaker/Microphone for voice features
- Push buttons for various functions

### GPIO Pin Configuration
- **Keypad Rows**: GPIO 18, 25, 8, 7
- **Keypad Columns**: GPIO 5, 27, 17, 4
- **Lock Control**: GPIO 6
- **Control Buttons**: GPIO 23, 24, 25, 26, 16, 20

## Software Components

### 1. Raspberry Pi Controller (`raspberryPythonSC/rei2.py`)
**Core Features:**
- GPIO hardware control
- Multi-modal authentication (PIN, fingerprint, voice)
- Flask web server for API endpoints
- Real-time camera streaming
- LCD status display
- Email notification system
- Text-to-speech responses

**Key Libraries:**
- `RPi.GPIO` - Hardware GPIO control
- `speech_recognition` - Voice input processing
- `gtts` - Text-to-speech output
- `PyFingerprint` - Fingerprint sensor interface
- `RPLCD` - LCD display control
- `picamera2` - Camera functionality
- `Flask` - Web server framework

### 2. Web Application (`smartlockV1SCWebApp/`)
**Files:**
- `index.php` - Login interface with security features
- `interface.php` - Main control dashboard
- `change.php` - Settings/configuration
- `get_notifications.php` - API for fetching notifications
- `new_notifications.php` - API for creating notifications
- `logout.php` - Session management

**Features:**
- Secure login with IP blocking
- Real-time door control
- Live camera streaming
- Notification management
- Responsive web design

### 3. Database (`database/LOCK.sql`)
**Tables:**
- `notifications` - Access logs and system notifications

**Sample Data Includes:**
- PIN access attempts (granted/denied)
- Fingerprint authentication logs
- Voice recognition events
- System status messages
- Security alerts

## Installation & Setup

### Prerequisites
```bash
# Raspberry Pi
sudo apt update
sudo apt install python3-pip python3-rpi.gpio
pip install speechrecognition gtts RPLCD pyfingerprint flask picamera2 opencv-python

# Web Server
- PHP 8.0+
- MySQL/MariaDB
- Apache/Nginx web server
```

### Raspberry Pi Setup
1. Connect all hardware components according to GPIO pin configuration
2. Install required Python libraries
3. Configure email settings for notifications
4. Run the main script: `python3 rei2.py`

### Web Application Setup
1. Deploy PHP files to web server
2. Import database schema from `LOCK.sql`
3. Configure database connection settings
4. Set up ngrok or similar tunneling service for remote access

### Database Setup
```sql
mysql -u root -p < database/LOCK.sql
```

## API Endpoints

### Raspberry Pi Flask Server
- `POST /verify_credentials` - Verify user login
- `GET /camera_feed` - Live camera stream
- `POST /control_lock` - Remote lock control
- `GET /notifications` - Fetch system notifications

### Web Application APIs
- `get_notifications.php` - Retrieve notifications
- `new_notifications.php` - Create new notifications

## Security Features

- **Multi-factor Authentication**: PIN + Biometric options
- **IP Blocking**: Automatic blocking after 3 failed attempts
- **Access Logging**: Complete audit trail of all access attempts
- **Session Management**: Secure PHP sessions with timeout
- **Input Validation**: Sanitized user inputs across all interfaces

## Usage

### Hardware Operation
1. **PIN Access**: Press 'A' on keypad, enter 4-digit code, press 'OK'
2. **Fingerprint**: Press fingerprint button, place finger on sensor
3. **Voice**: Press voice button, speak registered command
4. **Manual Control**: Use physical buttons for direct control

### Web Interface
1. Login with credentials at the web portal
2. View live camera feed
3. Control door lock remotely
4. Monitor access notifications
5. Configure system settings

## Future Enhancements

- **Mobile Application**: Native iOS/Android app development
- **Advanced Analytics**: Access pattern analysis and reporting
- **Integration APIs**: Smart home platform integration (Alexa, Google Home)
- **Cloud Backup**: Secure cloud storage for access logs
- **Advanced Security**: Facial recognition, RFID cards
- **Energy Optimization**: Low-power modes and battery backup

## Troubleshooting

### Common Issues
- **GPIO Permission Denied**: Run with `sudo` or configure GPIO permissions
- **Camera Not Working**: Check camera module connections and enable in raspi-config
- **Fingerprint Sensor**: Ensure proper sensor initialization and finger positioning
- **Voice Recognition**: Check microphone sensitivity and background noise levels

### Logs and Debugging
- Check Raspberry Pi console output for hardware errors
- Review web server logs for API issues
- Monitor database for notification logging
- Use browser developer tools for web interface debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on hardware
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review system logs
- Ensure all hardware connections are secure
- Verify software dependencies are installed correctly

---

**Note**: This system requires physical hardware setup and should be installed by qualified personnel familiar with Raspberry Pi and electronic security systems.