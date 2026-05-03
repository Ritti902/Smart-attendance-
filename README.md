# 📚 Smart Attendance System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

> An intelligent class attendance system that automates attendance tracking using multiple biometric technologies including Face Recognition, RFID, and biometric verification.

## 🎯 Features

- **Multi-Modal Authentication**
  - 👤 Face Recognition for contactless attendance
  - 📡 RFID card scanning for quick verification
  - 🔐 Biometric authentication support

- **Real-Time Processing**
  - Instant attendance marking
  - Live dashboard updates
  - Immediate notifications

- **Anti-Fraud Protection**
  - Proxy prevention mechanisms
  - Duplicate entry detection
  - Audit trail logging

- **Efficient Management**
  - Reduced manual workload
  - Automated report generation
  - Secure data storage

- **Data Security**
  - Encrypted data storage
  - Role-based access control
  - GDPR-compliant privacy measures

## 📋 Table of Contents

- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Contact](#-contact)

## 📦 Requirements

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB for installation and dependencies

### Hardware Requirements (Optional)
- RFID Card Reader/Writer
- Biometric Scanner
- Webcam (for face recognition)
- Network connectivity

### Python Dependencies
See `requirements.txt` for the complete list of packages.

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Ritti902/Smart-attendance-.git
cd Smart-attendance-
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure the System
```bash
cp config.example.json config.json
# Edit config.json with your settings
```

### Step 5: Initialize Database
```bash
python setup_database.py
```

### Step 6: Run the Application
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## ⚙️ Configuration

Create a `config.json` file in the root directory:

```json
{
  "app": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "secret_key": "your-secret-key-here"
  },
  "database": {
    "type": "sqlite",
    "path": "data/attendance.db"
  },
  "face_recognition": {
    "enabled": true,
    "model": "cnn",
    "tolerance": 0.6
  },
  "rfid": {
    "enabled": true,
    "port": "COM3",
    "baud_rate": 9600
  },
  "biometric": {
    "enabled": false,
    "device_id": ""
  },
  "security": {
    "encryption": true,
    "log_attendance": true
  }
}
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `app.debug` | Boolean | Enable debug mode for development |
| `face_recognition.tolerance` | Float | Face match tolerance (0.0-1.0, lower = stricter) |
| `rfid.port` | String | Serial port for RFID reader |
| `security.encryption` | Boolean | Enable data encryption |

## 💻 Usage

### Starting the Application

```bash
python main.py
```

### Web Interface

1. Open `http://localhost:5000` in your browser
2. Log in with admin credentials
3. Navigate to the dashboard

### Key Features

#### Marking Attendance
- **Face Recognition**: Look at the camera for 2-3 seconds
- **RFID**: Scan your card on the reader
- **Manual Entry**: Admin can manually add attendance

#### Viewing Reports
```bash
# Generate daily report
python scripts/generate_report.py --date 2026-05-03

# Generate attendance for specific student
python scripts/generate_report.py --student-id STU001
```

#### Exporting Data
```bash
# Export to CSV
python scripts/export_data.py --format csv --output attendance.csv

# Export to Excel
python scripts/export_data.py --format excel --output attendance.xlsx
```

## 📁 Project Structure

```
Smart-attendance-/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   ├── auth/                # Authentication logic
│   └── templates/           # HTML templates
├── recognition/
│   ├── face_recognition.py  # Face recognition module
│   ├── rfid_reader.py       # RFID module
│   └── biometric.py         # Biometric module
├── database/
│   ├── schema.sql           # Database schema
│   └── migrations/          # Database migrations
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── setup_database.py        # Database initialization
└── README.md               # This file
```

## 🔌 API Documentation

### Authentication
All API requests require a valid JWT token in the `Authorization` header.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/attendance
```

### Endpoints

#### Get Attendance Records
```
GET /api/attendance
Query Parameters:
  - date: YYYY-MM-DD
  - student_id: string
  - limit: number (default: 100)
```

#### Mark Attendance
```
POST /api/attendance/mark
Body:
{
  "student_id": "STU001",
  "method": "face_recognition|rfid|manual",
  "timestamp": "2026-05-03T10:30:00Z"
}
```

#### Get Student List
```
GET /api/students
Query Parameters:
  - class_id: string
  - limit: number
```

#### Generate Report
```
GET /api/reports/attendance?date=2026-05-03&class_id=CLASS01
```

## 🛠 Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLite/PostgreSQL
- **Face Recognition**: OpenCV, face_recognition library
- **Frontend**: HTML5, CSS3, JavaScript
- **RFID**: pyserial
- **Authentication**: JWT
- **Data Encryption**: cryptography library

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Write docstrings for functions
- Include unit tests for new features

## 🐛 Troubleshooting

### Face Recognition Not Working
- Ensure webcam is connected and accessible
- Check lighting conditions (good lighting needed)
- Increase `tolerance` value in config.json
- Verify face_recognition library is installed: `pip install face_recognition`

### RFID Reader Not Detected
- Check USB connection and driver installation
- Verify COM port in config.json
- Test connection: `python -m serial.tools.list_ports`
- Try different baud rates

### Database Connection Issues
- Ensure database file path is correct in config.json
- Check file permissions in the data directory
- Run `python setup_database.py` to reinitialize

### Performance Issues
- Reduce camera resolution
- Increase face recognition tolerance
- Limit database queries with proper indexing
- Monitor RAM usage and close unused applications

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Author**: Ritti902
- **Repository**: [GitHub](https://github.com/Ritti902/Smart-attendance-)
- **Issues**: [Report a Bug](https://github.com/Ritti902/Smart-attendance-/issues)
- **Email**: [Your Email]

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with [face_recognition](https://github.com/ageitgey/face_recognition)
- Inspired by modern attendance management systems

---

**Last Updated**: May 3, 2026

For more information and updates, visit the [GitHub repository](https://github.com/Ritti902/Smart-attendance-).
