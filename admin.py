import streamlit as st
import os
import pandas as pd

def main():
    # Set the title of the dashboard
    st.title('Fallback CSV Display Dashboard')

    # Define the path to the CSV file
    csv_file_path = os.path.join('database', 'fallback.csv')

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path)
        
        # Display the dataframe on the Streamlit dashboard
        st.write("Here is the content of fallback.csv:")
        st.dataframe(df)  # Displays the dataframe in an interactive table
    else:
        st.error("The file fallback.csv was not found in the database folder.")

if __name__ == "__main__":
    main()
