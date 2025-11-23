import requests
import csv

API_URL = "http://127.0.0.1:8000/recommend"

input_file = "qureis.txt"
output_file = "evaluation_output.csv"

with open(input_file, "r") as f:
    queries = [line.strip() for line in f if line.strip()]

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Query", "Assessment_url"])

    for query in queries:
        response = requests.post(API_URL, json={"query": query})
        data = response.json()

        recommendations = data.get("recommendations", [])

        for rec in recommendations:
            writer.writerow([query, rec["url"]])

print("✅ evaluation_output.csv generated successfully")
