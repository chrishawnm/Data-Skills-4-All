# save the following within a config.toml file
# [server]
# maxUploadSize = 5000
# maxMessageSize = 5000

import streamlit as st
import pandas as pd
import time 
import json
import sqlite3

from pandas_llm import PandasLLM


import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession



st.title("Data Ingestion Tool") 

st.header("Upload your dataset for processing")

spark = SparkSession.builder.getOrCreate()

##------------- initializing -------------------
if "df" not in st.session_state:
    st.session_state["df"] = None

if "result_df" not in st.session_state:
    st.session_state["result_df"] = None

if "df2" not in st.session_state:
    st.session_state["df2"] = None

# Set the max upload size to 1 GB
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

# Define a function to handle the file upload
def upload_file():
    uploaded_file = st.file_uploader("Choose a file",key="1",type='csv')
    if uploaded_file is not None:
        # Do something with the file
        ##st.write("File uploaded successfully!")
        name_str = uploaded_file.name
        df = spark.read.format("csv").option("header","true").load(name_str)
        ##data = pd.read_csv(uploaded_file)
        st.write(df)
        st.session_state["df"] = df
        result_df = df.limit(100000).toPandas()
        st.session_state["result_df"] = result_df
        return result_df,df
    else:
        st.write("No file uploaded.")

# Call the function to upload the file
upload_file()

st.header("Upload the transformations you want to apply")

def click_button():
    st.session_state.clicked = True

def upload_file_transform():
    uploaded_file = st.file_uploader("Choose a file",key="2",type='json')
    if uploaded_file is not None:
        # Do something with the file
        ##st.write("File uploaded successfully!")
        name_str = uploaded_file.name
        with open(name_str, 'r') as f:
            transformations = json.load(f)
            transformations_list = list(transformations.items())
            df_trans = pd.DataFrame.from_dict(transformations)
        st.write(df_trans)


        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        st.button('Apply Transformation',on_click=click_button)
        if st.session_state.clicked:
            
            with st.spinner('Applying Transformation'):
                time.sleep(2)
                for col, trans in transformations_list:
                    if 'map' in trans:
                        try:
                            st.session_state.result_df[col] =st.session_state.result_df[col].map(trans['map'])
                        except:
                            pass
                    elif 'astype' in trans:
                        try:
                            st.session_state.result_df[col] = st.session_state.result_df[col].map(trans['astype'])
                        except:
                            pass
                st.write(st.session_state.result_df)
            st.success('Transformation Applied!')
            
    else:
        st.write("No file uploaded.")

upload_file_transform()

st.header("Data Export to SQL Database")
def click_button_db():
    st.session_state.clicked_db = True

def create_db_table():

    if 'clicked_db' not in st.session_state:
        st.session_state.clicked_db = False

    option = st.selectbox(
    'Select Table',
    ('Create table and insert data','Insert into already existing table'),
    index=None,
    placeholder="Select Table method...",)
    title = st.text_input('Enter Table Name: If New DB (DB & Table Ex. Finance.credit_card_data)')
    

    
    st.button('Update to SQL Database',on_click=click_button_db)
    if st.session_state.clicked_db:
        str_title = str(title)

        if option == 'Create table and insert data':
            with st.spinner('Updating Databse...'):
                conn = sqlite3.connect(str_title.split('.')[0]+'.db')
                st.session_state.result_df.to_sql(str_title.split('.')[1], conn, if_exists='replace', index=False)
                st.success('Table ' + title + ' was updated!')

        else:
            pass
            with st.spinner('Updating Databse...'):
                conn = sqlite3.connect(str_title.split('.')[0]+'.db')
                st.session_state.result_df.to_sql(str_title.split('.')[1], conn, if_exists='append', index=False)
                st.success('Table ' + title + ' was updated!')


create_db_table()

st.header("Data Export to CSV")

def data_export():
    title_export = st.text_input('Enter File Name (excluding .csv)')
    
    if title_export != '':
        st.download_button(
            label="Download data as CSV",
            data=st.session_state.result_df.to_csv().encode('utf-8'),
            file_name= title_export +'.csv',
            mime='text/csv',
        )

data_export()

st.header("Describe sample dataset with ChatGPT API")

def click_button_ai():
    st.session_state.clicked_ai = True

def openai_response():
    if 'clicked_ai' not in st.session_state:
        st.session_state.clicked_ai = False


    openai_api_key= ''
    st.button('Analyze Data Sample',on_click=click_button_ai)
    if st.session_state.clicked_ai:
        conv_df = PandasLLM(data=st.session_state.result_df, llm_api_key = openai_api_key)
        result = conv_df.prompt("how many rows in the dataset")
        time.sleep(5)
        result1 = conv_df.prompt("how many different credit cards")
        time.sleep(5)
        result2 = conv_df.prompt("how many different users")
        time.sleep(5)
        result3 = conv_df.prompt("which user has the most credit card transactions and how many")
        time.sleep(5)
        result4 = conv_df.prompt("what's the earliest and latest transaction date")
        list_results = ['There are '+ str(result) + ' results.',
                        'There are ' + str(result1) + ' different credit cards in the 10,0000 records.',
                        'There are ' + str(result2) + ' different users in the 10,000 records',
                        'The user that has the most is and with the following # of transactions: ' + str(result3),
                        'The earliest and latest transactions are the following: ' + str(result4)]
        st.session_state.df2 = list_results
        st.write(st.session_state.df2)
        
            
openai_response()
