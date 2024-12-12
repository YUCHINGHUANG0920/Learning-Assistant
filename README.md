# Learning Assistant Project

## Project Goals
GitHub is a hub for outstanding projects from developers worldwide. However, finding suitable resources for individual learning needs among the vast amount of repositories can be challenging.
This project leverages **LLM (Large Language Models)** alongside the GitHub API and OpenAI API to extract and analyze GitHub repository data. The goal is to intelligently recommend repositories based on difficulty levels tailored to the user's learning requirements.


![Image](image.png)

## Tools and Key Components
### - Backend -
### Tools Used:
* Programming Language: Python
* Framework: Flask
* APIs Integrated: GitHub API and OpenAI API
* Database: MongoDB

### Implementation Details:
1. Stores GitHub API and OpenAI API responses separately in MongoDB to reduce redundant requests.
    * GitHub API Content: Repository information, stars, and URLs.
    * OpenAI API Content: Analyzed difficulty levels and other insights useful for learning.
2. If the user requests the same topic within two weeks, the stored data is used instead of making new API calls, optimizing resource usage.

### API Key Setup: 
Before using the GitHub API and OpenAI API, you need to obtain the required API keys and store them in the `.env` file. This ensures secure access to the APIs without exposing sensitive information in the codebase.

You can obtain the following keys:

GitHub API Token: [GitHub API Token](https://github.com/settings/tokens)
OpenAI API Key: [OpenAI API Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)

Create a `.env` file in the root of your backend project and add the following content:

```bash
GITHUB_TOKEN = your_github_token_here
OPENAI_API_KEY = your_openai_api_key_here
```

### MongoDB Setup:
To connect the application to MongoDB:  
1. Create a Project and Cluster: Set up a project and cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).  
2. Create a User: Add a database user with a username and password for secure access.  
3. Get your connection string and Update it in the code 


### - Frontend -
### Tools Used:
* Framework: React
* Styling: CSS

### Setup Prerequisites:
1. Create the React application with the following command:

    ```bash
    npx create-react-app learning-assistant
    ```

2. Includes a table to display GitHub repository data and categorize results by difficulty levels to recommend the most suitable learning content.


## Running the Application
1. Start the Backend:
    Run the following command to launch the Flask server:

    ```bash
    python app.py
    ```
2. Start the Frontend:
    Navigate to the frontend folder and execute:

    ```bash
    npm start
    ```

3. Access the application through your browser to explore personalized GitHub repository recommendations.