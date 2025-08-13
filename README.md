# EvaluateHub 
EvaluateHub is a web-based platform for evaluating IELTS, SAT, and GRE essays.  
It has two parts:
- **Backend** (Django) – Handles AI evaluation using LLaMA2 via Ollama.
- **Frontend** (Node.js + Express) – Serves HTML pages and interacts with the backend.

### Workflow
Run llama2, nodejs server and django server. Open web app at `http://127.0.0.1:3000` --> Select test type --> A prompt will be generated through backend (django)
--> write essay --> Press "Submit" button --> both essay and prompt will be sent to the backend --> backend will send eval;uation result to frontend and it will be displayed on the page.
### Note --> Local Setup takes about 30-40 secs for prompt generation and 7-8 minutes for essay evaluation. While the API setup takes 1-3 secs for both.

### Link for API Setup
https://github.com/ImAleenaSajid/fyp-frontend  (Frontend)
https://github.com/ImAleenaSajid/fyp-backend   (Backend)

### Running Application --> https://evaluatehubfrontend.vercel.app

### Deepseek vs Llama --> https://docs.google.com/spreadsheets/d/1mwDjxOqOM1vz-DtRJsvxRUEMoJk5m_2Afh6CNrEOcyU/edit?usp=sharing
---

## 📂 Project Structure

```

Django/
├── hello/
│   ├── views.py      # Handles essay submission & prompt generation
│   ├── urls.py
│   ├── models.py
│   └── ...
├── manage.py
├── requirements.txt

Node/
├── public/
│   ├── css/
│   ├── images/
│   ├── js/
│   ├── index.html
├── views/
│   ├── gre.html
│   ├── ielts.html
│   ├── sat.html
├── app.js            # Express server
├── package.json

````

---

## ⚙️ 1. Backend Setup (Django + Ollama + LLaMA2)

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (`venv`)
- [Ollama](https://ollama.ai/) installed locally

### Steps
1. **Navigate to the Django project:**
   ```bash
   cd DJANGO_PROJECT_FOLDER
``

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
**IF LOCAL SETUP**
4. **Install Ollama:**

   * Download and install from: [https://ollama.ai/download](https://ollama.ai/download)
   * After installation, verify:

     ```bash
     ollama --version
     ```

5. **Pull LLaMA2 model:**

   ```bash
   ollama pull llama2
   ollama run llama2
   ```
**IF API SETUP**
## 🔑 Getting Groq API Key for LLaMA 3.3 70B

Follow these steps to obtain and use your Groq API key for accessing the **LLaMA 3.3 70B** model:

### 1. Sign Up / Log In
- Visit [https://console.groq.com](https://console.groq.com)  
- Create an account or log in with your existing credentials.

### 2. Go to API Keys Section
- In the dashboard, find the **API Keys** section.
- This is usually located under your account/profile settings.

### 3. Create a New API Key
- Click **"Create API Key"**.
- Give it a descriptive name (e.g., `llama3-70b-access`).
- Ensure it has access to **`llama-3.3-70b-versatile`**.

### 4. Copy and Store Securely
- Once created, copy the key immediately (it will be shown only once).
- Store it securely (.env file in (Djnago Project).



6. **Apply Django migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Run Django backend:**

   ```bash
   python manage.py runserver
   ```

   Backend runs at:
   `http://127.0.0.1:8000`

---

## 🎨 2. Frontend Setup (Node.js + Express)

### Prerequisites

* Node.js 16+
* npm

### Steps

1. **Navigate to the Node.js project:**

   ```bash
   cd NODE_PROJECT_FOLDER
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start Node.js server:**

   ```bash
   node app.js
   ```

   Frontend runs at:
   `http://127.0.0.1:3000`

---

## 🔗 How They Work Together

* The **Node.js frontend** serves HTML pages and sends essay data to the **Django backend**.
* Django sends the essay text & prompt to **Ollama**, which uses **LLaMA2** to evaluate the essay.
* The response is returned to the frontend and shown to the user.

---

## 🚀 Running the App

1. **Start Django backend** (with Ollama running in the background):

   ```bash
   cd DJANGO_PROJECT_FOLDER
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python manage.py runserver
   ```

2. **Start Node.js frontend:**

   ```bash
   cd NODE_PROJECT_FOLDER
   node app.js
   ```

3. **Open in browser:**

   ```
   http://127.0.0.1:3000
   ```

---

## 📌 Notes

* **You only need to open the Node.js link in your browser** (`http://127.0.0.1:3000`).
* Ollama must be installed, and the `llama2` model must be pulled before running.
* The backend **must** be running for evaluations to work.
