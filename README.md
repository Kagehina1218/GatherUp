# GatherUp  
An AI-Powered Smart Scheduling and Availability Sharing Platform

GatherUp is a web application designed to simplify group scheduling through intelligent automation, real-time availability sharing, AI-driven recommendations, and voice-based input. Instead of relying on cluttered group chats or repetitive manual updates, GatherUp provides a clean, structured, and automated experience for staying organized and connected.

---

## 🚀 Features

### ✔ User Account System  
- Create personal profiles  
- Add friends, coworkers, or contacts  
- Control who can view parts of your schedule  

### ✔ Personalized Schedule Sharing  
- Selectively share specific events or time blocks  
- Maintain privacy and visibility control  

### ✔ Real-Time Availability Dashboard  
- View schedules with a clean visual interface  
- Automatic updates when events are added or changed  

### ✔ AI-Powered Recommendations (Gemini Integration)  
- Suggests optimal meeting times  
- Recommends group activities based on overlapping availability  
- Supports better time-management habits  

### ✔ Voice Input (NLP)  
- Uses Google Speech-to-Text API  
- Create events or set availability using your voice  

### ✔ Email Notifications  
- Get notified when friends update availability  
- Alerts sent when AI detects a good time for group activities  

---

## 🧰 Technology Stack

### **Frontend**
- HTML  
- CSS  

### **Backend**
- Flask  
- TinyDB (NoSQL database)

### **AI / NLP**
- Google Gemini API  
- Google Speech-to-Text API, Text-to-Speech API  

### **Notifications**
- Flask-Mail / Flask-Email  

### **Tools**
- VSCode  
- GitHub  

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kagehina1218/GatherUp.git
cd GatherUp/my-flask-app


## 2️⃣ Install Dependencies

Install all required libraries:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask tinydb google-generativeai speechrecognition pyaudio flask-mail
```

---

## 3️⃣ Create a `.env` file

Inside the `my-flask-app` folder, create a file named `.env`:

```
API_KEY="YOUR_GEMINI_API_KEY"
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME="your_email@gmail.com"
MAIL_PASSWORD="your_app_password"
```

---

## 4️⃣ Run the Flask Application

```bash
python app.py
```

Your app will run at:

👉 http://127.0.0.1:5000/

---

# 👨‍💻 Contributors

| Name | Role |
|------|------|
| **Balkarandeep Singh** | Backend, TinyDB, NLP + Speech-to-Text integration, notification |
| **Meien “Grace” Li** | AI Gemini integration, schedule logic, frontend, Agentic AI Integration |
| **Meera Bhaskarbhai Vyas** | UI/UX, user account pages, website design, feature edit, documentation |

---

# 📌 Project Status

| Feature | Status |
|---------|--------|
| Website Setup | ✅ Done |
| Gemini AI Integration | ✅ Done |
| Voice Input via NLP | ✅ Done |
| Email Notification System | ✅ Done |
| Schedule Recommendations | ✅ Done |
| Deployment | ⏳ Planned |

---

# 🧪 Testing & Debugging

- Workflow verification  
- Unit testing on scheduling + notifications  
- Exception handling for AI + STT  
- 50+ Git commits  
- Manual testing of UI/UX across features  

---

# 🔮 Future Enhancements

- Editable activity feature  
- Stronger authentication system  
- Custom AI scheduling model  
- Cloud deployment (Render / Heroku / AWS)  
- Mobile-friendly UI  

---

# 📄 License

This project was built as part of **San Jose State University – CS 152** coursework.  
For educational and portfolio use only.

---

# Acknowledgements

- Google Gemini API  
- Google Speech-to-Text  
- Flask documentation  
- TinyDB documentation  
