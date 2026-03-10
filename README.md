# 🛡 Cyber Threat Intelligence Dashboard

A cybersecurity web application built using **Python Flask** that analyzes IP addresses and URLs to detect potential cyber threats.
This dashboard simulates a **Security Operations Center (SOC)** style monitoring tool for threat intelligence.

---

# 🚀 Features

### 🔍 IP Threat Intelligence Scanner

* Detects country, ISP, organization
* Calculates **risk score**
* Identifies suspicious IP activity

### 🌐 Malicious URL Scanner

* Integrated with **VirusTotal API**
* Detects:

  * 🚨 Malicious engines
  * ⚠ Suspicious engines
  * ✅ Safe engines

### 📊 Threat Intelligence Dashboard

* Visual statistics
* High risk vs Low risk visualization
* Interactive charts

### 📁 Scan History

* Stores scans in **SQLite database**
* Displays full scan history

### 📥 CSV Report Export

* Download scan history reports

### 👨‍💻 Admin Panel

* View registered users
* Simple user management

### 🔐 Authentication System

* User registration
* Login system
* Session management

### 🎨 Cyber Security UI

* Dark hacker-style dashboard
* Animated UI components

---

# 🧰 Technologies Used

| Technology     | Purpose            |
| -------------- | ------------------ |
| Python         | Backend logic      |
| Flask          | Web framework      |
| SQLite         | Database           |
| HTML           | Frontend structure |
| CSS            | Styling            |
| Chart.js       | Data visualization |
| VirusTotal API | Malware detection  |
| GitHub         | Version control    |

---

# 🏗 Project Architecture

```
User
 │
 │  Scan Request
 ▼
Flask Web Server
 │
 ├── Authentication System
 │
 ├── IP Scanner
 │      │
 │      └── IP API
 │
 ├── URL Scanner
 │      │
 │      └── VirusTotal API
 │
 ├── Database
 │      │
 │      └── SQLite
 │
 └── Dashboard Analytics
        │
        └── Charts & Reports
```

---

# 📂 Project Structure

```
CyberDashboard
│
├── app.py
├── .env
├── .gitignore
├── README.md
│
├── templates
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── url_scan.html
│   ├── url_result.html
│   └── history.html
│
└── static
    ├── style.css
    └── dashboard.css
```

---

# ⚙ Installation

### 1️⃣ Clone Repository

```
git clone https://github.com/ayush00303/cyber-threat-intelligence-dashboard.git
```

### 2️⃣ Install Dependencies

```
pip install flask requests python-dotenv
```

### 3️⃣ Create `.env`

```
VT_API_KEY=your_virustotal_api_key
```

You can get a free API key from:

https://www.virustotal.com/gui/join-us

⚠ **Important:**  
The `.env` file is not included in this repository for security reasons.

---

# ▶ Run Application


### 4️⃣ Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 🔒 Security Note

Sensitive data such as **API keys** are stored using `.env` environment variables and excluded using `.gitignore`.

---

# 📊 Future Improvements

* Real-time cyber threat map
* Dark web breach detection
* AI-based threat prediction
* Live threat intelligence feed
* Malware file scanning

---

# 👨‍💻 Developer

**Ayush Nandavade**

Cybersecurity enthusiast focused on building threat intelligence tools.

GitHub
https://github.com/ayush00303

LinkedIn
https://www.linkedin.com/in/ayush-nandavade-8b6a9a333/

---

# ⭐ If you like this project

Give it a **Star ⭐ on GitHub**
