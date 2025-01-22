import json
import os
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Function to connect to MongoDB and fetch Markdown content from all matching job_ids
def fetch_markdown_from_db(job_id, mongo_uri):
    client = MongoClient(mongo_uri)
    db = client["parsing-data"]
    collection = db["data_1"]

    # Use ObjectId to query the job_id if it's an ObjectId type in MongoDB
    documents = collection.find({"job_id": ObjectId(job_id)})

    content_list = []  # List to store all content from matching documents
    for document in documents:
        content = document.get("content")
        if content:
            content_list.append(content)

    if content_list:
        return content_list
    else:
        return None

# Function to extract recommendations from Markdown content (if table format exists)
def extract_recommendations_from_table(md_content):
    lines = md_content.splitlines()
    table_lines = [line for line in lines if "|" in line and not line.startswith("|---")]

    recommendations = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 3:
            cor, loe, recommendation = cells
            if cor.lower() == "cor" and loe.lower() == "loe":
                continue
            recommendations.append({
                "recommendation_content": recommendation.strip(),
                "recommendation_class": cor.strip(),
                "rating": loe.strip()
            })

    return recommendations

# Function to extract recommendations from regular Markdown content (non-table)
def extract_recommendations_from_plain_text(md_content):
    recommendations = []
    if "recommendation:" in md_content.lower():
        recommendations.append({
            "recommendation_content": md_content.strip(),
            "recommendation_class": "General",  # Or some default class
            "rating": "N/A"  # Or set appropriate default
        })
    return recommendations

# Function to generate JSON chunks
def generate_json_chunks(recommendations, title, stage, disease, specialty):
    base_json = {
        "title": title,
        "subCategory": [],
        "guide_title": title,
        "stage": [stage],
        "disease": [disease],
        "rationales": [],
        "references": [],
        "specialty": [specialty]
    }

    json_chunks = []
    for rec in recommendations:
        chunk = base_json.copy()
        chunk.update({
            "recommendation_content": rec["recommendation_content"],
            "recommendation_class": rec["recommendation_class"],
            "rating": rec["rating"]
        })
        json_chunks.append(chunk)

    return json_chunks

# Main script
def main():
    # Prompt user for metadata and job_id
    title = input("Enter Guide Title: ")
    stage = input("Enter Stage: ")
    disease = input("Enter Disease Title: ")
    specialty = input("Enter Specialty: ")
    job_id = input("Enter Job ID (mandatory): ")

    if not job_id:
        print("Job ID is required to fetch data.")
        return

    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        print("MongoDB URI not found. Please ensure it's set in the .env file.")
        return

    # Fetch Markdown content from MongoDB
    md_contents = fetch_markdown_from_db(job_id, mongo_uri)
    
    if md_contents:  # If we got a list of contents
        print(f"{len(md_contents)} documents found with Job ID {job_id}.")
        all_recommendations = []
        
        # Iterate over each content and extract recommendations
        for md_content in md_contents:
            if "|" in md_content:  # If the content appears to be in table format
                recommendations = extract_recommendations_from_table(md_content)
            else:  # Process as plain text
                recommendations = extract_recommendations_from_plain_text(md_content)
            
            all_recommendations.extend(recommendations)

        if all_recommendations:
            json_chunks = generate_json_chunks(all_recommendations, title, stage, disease, specialty)
            
            # Save to {job_id}.json
            output_file = f"{job_id}.json"
            with open(output_file, "w") as f:
                json.dump(json_chunks, f, indent=2)

            print(f"JSON file generated: {output_file}")
        else:
            print("No recommendations found in the fetched Markdown content.")
    else:
        print(f"Job ID {job_id} not found in the database.")

if __name__ == "__main__":
    main()
