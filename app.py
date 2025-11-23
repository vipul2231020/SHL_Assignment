import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(
    page_title="SHL Assessment Recommendation System",
    page_icon="🔍",
    layout="centered"
)

st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.card {
    border: 1px solid #1f2933;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 15px;
    background: #111827;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}
.card h4 {
    color: #22c55e;
    margin-bottom: 8px;
}
.card a {
    color: #60a5fa;
    text-decoration: none;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align:center;'> SHL Assessment Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Enter hiring requirement or job description</p>", unsafe_allow_html=True)

query = st.text_area("Your Query", height=120, placeholder="e.g. Need Java developer with communication skills")

if st.button("Get Recommendations"):
    if query.strip() == "":
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Analyzing and generating recommendations..."):
            try:
                response = requests.post(API_URL, json={"query": query})
            except:
                st.error(" API Server not running. Please start FastAPI first.")
                st.stop()

        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recommendations", [])

            st.markdown("## Recommended Assessments")

            if not recommendations:
                st.warning("No recommendations found.")
            else:
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div class="card">
                        <h4>#{i} {rec['name']}</h4>
                        <a href="{rec['url']}" target="_blank">🔗 View Assessment</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error(" Failed to fetch recommendations from API")
