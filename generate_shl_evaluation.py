import pandas as pd
import requests
import csv

API_URL = "http://127.0.0.1:8000/recommend"


input_file = "Gen_AI Dataset.xlsx"   
df = pd.read_excel(input_file)


if "query" in df.columns:
    queries = df["query"].dropna().tolist()
else:
    queries = df[df.columns[0]].dropna().tolist()

output_file = "official_shl_evaluation.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "Assessment_url"])

    for query in queries:
        response = requests.post(API_URL, json={"query": query})
        data = response.json()

        recommendations = data.get("recommendations", [])

        for rec in recommendations:
            writer.writerow([query, rec["url"]])

print(" official_shl_evaluation.csv generated successfully")
