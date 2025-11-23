from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai


GENAI_API_KEY = "AIzaSyCIrA6ON96hRZyVLTIMKmLE7nIfN9gJ_-w"  
genai.configure(api_key=GENAI_API_KEY)


model = genai.GenerativeModel("models/gemini-1.5-flash-latest")



df = pd.read_csv("shl_individual_tests.csv")

def find_col(possible, df_cols):
    for c in possible:
        if c in df_cols:
            return c
    return None

name_col = find_col(["Assessment Name", "name", "Title"], df.columns)
url_col  = find_col(["URL", "url", "Link"], df.columns)
desc_col = find_col(["Description", "description"], df.columns)

df["text"] = df[name_col].astype(str) + " " + df[desc_col].fillna("").astype(str)

vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(df["text"])


def retrieve_top(query, top_k=10):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()
    top_indices = scores.argsort()[-top_k:][::-1]

    candidates = []
    for i in top_indices:
        candidates.append({
            "name": df.iloc[i][name_col],
            "url": df.iloc[i][url_col],
            "description": df.iloc[i][desc_col]
        })
    return candidates


import re
import json

def rag_recommend(query):
    candidates = retrieve_top(query, 10)

    if not candidates:
        return []

    context = "\n".join([
        f"{c['name']} ({c['url']})"
        for c in candidates
    ])

    prompt = f"""
You are an SHL assessment expert.

User Requirement:
{query}

Select the best 5 assessments from the list below.

Return the result STRICTLY in JSON format like:
[
  {{"name": "...", "url": "..."}},
  ...
]

Assessments:
{context}
"""

    try:
        response = model.generate_content(prompt)
        raw = response.text
        print("RAW GEMINI OUTPUT >>>")
        print(raw)

        
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and len(parsed) > 0:
                return parsed
        except:
            pass

        
        matches = re.findall(r"(.*?)\((https?://[^\)]+)\)", raw)
        results = [{"name": n.strip(" -*•"), "url": u.strip()} for n, u in matches[:5]]

        if results:
            return results

    except Exception as e:
        print("Gemini Error:", e)

    
    return [
        {"name": c["name"], "url": c["url"]}
        for c in candidates[:5]
    ]



app = FastAPI(title="SHL Assessment Recommendation API")

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/recommend")
def recommend(request: QueryRequest):
    raw_results = rag_recommend(request.query)

    final_results = []
    for r in raw_results:
        final_results.append({
            "url": r["url"],
            "name": r["name"],
            "adaptive_support": "No",
            "description": r.get("description", "Assessment for skill evaluation"),
            "duration": 30,
            "remote_support": "Yes",
            "test_type": ["K", "P"]
        })

    return {"recommended_assessments": final_results}
