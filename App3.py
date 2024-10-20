
from flask import Flask, request, jsonify
import pandas as pd
from groq import Groq
from datetime import datetime


import os
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Replace with your Groq API key
load_dotenv()
groq_api_key=os.environ['Groq_API_KEY'] #adding my groq api key

def load_sales_data(sales_performance_data): #Loads sales data from a CSV file.
    try:
        data = pd.read_csv(sales_performance_data) #sales_performance_data (str): Path to the CSV file containing sales data.
        return data
    except FileNotFoundError:  #pandas.DataFrame: The loaded sales data as a Pandas DataFrame, or None if file not found.

        return None

@app.route('/api/rep_performance/<userid>', methods=['GET'])
def rep_performance(userid): #Analyzes sales performance for a specific representative.
   
    employee_id = userid  #userid (str): The ID of the representative.
    sales_data = load_sales_data('sales_performance_data.csv')
    print(sales_data)  
    numerical_cols = ['employee_id',
    'lead_taken', 'tours_booked', 'applications', 'tours_per_lead', 'apps_per_tour', 'apps_per_lead',
    'revenue_confirmed', 'revenue_pending', 'revenue_runrate', 'tours_in_pipeline',
    'avg_deal_value_30_days', 'avg_close_rate_30_days', 'estimated_revenue', 'tours', 'tours_runrate',
    'tours_scheduled', 'tours_pending', 'tours_cancelled', 'mon_text', 'tue_text', 'wed_text', 'thur_text',
    'fri_text', 'sat_text', 'sun_text', 'mon_call', 'tue_call', 'wed_call', 'thur_call', 'fri_call', 'sat_call', 'sun_call'
    ]
    #grouping data by emmployee id
    grouped_df = sales_data.groupby('employee_id')[numerical_cols].mean()
  
    #Filtering data for the specific representative
    rep_data = grouped_df[ grouped_df['employee_id']==int(employee_id) ]
    print("the employee data looks like this", grouped_df)

    #Preparing data for Groq
    llm_data = rep_data.to_dict(orient='records')
    print('the llm data looks like this',llm_data)
    #Sending data to Groq
    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Analyze the following sales data for rep_id {employee_id}: {llm_data}. The data provided for this employee is the mean of all their datarows in the data file so keep that into account. Provide feedback on their performance, including strengths, weaknesses, and areas for improvement."}
        ],
        model="llama3-8b-8192"  #Groq model name
    )
    #Extracting feedback from the response
    feedback = response.choices[0].message.content
    return jsonify({'feedback': feedback}) #JSON: A JSON response containing feedback on the representative's performance.




@app.route('/api/team_performance', methods=['GET'])  #This API endpoint retrieves sales data, calculates team metrics,and sends the data to Groq for analysis and feedback generation.
def team_performance():
    #Retrieving all sales data
    sales_data = load_sales_data('sales_performance_data.csv')

    #Defining columns for numerical and categorical data analysis
    numerical_cols = ['employee_id',
    'lead_taken', 'tours_booked', 'applications', 'tours_per_lead', 'apps_per_tour', 'apps_per_lead',
    'revenue_confirmed', 'revenue_pending', 'revenue_runrate', 'tours_in_pipeline',
    'avg_deal_value_30_days', 'avg_close_rate_30_days', 'estimated_revenue', 'tours', 'tours_runrate',
    'tours_scheduled', 'tours_pending', 'tours_cancelled', 'mon_text', 'tue_text', 'wed_text', 'thur_text',
    'fri_text', 'sat_text', 'sun_text', 'mon_call', 'tue_call', 'wed_call', 'thur_call', 'fri_call', 'sat_call', 'sun_call'
    ]


    team_metrics = {}  #Creating an empty dictionary to store team metrics

    #Iterating through relevant columns in the data
    for column in ['lead_taken', 'tours_booked', 'applications', 'tours_per_lead', 'apps_per_tour', 'apps_per_lead',
                   'revenue_confirmed', 'revenue_pending', 'revenue_runrate', 'tours_in_pipeline',
                   'avg_deal_value_30_days', 'avg_close_rate_30_days', 'estimated_revenue', 'tours', 'tours_runrate',
                   'tours_scheduled', 'tours_pending', 'tours_cancelled', 'mon_text', 'tue_text', 'wed_text', 'thur_text',
                   'fri_text', 'sat_text', 'sun_text', 'mon_call', 'tue_call', 'wed_call', 'thur_call', 'fri_call', 'sat_call', 'sun_call']:
        if sales_data[column].dtype == 'object':  #Handling categorical data
            team_metrics[column] = sales_data[column].value_counts().to_dict()
        else:   #Handling numerical data - calculate mean, median, std, min, max
            team_metrics[column] = {
                'mean': sales_data[column].mean(),
                'median': sales_data[column].median(),
                'std': sales_data[column].std(),
                'min': sales_data[column].min(),
                'max': sales_data[column].max()
            }

    client = Groq(api_key=groq_api_key)  #Creaing Groq client using your API key
    response = client.chat.completions.create( #Sending data to Groq for analysis using chat.completions.create method
        messages=[  #Preparing message for Groq including team metrics
            {"role": "user", "content": f"Analyze the following sales data for the entire team: {team_metrics}. Provide feedback on the team's overall performance, including strengths, weaknesses, and areas for improvement."}
        ],  
        model="llama3-8b-8192"  # Replacing with your Groq model name
    )

    #Extracting feedback from the response
    feedback = response.choices[0].message.content
    return jsonify({'feedback': feedback}) #JSON: A JSON response containing the feedback from Groq.



@app.route("/") #This is a simple API endpoint that returns "hello world" for testing
def home():  
    return "hello world"


 #This api is not working as it is supposed to as of now it's just to show case my work and logic 

@app.route('/api/performance_trends/<time_period>', methods=['GET'])  #This API endpoint retrieves sales data based on a time period,calculates performance metrics, sends data to Groq for analysis,and returns the feedback.

def performance_trends(time_period): #time_period (str): The time period (for monthly).
    
    print("working1") #Placeholder for debugging
    sales_data = load_sales_data('sales_performance_data.csv')
    
    import datetime

    if time_period == '3':
        try:
            current_month = time_period
            #current_month = datetime.datetime.now().month
            print("This is data type before before",sales_data[sales_data["dated"]=="2022-07-26"])#Placeholder for debugging
            print("This is data type before",sales_data["dated"])#Placeholder for debugging
            print(sales_data['dated'].dtype)#Placeholder for debugging
            print(sales_data['employee_id'].dtype)#Placeholder for debugging
            # sales_data['dated'] = pd.to_datetime(sales_data['dated'])
            sales_data = sales_data[sales_data['dated'].dt.month == current_month]
            print("working2") #Placeholder for debugging
        except ValueError:
            # Handle conversion error if 'dated' cannot be converted
            return jsonify({'error': 'Failed to convert "dated" column to datetime format'}), 400
        #sales_data = sales_data[sales_data['dated'].dt.month == datetime.datetime.now().month]
        print("working3") #Placeholder for debugging
    # elif time_period == 'quarterly':
        # ... (your logic for quarterly filtering)
    else:
        return jsonify({'error': 'Invalid time period'}), 400
    print("working4") #Placeholder for debugging
    
    print ("this is data", sales_data['dated'].dt.month,"my current month", current_month) #Placeholder for debugging
   
    #Fetching sales data based on time period
    trend_data = {
    'total_leads_taken': sales_data[sales_data['dated'].dt.month == current_month]['lead_taken'].sum(),
    'total_tours_booked': sales_data[sales_data['dated'].dt.month == current_month]['tours_booked'].sum(),
    'total_applications': sales_data[sales_data['dated'].dt.month == current_month]['applications'].sum(),
    'average_tours_per_lead': sales_data[sales_data['dated'].dt.month == current_month]['tours_per_lead'].mean(),
    'average_apps_per_tour': sales_data[sales_data['dated'].dt.month == current_month]['apps_per_tour'].mean(),
    'average_apps_per_lead': sales_data[sales_data['dated'].dt.month == current_month]['apps_per_lead'].mean(),
    'total_revenue_confirmed': sales_data[sales_data['dated'].dt.month == current_month]['revenue_confirmed'].sum(),
    'total_revenue_pending': sales_data[sales_data['dated'].dt.month == current_month]['revenue_pending'].sum(),
    'average_revenue_runrate': sales_data[sales_data['dated'].dt.month == current_month]['revenue_runrate'].mean(),
    'total_tours_in_pipeline': sales_data[sales_data['dated'].dt.month == current_month]['tours_in_pipeline'].sum(),
    'average_deal_value_30_days': sales_data[sales_data['dated'].dt.month == current_month]['avg_deal_value_30_days'].mean(),
    'average_close_rate_30_days': sales_data[sales_data['dated'].dt.month == current_month]['avg_close_rate_30_days'].mean(),
    'estimated_total_revenue': sales_data[sales_data['dated'].dt.month == current_month]['estimated_revenue'].sum(),
    'total_tours': sales_data[sales_data['dated'].dt.month == current_month]['tours'].sum(),
    'average_tours_runrate': sales_data[sales_data['dated'].dt.month == current_month]['tours_runrate'].mean(),
    'total_tours_scheduled': sales_data[sales_data['dated'].dt.month == current_month]['tours_scheduled'].sum(),
    'total_tours_pending': sales_data[sales_data['dated'].dt.month == current_month]['tours_pending'].sum(),
    'total_tours_cancelled': sales_data[sales_data['dated'].dt.month == current_month]['tours_cancelled'].sum(),
    'average_calls_per_day': (sales_data[sales_data['dated'].dt.month == current_month]['mon_call'] +
                              sales_data[sales_data['dated'].dt.month == current_month]['tue_call'] +
                              sales_data[sales_data['dated'].dt.month == current_month]['wed_call'] +
                              sales_data[sales_data['dated'].dt.month == current_month]['thur_call'] +
                              sales_data[sales_data['dated'].dt.month == current_month]['fri_call'] +
                              sales_data[sales_data['dated'].dt.month == current_month]['sat_call'] +
                              sales_data[sales_data['dated'].dt.month == current_month]['sun_call']) / 7
    }  
     
    print("this is the trend data",trend_data) #Placeholder for debugging
    #Sending data to Groq
    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Analyze the following sales data for the specified time period: {trend_data}. Identify trends and forecast future performance."}
        ],
        model="llama3-8b-8192"  #Groq model name
    )
    print("working6")#Placeholder for debugging
    # Extract feedback from the response
    feedback = response.choices[0].message.content
    return jsonify({'feedback': feedback}) #JSON response containing the feedback from Groq.


if __name__ == '_main_':
    app.run(debug=True)

