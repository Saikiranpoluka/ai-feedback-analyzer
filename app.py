import streamlit as st
import mysql.connector
from transformers import pipeline
from datetime import date
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="Enterprise AI Feedback Hub", page_icon="⚡", layout="wide")

st.title("⚡ Enterprise AI Feedback & Issue Classifier")
st.caption("Powered by Hugging Face, AgentRouter, & Aiven MySQL")

# 2. Load Local Hugging Face Models (Cached for Performance)
@st.cache_resource
def load_models():
    # Sentiment Classifier (Positive/Negative)
    sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    # Zero-Shot Topic Classifier (Categorization)
    topic_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return sentiment_model, topic_model

sentiment_analyzer, topic_classifier = load_models()

# 3. Build the UI
col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area(
        "Customer Review / Feedback:", 
        height=150, 
        placeholder="e.g., The app keeps lagging during checkout and charged my card twice!!"
    )
    
    # Define the categories you want the AI to sort feedback into
    candidate_labels = ["UI/UX Bug", "Billing & Payment", "Performance & Lag", "Customer Support", "General Praise"]
    
    submit_btn = st.button("Run Full AI Analysis", type="primary")

# 4. Core Application Logic
if submit_btn and user_input:
    with st.spinner("Analyzing with Neural Networks..."):
        
        # Step A: Predict Sentiment
        sent_result = sentiment_analyzer(user_input)[0]
        sentiment = sent_result['label']
        sent_score = sent_result['score']
        
        # Step B: Predict Category / Aspect
        topic_result = topic_classifier(user_input, candidate_labels)
        top_category = topic_result['labels'][0]
        category_score = topic_result['scores'][0]

    # Step C: Display Metrics in UI
    st.subheader("AI Analysis Output")
    m1, m2, m3 = st.columns(3)
    
    m1.metric("Sentiment", sentiment, delta=f"{sent_score*100:.1f}% Confidence")
    m2.metric("Detected Category", top_category, delta=f"{category_score*100:.1f}% Match")
    
    # Step D: Generative AI Feature (AgentRouter LLM)
    if sentiment == "NEGATIVE":
        st.error(f"🚨 **Issue Flagged:** Customer reported a **{top_category}** issue.")
        
        with st.spinner("Drafting custom apology email using AgentRouter..."):
            try:
                # Initialize the OpenAI client to point to AgentRouter's gateway
                client = OpenAI(
                    base_url="https://agentrouter.org/v1",
                    api_key=st.secrets["AGENTROUTER_API_KEY"]
                )
                
                # Prompt Engineering
                prompt = f"""
                You are a senior customer support manager. 
                A customer just left this negative review: "{user_input}"
                The AI categorized this issue as: {top_category}
                
                Write a short, empathetic, and professional apology email to this customer. 
                Acknowledge their specific issue. Offer a 20% discount code (SORRY20) to make things right.
                Keep it under 3 paragraphs. Do not include subject lines, just the email body.
                """
                
                # Call Claude 3.5 Sonnet (or swap with 'gpt-4o' or 'deepseek-reasoner')
                response = client.chat.completions.create(
                    model="claude-3-5-sonnet", 
                    messages=[
                        {"role": "system", "content": "You are an empathetic customer support manager."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                draft_email = response.choices[0].message.content
                
                st.subheader("✉️ Auto-Generated Apology Draft")
                st.info(draft_email)
                
            except Exception as e:
                st.warning(f"Failed to generate email: {e}. Check your AgentRouter API key in secrets.")
    else:
        st.success(f"🎉 **Positive Feedback:** Related to **{top_category}**.")

    # Step E: Database Insertion
    try:
        # Secure connection using st.secrets
        db = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=int(st.secrets["mysql"]["port"]),
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            ssl_ca="ca.pem"
        )
        cursor = db.cursor()
        
        # Ensure the 'category' column exists
        cursor.execute("ALTER TABLE reviews ADD COLUMN IF NOT EXISTS category VARCHAR(100);")
        
        sql = """
            INSERT INTO reviews (date_received, raw_text, ai_sentiment, ai_confidence, category)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (date.today(), user_input, sentiment, float(sent_score), top_category))
        db.commit()
        
        cursor.close()
        db.close()
        st.success("💾 Results successfully saved to Aiven Cloud Database!")
    except Exception as e:
        st.warning(f"Database error: {e}")