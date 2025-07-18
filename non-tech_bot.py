import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- Config ---
API_KEY = "AIzaSyC4GFljfImdJ39uzkyj2vLZqbjqZ3fNGjg"
genai.configure(api_key=API_KEY)

# --- Load Data ---
df = pd.read_csv("chatbot/shopify.csv")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
country = st.sidebar.selectbox("Shipping Country", ["All"] + sorted(df["Shipping Country"].dropna().unique()))
category = st.sidebar.selectbox("Product Category", ["All"] + sorted(df["Product Category"].dropna().unique()))
min_rating = st.sidebar.slider("Minimum Rating", 1, 5, 1)
max_rating = st.sidebar.slider("Maximum Rating", 1, 5, 5)

# --- Apply Filters ---
filtered_df = df[
    (df["Rating"] >= min_rating) &
    (df["Rating"] <= max_rating)
]
if country != "All":
    filtered_df = filtered_df[filtered_df["Shipping Country"] == country]
if category != "All":
    filtered_df = filtered_df[filtered_df["Product Category"] == category]

# --- UI ---
st.title("🛍️ Shopify Review Explorer")
st.write("Ask a natural language question and get instant review insights.")

user_query = st.text_input("❓ Your question", placeholder="e.g. What are top complaints in Canada?")

# --- Gemini Prompt Function ---
def genaimodel(user_query, sample_data, model="gemini-2.0-flash", max_tokens=500, temperature=0.4):
    prompt = f"""
You are a helpful data analyst. You will answer only based on the data shown below.
return only asked information totally relevant to the user's question. Be brief. Do not give long summaries or dataset overviews.
Focus only on what's relevant to the question.
Be concise. For summaries like 'top complaints or compliments', list the key issues or praises as short phrases (e.g., 'Late delivery', 'Great packaging').
Do NOT say the data is insufficient unless reviews are truly blank.


User Question: {user_query}

Here is the relevant data:
{sample_data}
    """

    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Button Action ---
if st.button("Get Insights") and user_query:
    if filtered_df.empty:
        st.warning("No data matches your filters.")
    else:
        sample_rows = filtered_df[[
            "Review Content", "Product Name", "Rating", "Product Category", "Timestamp",
            "Order Value", "Fulfillment Status", "Shipping Country"
        ]].to_dict(orient="records")

        sample_str = "\n".join([str(row) for row in sample_rows])

        answer = genaimodel(user_query, sample_str)

        st.markdown("### 📊 Insight")
        st.write(answer)

