# Backend-Development-Exercise-Sales-Team-Per-formance-Analysis-Using-LLM
 Develop a backend system that uses a Large Language Model (LLM) to analyze  sales data and provide feedback on both individual sales representatives and  overall team performance.

 ## Task Description

### Data Ingestion
* Implement a flexible mechanism to ingest sales data in CSV or JSON format.

### LLM Integration
* Integrate a Large Language Model (like GPT) for data analysis.
* The system should process data and generate insights for both individual representatives and the sales team as a whole.

### API Development
* Develop multiple RESTful API endpoints:
  * An endpoint to query performance feedback for a specific sales representative.
  * An endpoint to assess overall team performance.
  * An endpoint for sales performance trends and forecasting.
* Each endpoint should accept relevant parameters and return LLM-generated insights.

### Feedback Generation
* Leverage the LLM to provide qualitative feedback and actionable insights based on the sales data.

### Technology Choice
* You are free to use any backend technologies and frameworks you prefer.
* The API endpoints should be tested using API testing tools like Postman or Insomnia.


Code Explanation:

The provided code is a Flask application that analyzes sales performance data using a large language model (LLM) from Groq. It offers endpoints for various analysis tasks, including:

    /api/rep_performance/<userid>: Provides feedback on a specific representative's performance based on their sales data.
    /api/team_performance: Provides feedback on the overall team's performance.
    /api/performance_trends/<time_period>: Analyzes performance trends for a given time period (currently supports monthly).

Key Functionality:

    Load Sales Data:
        The load_sales_data function reads the sales performance data from a CSV file named sales_performance_data.csv.
        If the file is not found, it returns None.

    Representative Performance Analysis:
        The /api/rep_performance/<userid> endpoint retrieves sales data for a specific representative.
        It calculates various metrics based on the data and sends it to the LLM for analysis.
        The LLM provides feedback on the representative's performance, including strengths, weaknesses, and areas for improvement.

    Team Performance Analysis:
        The /api/team_performance endpoint retrieves all sales data.
        It calculates team-level metrics and sends them to the LLM for analysis.
        The LLM provides feedback on the team's overall performance.

    Performance Trends Analysis:
        The /api/performance_trends/<time_period> endpoint analyzes performance trends for a given time period (currently only monthly).
        It filters the sales data based on the specified time period and calculates relevant metrics.
        The calculated metrics are sent to the LLM for analysis and forecasting.

Running the Code:

    Prerequisites:
        Ensure you have Python 3.6 or later installed.
        Install the required libraries: Flask, pandas, groq, dotenv, and datetime. You can use pip install Flask pandas groq dotenv datetime to install them.
        Create a .env file in your project directory and add your Groq API key as Groq_API_KEY.

    Virtual Environment (Optional):
        To isolate your project's dependencies and avoid conflicts with other projects, it's recommended to use a virtual environment.
        Create a virtual environment using virtualenv venv (or python -m venv venv for Python 3.6+).
        Activate the virtual environment using venv\Scripts\activate on Windows or source venv/bin/activate on macOS/Linux.
        Install the required libraries within the virtual environment.

    Run the Application:
        Navigate to your project directory in the terminal.
        Run the Flask application using python app.py.

Accessing Endpoints:

Once the application is running, you can access the endpoints using the following URLs:

    Representative Performance: http://localhost:5000/api/rep_performance/<userid> (replace <userid> with the actual representative ID)
    Team Performance: http://localhost:5000/api/team_performance
    Performance Trends: http://localhost:5000/api/performance_trends/<time_period> (replace <time_period> with "3" for monthly)


**Purpose of `.env` Files:**

- `.env` files are used to store sensitive information, such as API keys, passwords, or database credentials.
- By storing these values in a separate file, you can avoid accidentally committing them to version control (e.g., Git), which could expose them publicly.
- This helps maintain security and privacy.

**Usage in the Code:**

1. **Create the `.env` File:**
   - Create a file named `.env` in the same directory as your Python code.
   - Add the environment variables you want to use, in the format:
     ```
     VARIABLE_NAME=VALUE
     ```
     For example, if your Groq API key is `my_secret_api_key`, you would add:
     ```
     Groq_API_KEY=my_secret_api_key
     ```

2. **Load Environment Variables:**
   - Import the `dotenv` library at the beginning of your Python code.
   - Call the `load_dotenv()` function to load the environment variables from the `.env` file into the `os.environ` dictionary.

   Here's how it's used in the provided code:

   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   groq_api_key = os.environ['Groq_API_KEY']
   ```

3. **Access Environment Variables:**
   - Once the environment variables are loaded, you can access them using the `os.environ` dictionary.

   In the code, the Groq API key is accessed using:

   ```python
   client = Groq(api_key=groq_api_key)
   ```

**Important Considerations:**

- **Security:** Remember to **never** commit the `.env` file to version control. This would expose your sensitive information.
- **Environment:** Make sure the `.env` file is in the same directory as your Python code when running it.
- **Best Practices:** Use meaningful variable names for your environment variables to improve readability.

By following these steps, you can effectively use `.env` files to store sensitive information in your Python projects and maintain security.


Example Usage:

To get the performance feedback for a representative with ID 123, you can use the following curl command:
Bash

curl http://localhost:5000/api/rep_performance/123

Use code with caution.

This will send a GET request to the /api/rep_performance/<userid> endpoint and return the LLM's feedback in JSON format.
