# 🔥 BREACH — Email Breach Checker (LeakCheck Public API)

`breach.py` is a neon-styled, animated terminal tool that checks if an email appears in public data breaches using the **LeakCheck.io Public API**.  
→ No API key required  
→ Free to use  
→ Works on Linux, macOS, Windows (Git Bash)

Built by **xycaerys**.

---

## ⚡ Features
- 🔥 Neon glitch ASCII banner  
- ⚡ Typing animation  
- 📨 Email breach lookup using LeakCheck Public API  
- 🧩 JSON output mode  
- 🎨 Colorful formatted terminal output  
- 🖥 Cross-platform support  

---

## 🔧 Requirements

Add this to `requirements.txt`:

requests  
colorama   # optional for Windows CMD

Install:

```bash
pip install -r requirements.txt

## ▶️ Usage

### ▶️ Basic Usage
python breach.py someone@example.com

### ▶️ Interactive Mode (no email passed)
python breach.py

Tool will ask:
[?] Enter email to check:

### ▶️ JSON Output
python breach.py someone@example.com --json

---

## ⚙️ How It Works

BREACH sends a GET request to:
https://leakcheck.io/api/public?check=<email>

Example response:
{
  "success": true,
  "found": 3,
  "fields": ["username", "address", "password"],
  "sources": [
      {"name": "Evony.com", "date": "2016-07"},
      {"name": "LinkedIn", "date": "2012"}
  ]
}

BREACH displays:
- Breach count
- Exposed data fields
- Leak source names
- Leak dates

## 👨‍💻 Author

Made by **xycaerys**  
Powered by **LeakCheck.io**  
Built with ❤️ using **Python**

GitHub: https://github.com/xycaerys

If you enjoy this tool, feel free to ⭐ the repository!
