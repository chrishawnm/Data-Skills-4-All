In my data engineering fellowship I created two streamlit applications of varying difficulty that showcased my knowledge and understanding of the following:

Tech Stack
- Streamlit for Web Application Framework
- Python for data transformations (pandas library)
- SQL for Data Storage (Cloud hosted)
- OpenAI GPT API to get quick Data Insights

First Challenge (R) [Dataset](https://pages.github.com/)
- Design and develop a chatbot in Streamlit that can interact with a database. You should upload the CSV files into a database (locally or Cloud) and create the corresponding tables. 
- Enable the chatbot to answer questions related to sales, marketing, and production. It should create a query that might respond to the answer and run it on the database. 
- Restrict DML operations such as DELETE, UPDATE, and so on).
- Implement a feature to display the SQL query used to fetch the data for answering the questions.
- Display the relevant data in a data frame within the Streamlit app.
- Ensure the chatbot is user-friendly and intuitive using the Streamlit chat widget.

To Run (streamlit example R)
   - download csv files
   - run commented out code in your python ide starting in lines 24 to 38 this will create the pandas dataframes that then are ingested into a local sqlite database
   - open terminal and navigate to the folder where streamlit python file was downloaded and make sure the local database is saved in the same folder
   - run the following command streamlit_example_r.py
   - a browser window will show up with the application

![Image Alt text](/images/Streamlit_example_R.png "Optional title")  

Second Challenge (F)

1. Develop a User-Friendly Data Ingestion Interface
 - Enable users to upload Parquet files through a simple drag-and-drop interface.
 - Provide real-time validation and error handling to ensure only compatible files are uploaded.
 - Implement a preview feature to display the first few rows of the dataset immediately after upload.

2. Facilitate Customizable Data Transformation
 - Allow users to upload a JSON file containing specific data transformation rules, such as field cleansing and data type parsing.
 - Implement a one-click transformation feature to apply multiple rules simultaneously.
 - Display the transformed data in a side-by-side comparison with the original data for immediate validation.

3. Implement Quick and Insightful Data Analysis
 - Integrate the OpenAI ChatGPT API to analyze uploaded datasets automatically.
 - Provide summarized insights and recommendations based on the analysis.
 - Offer options for users to select the type of analysis they want to perform, such as descriptive statistics or trend analysis.

4. Ensure Seamless SQL Database Integration
 - Implement a feature that allows users to connect to their SQL databases directly from the application.
 - Provide options for creating new database tables or appending data to existing tables.
 - Include robust error handling and data validation features to ensure that only clean, transformed data is inserted into the database.

 To Run (streamlit example F)
   - download streamlit python file
   - in your .streamlit folder config.toml make sure you add the following to account for parquet file size issues:
        [server]
        maxUploadsSize = 5000
        maxMessageSize = 5000
   - navigate to the folder where you downloaded the file and run the following command streamlit_example_f.py
   - a browser window will show up with the application
   - download csv files from read in second challenge section
   - upload those files to application
   - upload [Transformation File](https://github.com/chrishawnm/Data-Skills-4-All/blob/main/Streamlit_example_F_transformations.json) to the streamlit app where specified


![Image Alt text](/images/streamlit_example_f_DE.png "Optional title")


![Image Alt text](/images/Streamlit_example_F.png "Optional title")
