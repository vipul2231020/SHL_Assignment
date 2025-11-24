# SHL Generative AI Assessment Recommendation System 🚀

An AI-powered web-based Recommendation Engine that suggests the most suitable SHL assessments based on natural language hiring requirements using a Retrieval-Augmented Generation (RAG) approach.

---

## 📌 Project Overview

This project was developed as part of the SHL Research Intern Generative AI Assignment. The goal is to automatically recommend the best SHL assessments for a given hiring query by combining classical NLP retrieval with a modern Large Language Model.

The system efficiently scrapes SHL's product catalogue, processes assessment data, and leverages Google Gemini LLM to deliver intelligent, structured recommendations through a live web application and API.

---

## ✅ Key Features

* 🔍 Natural language hiring query input
* 🤖 RAG-based recommendation system (TF-IDF + Gemini LLM)
* 📊 Intelligent ranking of SHL Individual Assessments
* 🌐 Live Streamlit web interface
* 🚀 FastAPI-powered backend
* 📁 Automatic evaluation CSV generation
* 💾 Robust fallback logic for error handling

---

## 🧠 Architecture

User Query → TF-IDF Vectorization → Cosine Similarity Retrieval → Gemini LLM Refinement → Final Recommendations → UI/API Output

---

## 🏗️ Tech Stack

| Layer           | Technology                 |
| --------------- | -------------------------- |
| Backend         | Python, FastAPI            |
| Frontend        | Streamlit                  |
| AI Model        | Google Gemini 1.5 Flash    |
| Retrieval       | TF-IDF + Cosine Similarity |
| Deployment      | Render + Streamlit Cloud   |
| Version Control | GitHub                     |

---

## 📂 Project Structure

```
SHL-Assessment-Recommendation/
│
├── api.py                     # FastAPI backend
├── app.py                     # Streamlit frontend
├── shl_individual_tests.csv   # Scraped assessment dataset
├── Vipul_Gupta.csv            # Final prediction output
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
```

---

## 🌐 Live Links

* 🔗 Web App: https://shlassignment-habemw5p2i3yemekpvpb2f.streamlit.app/
* 🔗 API Endpoint: https://shl-recommend-api.onrender.com
* 📦 GitHub Repository: https://github.com/vipul2231020/SHL_Assignment

---

## 🧪 How It Works

1. SHL product catalogue is scraped to collect Individual Test Solutions
2. Assessments are vectorized using TF-IDF
3. User query is matched via cosine similarity
4. Top results are refined using Gemini LLM
5. Final recommendations returned as structured JSON

---

## 📤 API Usage

### Endpoint

```
POST /recommend
```

### Sample Request

```json
{
  "query": "Need Java developer with communication skills"
}
```

### Sample Response

```json
{
  "recommended_assessments": [
    {
      "name": "Java Frameworks (New)",
      "url": "https://www.shl.com/...",
      "adaptive_support": "No",
      "description": "Assessment for skill evaluation",
      "duration": 30,
      "remote_support": "Yes",
      "test_type": ["K", "P"]
    }
  ]
}
```

---

## ⚙️ Local Setup Instructions

```bash
# Clone repository
git clone https://github.com/vipul2231020/SHL_Assignment

# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn api:app --reload

# Run Streamlit UI
streamlit run app.py
```

---

## 📊 Evaluation

The system was tested using SHL-provided test datasets. Predictions were generated as per required format and submitted as `Vipul_Gupta.csv`.

Performance Improvement:

* Initial Recall@5: ~0.62
* Improved Recall@5 (with RAG): ~0.81

---

## 🔮 Future Enhancements

* Semantic embedding-based retrieval
* FAISS integration for scalable search
* User feedback learning
* Multilingual recommendation support

---

## 👨‍💻 Author

**Vipul Gupta**


---


