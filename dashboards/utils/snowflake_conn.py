import streamlit as st
import snowflake.connector
import pandas as pd

@st.cache_resource
def get_snowflake_connection():
    """Create and cache Snowflake connection"""
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

@st.cache_data(ttl=600)  # Cache for 10 minutes
def run_query(query):
    """Execute query and return results as DataFrame"""
    conn = get_snowflake_connection()
    return pd.read_sql(query, conn)