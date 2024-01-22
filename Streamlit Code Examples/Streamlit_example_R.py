#streamlit/openAI lib packages
import openai
import streamlit as st

#langchain api packages
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain import OpenAI, SQLDatabase

#database
import sqlite3
import pandas as pd

#---------------- User Input API key + how to ------------------------------

with st.sidebar:
    user_openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

#--------------------  Database Creation -----------------------------------
#If you want to create the database uncomment the following code

#read the data into pandas dataframes
#df = pd.read_csv('BigSupplyCo_Categories.csv', encoding='iso-8859-1')
#df1 = pd.read_csv('BigSupplyCo_Customers.csv', encoding='iso-8859-1')
#df2 = pd.read_csv('BigSupplyCo_Departments.csv', encoding='iso-8859-1')
#df3 = pd.read_csv('BigSupplyCo_Orders.csv', encoding='iso-8859-1')
#df4 = pd.read_csv('BigSupplyCo_Products.csv', encoding='iso-8859-1')

#connect and create a sql lite database
#conn = sqlite3.connect('Retail_Challenge.db')

#store your pandas dataframes as tables in the sql lite databse
#df.to_sql('BigSupplyCo_Categories', conn, if_exists='replace', index=False)
#df1.to_sql('BigSupplyCo_Customers', conn, if_exists='replace', index=False)
#df2.to_sql('BigSupplyCo_Departments', conn, if_exists='replace', index=False)
#df3.to_sql('BigSupplyCo_Orders', conn, if_exists='replace', index=False)
#df4.to_sql('BigSupplyCo_Products', conn, if_exists='replace', index=False)


#---------------------- Connect API to SQL Lite Database ------------------------

db = SQLDatabase.from_uri("sqlite:///Retail_Challenge.db")

#---------------------- Streamlit App UX Design ------------------------------

st.title("Retail Database Query Chatbot") 
st.caption("Welcome to my streamlit app where you can query data from our company retail store database. Please note no DML operations can be completed")

if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input('What would you like to know from the Retail Database?', key="Qs"):

    prompt_str = prompt
    if not user_openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    st.session_state['user_question'] = prompt

    chain = create_sql_query_chain(ChatOpenAI(temperature=0,openai_api_key=user_openai_api_key), db)
    
    x=0
    dml_operations = ['insert','update','delete','merge','upsert','transactions']
    for word in dml_operations:
        if word in prompt.lower():
            x=x+1
            break

    if x > 0:
        st.chat_message("assistant").write("Can't perform DML operations besides select statements.")

    else:     
        response = chain.invoke({"question": prompt})
        st.chat_message("user").write(prompt)


        my_list = eval(db.run(response))
        df = pd.DataFrame(my_list)
        st.chat_message("assistant").write(df)
        #st.chat_message("assistant").write(response)
       
on = st.toggle('Show Code')

if on:
    my_new_string = st.session_state['user_question']
    chain = create_sql_query_chain(ChatOpenAI(temperature=0,openai_api_key=user_openai_api_key), db)
    response = chain.invoke({"question": my_new_string})

    st.chat_message("assistant").write(response)

