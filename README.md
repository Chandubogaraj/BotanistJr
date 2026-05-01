# 🌿 BotanistJR - Plant Identification Web App

BotanistJR is a Flask-based web application that allows users to **register, log in, and identify plants** by uploading images. It uses the **PlantNet API** to analyze images and return plant names with confidence scores.



# Features

*  User authentication (Register/Login/Logout)
*  Plant identification using image upload
*  Displays:

  * Common name
  * Scientific name
  * Confidence score
  * SQLite database for user management



# Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **API:** PlantNet API
* **Frontend:** HTML (Jinja templates)



# Project Structure

```
BotanistJR/
│
├── app.py
├── botanistjr.db
├── templates/
│   ├── login.html
│   ├── register.html
│   └── main.html
│
└── README.md
```



# Installation & Setup

# Clone the repository

```
git clone https://github.com/your-username/botanistjr.git
cd botanistjr
```

#Install dependencies

```
pip install flask requests python-dotenv
```

---

#Set up environment variables

Create a `.env` file in the root directory:

```
PLANTNET_API_KEY=your_api_key_here
```

---

# Run the application

```
python app.py
```

---

# Open in browser

```
http://127.0.0.1:5000
```

---

# API Key Setup

* Get your API key from: https://my.plantnet.org/
* Add it to `.env` file or environment variables.

---

# Usage

1. Register a new account
2. Log in
3. Upload or capture a plant image
4. View identification results instantly

---

# Notes

* Make sure your API key is valid
* Do not expose your API key in public repositories
* Works best with clear plant images

---

# Troubleshooting

# "Unauthorized" error

* Ensure you are logged in before making prediction requests

# "Invalid image data"

* Check if image is properly encoded in base64

# API not working

* Verify your PlantNet API key
* Check internet connection

---

# Future Improvements

* Mobile-friendly UI
* Multi-language support
* AI model integration (offline mode)
* Camera capture support

---

# Author

Your Name
GitHub: https://github.com/your-username

---

# License

This project is open-source and available under the MIT License.

