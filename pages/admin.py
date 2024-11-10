import streamlit as st
import os
import pandas as pd


def main():
    # Set the title of the dashboard
    st.title("CSV Display Dashboard")

    # Define the path to the CSV file
    csv_file_path = os.path.join("data", "fallback.csv")

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path)

        # Display the original CSV file
        st.header("Original Fallback CSV Data")
        st.dataframe(df)

        # Make a copy so we don't alter the original data
        df_modified = df.copy()

        # Create a Points column based on the Alert column
        def assign_points(alert):
            if pd.isnull(alert) or alert.strip() == "":
                return 0
            elif alert.strip().lower() == "rejected":
                return 1
            elif alert.strip().lower() == "suspicious":
                return 2
            else:
                return 0  # Default to 0 points if alert is unrecognized

        df_modified["Points"] = df_modified["Alert"].apply(assign_points)

        # Group by Email and sum the Points
        df_grouped = (
            df_modified.groupby("Email")
            .agg(
                {
                    "Points": "sum",
                    "Status": "last",
                    "Message": "last",
                    "Alert": lambda x: ", ".join(x.dropna().unique()),
                }
            )
            .reset_index()
        )

        # Sort the dataframe by Points in descending order
        df_grouped = df_grouped.sort_values(by="Points", ascending=False)

        # Display the processed dataframe
        st.header("Processed Data with Points per User")
        st.dataframe(df_grouped)

    else:
        st.error(f"CSV file not found at path: {csv_file_path}")


if __name__ == "__main__":
    main()
