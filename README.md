# LLM-Based Automation Agent

# PLEASE NOTE : In the format of dockerhub-username/repository-name:tag, my image can be found in namitabhatt/llm-automation-agent:latest !

This project is an automation agent that uses a Large Language Model (LLM) to perform various tasks, such as file manipulation, data extraction, and more. It exposes an API with two endpoints: `/run` to execute tasks and `/read` to read files.

## Features
- **Task Execution**: Accepts plain-English tasks and performs multi-step processes using an LLM.
- **File Operations**: Reads and writes files in the `/data` directory.
- **LLM Integration**: Uses OpenAI's GPT-4o-Mini model for text and image-based tasks.
- **Dockerized**: Easily deployable using Docker.

## API Endpoints
1. **POST /run**
   - Executes a task described in plain English.
   - Example:
     ```json
     {
       "task": "Count the number of Wednesdays in /data/dates.txt and write the result to /data/dates-wednesdays.txt"
     }
     ```
   - Returns:
     ```json
     {
       "message": "Task executed successfully",
       "output_path": "/data/dates-wednesdays.txt"
     }
     ```

2. **GET /read**
   - Reads the content of a file.
   - Example:
     ```
     /read?path=/data/dates-wednesdays.txt
     ```
   - Returns the file content as plain text.

## Setup

### Prerequisites
- Python 3.9
- Docker
- OpenAI API key (set as `AIPROXY_TOKEN` environment variable)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/namitabhatt22/llm-automation-agent.git
   cd llm-automation-agent

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

Set up environment variables:

Create a .env file and add your OpenAI API key: AIPROXY_TOKEN=your_openai_api_key


Docker
1. Build the Docker image:
    ```bash
    docker build -t namitabhatt/llm-automation-agent:latest .

2. Run the Docker container:
    ```bash  
    docker run -p 8000:8000 -e AIPROXY_TOKEN=your_openai_api_key namitabhatt/llm-automation-agent


Code Structure
- src/main.py: Flask application with API endpoints.
- src/tasks.py: Task execution logic.
- src/llm_utils.py: Utility functions for interacting with the LLM.
- Dockerfile: Docker configuration for the application.
- requirements.txt: Python dependencies.
- docker-imageee.yml: GitHub Actions workflow for Docker image build and push.
