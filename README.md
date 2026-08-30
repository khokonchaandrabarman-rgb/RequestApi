নিচের README.md ফাইলটি তোমার Python Flask API Dashboard প্রজেক্টের জন্য ব্যবহার করতে পারো।

🚀 Python Flask API Dashboard

একটি সুন্দর ও সহজ Python Flask API Dashboard, যেখানে একই Python ফাইলের মাধ্যমে Website এবং REST API পরিচালনা করা যায়।

এখানে "GET", "POST", "PUT", এবং "DELETE" Request পাঠানো এবং Request History দেখা যায়।

---

✨ Features

- 🐍 Python Flask Backend
- 🌐 সুন্দর Web Dashboard
- 📥 GET Request
- 📤 POST Request
- ✏️ PUT Request
- 🗑️ DELETE Request
- 📡 Real-time Request History
- 📊 Total Data Counter
- 📈 Total Request Counter
- 🧪 Built-in API Tester
- 📝 JSON Request Body Support
- 🔄 Automatic Request History Refresh
- 📱 Mobile Responsive Design
- 📄 সব Website Code একটি "app.py" ফাইলে

---

📁 Project Structure

python-flask-api/
│
└── app.py

এই প্রজেক্টে আলাদা HTML, CSS বা JavaScript ফাইলের প্রয়োজন নেই।

সবকিছু "app.py"-এর মধ্যে রয়েছে।

---

⚙️ Installation

প্রথমে Python ইনস্টল থাকতে হবে।

তারপর Flask ইনস্টল করুন:

pip install flask

---

▶️ Run

প্রজেক্টের folder-এ গিয়ে চালান:

python app.py

Server চালু হলে সাধারণত দেখাবে:

Running on http://127.0.0.1:5000

তারপর Browser-এ যান:

http://127.0.0.1:5000

---

🔌 API Endpoints

GET

সব Data পাওয়ার জন্য:

GET /api/data

Example:

http://127.0.0.1:5000/api/data

Response:

{
    "success": true,
    "count": 1,
    "data": [
        {
            "id": 1,
            "name": "Khokon",
            "message": "Hello API!",
            "time": "2026-08-30 12:00:00"
        }
    ]
}

---

📤 POST

নতুন Data যোগ করতে:

POST /api/data

JSON Body:

{
    "name": "Khokon",
    "message": "Hello from Python!"
}

Python "requests" দিয়ে:

import requests

url = "http://127.0.0.1:5000/api/data"

data = {
    "name": "Khokon",
    "message": "Hello from Python!"
}

response = requests.post(
    url,
    json=data
)

print(response.status_code)
print(response.json())

---

✏️ PUT

আগের Data পরিবর্তন করতে:

PUT /api/data/1

JSON Body:

{
    "name": "New Name",
    "message": "Updated message"
}

Python:

import requests

url = "http://127.0.0.1:5000/api/data/1"

data = {
    "name": "New Name",
    "message": "Updated message"
}

response = requests.put(
    url,
    json=data
)

print(response.json())

---

🗑️ DELETE

Data মুছে ফেলতে:

DELETE /api/data/1

Python:

import requests

url = "http://127.0.0.1:5000/api/data/1"

response = requests.delete(url)

print(response.json())

---

📡 Request History

প্রতিটি API Request Dashboard-এর Request History section-এ দেখা যাবে।

প্রতিটি Request-এর:

- Method
- API Path
- Status Code
- Request Time
- JSON Body

দেখানো হবে।

History API:

GET /api/history

---

🧪 Built-in API Tester

Dashboard-এর API Tester ব্যবহার করে Browser থেকেই Request পাঠানো যায়।

Supported methods:

GET
POST
PUT
DELETE

উদাহরণ:

Method: POST

Path:
/api/data

Body:

{
    "name": "Test User",
    "message": "Testing API"
}

তারপর:

⚡ Send Request

button চাপলেই Request পাঠানো হবে।

---

🧹 Clear Request History

সব Request History মুছে ফেলতে:

POST /api/history/clear

Dashboard-এর:

🗑 Clear

button ব্যবহার করা যাবে।

---

📱 Mobile Support

Dashboardটি Responsive Design ব্যবহার করে তৈরি।

তাই:

- Android
- iPhone
- Tablet
- Laptop
- Desktop

সব ধরনের Screen-এ ব্যবহার করা যাবে।

---

🐍 Python Client Example

GET:

import requests

url = "http://127.0.0.1:5000/api/data"

response = requests.get(url)

print(response.json())

POST:

import requests

url = "http://127.0.0.1:5000/api/data"

payload = {
    "name": "Khokon",
    "message": "Testing POST API"
}

response = requests.post(
    url,
    json=payload
)

print(response.json())

---

🌐 Deploy করার আগে

Development-এর জন্য:

app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)

ব্যবহার করা হয়েছে।

Production server-এ deploy করার সময় "debug=True" ব্যবহার না করাই ভালো।

---

⚠️ গুরুত্বপূর্ণ

এই version-এর Data Python-এর memory-তে রাখা হয়।

তাই Flask server বন্ধ বা restart করলে Data হারিয়ে যাবে।

Production project-এর জন্য পরবর্তীতে ব্যবহার করা যেতে পারে:

- SQLite
- MySQL
- PostgreSQL
- MongoDB

---

🔐 Security

Production ব্যবহারের আগে যুক্ত করা উচিত:

- API Key / Authentication
- Rate Limiting
- Input Validation
- HTTPS
- CORS Configuration
- Database
- Error Logging

---

📜 License

এই project শেখার এবং ব্যক্তিগত ব্যবহারের জন্য ব্যবহার করা যেতে পারে।

---

👨‍💻 Built With

Python + Flask + HTML + CSS + JavaScript

Made with ❤️ using Python.
