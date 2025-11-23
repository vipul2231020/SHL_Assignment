import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

GENAI_API_KEY = "AIzaSyCIrA6ON96hRZyVLTIMKmLE7nIfN9gJ_-w"
genai.configure(api_key=GENAI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

df = pd.read_csv("shl_individual_tests.csv")

def find_col(possible, df_cols):
    for c in possible:
        if c in df_cols:
            return c
    return None

name_col = find_col(["Assessment Name","name","Title"], df.columns)
url_col  = find_col(["URL","url","Link"], df.columns)
desc_col = find_col(["Description","description"], df.columns)

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


def rag_recommend(query):
    candidates = retrieve_top(query, 10)

    context = "\n".join([
        f"{c['name']} - {c['description']} ({c['url']})"
        for c in candidates
    ])

    prompt = f"""
You are an SHL assessment expert.

User Requirement:
{query}

From the following assessments, choose the best 5 that match the requirement.
Ensure balance between technical and behavioral skills if both are present.

Assessments:
{context}

Return only the names and URLs in list format.
"""

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    while True:
        q = input("\nEnter hiring query (or 'exit'): ")
        if q.lower() == "exit":
            break

        print("\n🔹 Final RAG Recommendations:\n")
        print(rag_recommend(q))
