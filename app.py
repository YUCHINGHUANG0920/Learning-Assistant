from flask import *
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import pymongo
from datetime import datetime, timedelta
import atexit

app = Flask(__name__, static_folder='static')

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
github_key = os.getenv("GITHUB_TOKEN")

# Connect to MongoDB
db_client = pymongo.MongoClient("YourConnectionString")
db = db_client["LearningAssistant"]
githubResponse = db["githubResponse"]
openaiResponse = db["openaiResponse"]


# Route
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.static_folder), 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

@app.route('/manifest.json')
def send_manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

@app.route("/learning_assistant", methods=["POST"])
def learning_assistant():
    data = request.json
    topic = data.get("topic")
    difficulty = data.get("difficulty")

    if not topic or not difficulty:
        return jsonify({"error": "Please provide Topic and Difficulty"}), 400

    # Call GitHub API (Use DB to reduce calls)
    existing_record = githubResponse.find_one({"topic": topic})
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
    if existing_record and existing_record["github_timestamp"] > two_weeks_ago:
        github_response = existing_record["github_response"]
        repositories = github_response.get("items", [])
    else:
        url = f"https://api.github.com/search/repositories?q={topic}&sort=stars"
        headers = {"Authorization": f"Bearer {github_key}"}
        github_response = requests.get(url, headers=headers)
        if github_response.status_code != 200:
            return jsonify({"error": "Cannot Access GitHub API"}), 500
        githubResponse.update_one(
            {"topic": topic},
            {'$set': {"github_response": github_response.json(), "github_timestamp": datetime.utcnow()}},
            upsert=True
        )
        repositories = github_response.json().get("items", [])

    # Process repositories 
    if not isinstance(repositories, list):
        return jsonify({"error": "GitHub API Issue"}), 500
    repositories = repositories[:20]
    
    if not repositories:
        return jsonify({"error": "There are no related repositories"}), 404

    repo_details = [
        {"name": repo["name"], "description": repo["description"] or "No description", "stars": repo["stargazers_count"], "url": repo["html_url"]}
        for repo in repositories
    ]

    repo_descriptions = "\n".join(
        [f"{idx + 1}. {repo['name']}: {repo['description']} URL: {repo['url']}" for idx, repo in enumerate(repo_details)]
    )

    # Call OpenAI API (Use DB to reduce calls)
    openai_record = openaiResponse.find_one({"topic": topic, "difficulty": difficulty})
    if openai_record:
        structured_data = openai_record["openai_response"]
        return jsonify({"results": structured_data})
    else:
        prompt = f"""
        I have found the following GitHub repositories related to {topic}. Provide a filtered list of up to **five repositories** that are the most suitable for this level, along with their URLs and brief justifications for your selections. 
        
        Please use the following format:
        
        1. **NAME**
        - **URL:** 
        - **Justification:** 

        2. **NAME**
        - **URL:** 
        - **Justification:** 

        Repositories:
        {repo_descriptions}
        """

        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in GitHub project recommendations."},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-3.5-turbo",
                timeout=20
            )

            advice_text = response.choices[0].message.content

            repo_entries = advice_text.split('\n\n')
            structured_data = []
            for entry in repo_entries:
                if entry.strip() and entry[0].isdigit():
                    lines = entry.strip().split("\n")
                    idx = entry.split(".")[0].strip()
                    name_line = lines[0].strip()
                    url_line = lines[1].strip()
                    justification_line = lines[2].strip()

                    name = name_line.split("**")[1].strip() 
                    url = url_line.split("**")[2].strip()
                    justification = justification_line.split("**")[2].strip()
                    
                    matching_repo = next((r for r in repo_details if r["url"].lower() == url.lower()), None)
                    stars = matching_repo["stars"] if matching_repo else "Unknown"
                    
                    structured_data.append({
                        "id": idx,
                        "name": name,
                        "url": url,
                        "stars": stars,
                        "justification": justification
                        })

            openaiResponse.update_one(
                {"topic": topic, "difficulty": difficulty},
                {"$set": {"openai_response": structured_data}},
                upsert=True
            )

            return jsonify({"results": structured_data})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            print("Cleaning up resources")


def on_exit():
    print("Server shutting down...")


atexit.register(on_exit)


if __name__ == "__main__":
    try:
        app.run(port = 3000)
    except KeyboardInterrupt:
        print("Shutting down server with Ctrl+C")


