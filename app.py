
import streamlit as st
import requests

API_URL = "https://shl-recommend-api.onrender.com/recommend"  

st.set_page_config(page_title="SHL Assessment Recommendation", layout="centered")

st.title(" SHL Assessment Recommendation System")
st.write("Enter hiring requirement or job description:")

query = st.text_area("Your Query")

if st.button("Get Recommendations"):
    if query.strip() == "":
        st.warning("Please enter a query first.")
    else:
        response = requests.post(API_URL, json={"query": query})

        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recommended_assessments", [])

            if not recommendations:
                st.warning("No recommendations found.")
            else:
                st.subheader(" Recommended Assessments")

                for idx, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
### {idx}. {rec['name']}
**Description:** {rec['description']}  
**Duration:** {rec['duration']} mins  
**Remote Support:** {rec['remote_support']}  
**Adaptive Support:** {rec['adaptive_support']}  
**Test Type:** {', '.join(rec['test_type'])}  

🔗 [Open Assessment]({rec['url']})
---
""")
        else:
            st.error(" Failed to fetch recommendations from API")
