# WhatsApp Chat Analyzer 📊

A Python-based analytics tool that processes exported WhatsApp chat files and provides meaningful insights using data analysis and Natural Language Processing (NLP).

This project helps users understand communication patterns, word usage, and sentiment trends from WhatsApp conversations in a simple and visual way.

---

## 🔍 Why This Project?

WhatsApp chats contain valuable information about:
- Communication habits
- User activity patterns
- Emotional tone of conversations

However, raw chat files are unstructured and difficult to analyze manually.  
This project solves that problem by converting chat data into structured insights using Python and NLP techniques.

---

## ⚙️ What Does This Project Do?

- Parses raw WhatsApp `.txt` chat export files
- Cleans and structures message data
- Analyzes:
  - Message frequency (daily, monthly, user-wise)
  - Most used words
  - Emoji usage
  - Sentiment distribution (Positive / Negative / Neutral)
- Displays insights using charts and graphs
- Provides a simple and user-friendly interface using Streamlit

---

## 🛠 Tech Stack Used

- **Programming Language:** Python  
- **Libraries & Tools:**
  - Pandas – data processing
  - NumPy – numerical operations
  - Regex – chat parsing
  - NLTK – NLP preprocessing
  - Matplotlib – data visualization
  - Streamlit – web-based user interface

---

## 📂 Project Workflow

1. Export WhatsApp chat as a `.txt` file
2. Upload the chat file to the application
3. Parse messages using Regex
4. Clean and preprocess text data
5. Perform statistical and sentiment analysis
6. Visualize insights using graphs and charts

---

## ▶️ How to Run the Project

```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git   # Clone the repository

cd whatsapp-chat-analyzer                                               # Navigate to the project directory

python -m venv venv                                                     # Create a virtual environment

# Activate the virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt                                         # Install all required dependencies (Pandas, NumPy, NLTK, Matplotlib, Streamlit)

streamlit run app.py                                                     # Run the Streamlit application
# The browser will open automatically. If not, copy the URL from the terminal (usually http://localhost:8501)

# Upload your WhatsApp chat .txt file (exported without media)
# Explore detailed analysis:
# - Message frequency (daily, monthly, user-wise)
# - Most used words
# - Emoji usage
# - Sentiment distribution (Positive / Negative / Neutral)
# - User activity patterns

# Notes:
# - Make sure Python 3.8 or above is installed
# - Only .txt chat files are supported (do not upload ZIP files)
