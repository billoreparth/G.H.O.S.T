import pandas as pd
from pymongo import MongoClient

# 🔐 MongoDB Atlas cluster URL
MONGO_URI = "mongodb+srv://***db_user***:******pass******@ghostapi.3qe1pdk.mongodb.net/?appName=GHOSTapi"

# 📌 Database and collection names
DB_NAME = "GHOSTapi"
COLLECTION_NAME = "readings"

# 📁 Output CSV file
OUTPUT_FILE = "transmission_data.csv"

def export_mongodb_to_csv():
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Fetch all documents
    cursor = collection.find({}, {"_id": 0})  # exclude _id

    # Convert to DataFrame
    df = pd.DataFrame(list(cursor))

    if df.empty:
        print("⚠ No data found in collection.")
        return

    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Data exported successfully to {OUTPUT_FILE}")

if __name__ == "__main__":
    export_mongodb_to_csv()
