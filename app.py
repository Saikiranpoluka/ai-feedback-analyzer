import streamlit as st
import mysql.connector
from transformers import pipeline
from datetime import date

# 1. Setup the Web Page
st.set_page_config(page_title="AI Feedback Analyzer", page_icon="🤖")
st.title("Customer Feedback AI Analyzer")
st.write("Type a mock customer review below. My Hugging Face model will analyze the sentiment, and save the result to a live Aiven Cloud Database!")

# 2. Load the AI (Streamlit caches this so it doesn't reload on every button click)
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

analyzer = load_model()

# 3. Create the User Input Form
user_input = st.text_area("Enter a customer review:", placeholder="e.g., The app crashed and I hate the new update...")

if st.button("Analyze & Save to Database"):
    if user_input:
        # Run AI
        result = analyzer(user_input)[0]
        sentiment = result['label']
        confidence = result['score']
        
        # Display the result to your friend on the website
        if sentiment == "POSITIVE":
            st.success(f"🟢 **POSITIVE** (Confidence: {confidence:.2f})")
        else:
            st.error(f"🔴 **NEGATIVE** (Confidence: {confidence:.2f})")
            
        # Save to Aiven MySQL
        try:
            db = mysql.connector.connect(
                host="mysql-353b8030-polukasaikiranreddy-71cd.b.aivencloud.com",
                port=25138,
                user="avnadmin",
                password= st.secrets["mysql"]["password"],
                database="ai_feedback_hub",
                ssl_ca="ca.pem" 
            )
            cursor = db.cursor()
            sql = "INSERT INTO reviews (date_received, raw_text, ai_sentiment, ai_confidence) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (date.today(), user_input, sentiment, float(confidence)))
            db.commit()
            cursor.close()
            db.close()
            st.info("✅ Successfully saved to the Cloud Database! Check Power BI to see it live.")
        except Exception as e:
            st.warning(f"Database error: {e}")
    else:
        st.warning("Please type a review first!")