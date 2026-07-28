import mysql.connector
from transformers import pipeline
from datetime import date

# 1. Connect to your Aiven MySQL Cloud Database
print("Connecting to Aiven Cloud Database...")
try:
    db = mysql.connector.connect(
        host="mysql-353b8030-polukasaikiranreddy-71cd.b.aivencloud.com", # Replace with your Aiven Host
        port=25138,                                     # Replace with your Aiven Port
        user="avnadmin",                                # Replace with your Aiven User
        password="PASSWORD_REMOVED_FOR_SECURITY",                 # Replace with your Aiven Password
        database="ai_feedback_hub"
    )
    cursor = db.cursor()
    print("Successfully connected to the database!\n")
except Exception as e:
    print(f"Database connection failed: {e}")
    exit()

# 2. Load the NLP Transformer Model
print("Downloading/Loading the Hugging Face AI Model...")
# This specific model is highly optimized for fast sentiment analysis
analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# 3. Simulate incoming raw data (e.g., from an app store or support emails)
incoming_reviews = [
    "The app crashed three times during checkout, absolutely terrible experience.",
    "I love the new dashboard update! So fast, clean, and easy to use.",
    "Customer service was completely unhelpful when I asked for a refund.",
    "Decent app, but the load times are a bit slow sometimes.",
    "Best service I have ever used. Highly recommend to everyone!"
]

# 4. Analyze and Insert Loop
print("\nProcessing reviews through the AI...")
for text in incoming_reviews:
    # Run the Transformer model
    ai_result = analyzer(text)[0] 
    sentiment = ai_result['label']      # Returns 'POSITIVE' or 'NEGATIVE'
    confidence = ai_result['score']     # Returns a float like 0.9998
    
    # Prepare the SQL command
    sql = """
        INSERT INTO reviews (date_received, raw_text, ai_sentiment, ai_confidence) 
        VALUES (%s, %s, %s, %s)
    """
    
    # Package the variables safely
    values = (date.today(), text, sentiment, float(confidence))
    
    # Execute the insertion
    cursor.execute(sql, values)
    
    # Print a live log to your console
    print(f"Stored: [{sentiment}] (Confidence: {confidence:.2f}) -> {text[:40]}...")

# 5. Commit changes to the cloud and close
db.commit()
cursor.close()
db.close()

print(f"\nSuccess! {len(incoming_reviews)} reviews analyzed and stored in MySQL.")