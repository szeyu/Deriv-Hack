import json
import pandas as pd


def extract_json_from_md(file_path):
    """
    Extract JSON data from a markdown (.md) file.
    """
    try:
        with open(file_path, "r") as md_file:
            content = md_file.read()
            start_index = content.find("{")
            end_index = content.rfind("}") + 1
            if start_index == -1 or end_index == -1:
                raise ValueError("No JSON data found in the .md file.")
            json_data = content[start_index:end_index]
            return json.loads(json_data)
    except Exception as e:
        print(f"Error processing the file: {e}")
        return None


def update_fallback_csv(customer_id, verification_status, message):
    """
    Update the 'fallback.csv' with the customer's verification attempt.
    """
    try:
        # Load existing fallback.csv if it exists
        fallback_df = (
            pd.read_csv("fallback.csv")
            if pd.io.common.file_exists("fallback.csv")
            else pd.DataFrame(columns=["Customer_ID", "Verification_Status", "Message"])
        )

        # Append new data
        new_data = pd.DataFrame(
            {
                "Customer_ID": [customer_id],
                "Verification_Status": [verification_status],
                "Message": [message],
            }
        )

        fallback_df = pd.concat([fallback_df, new_data], ignore_index=True)
        fallback_df.to_csv("fallback.csv", index=False)
    except Exception as e:
        print(f"Error updating fallback.csv: {e}")


def verify_user_data(email, md_file_path, customer_database):
    """
    Verify user data from the JSON in the markdown file and compare it with the database.
    """
    # Extract JSON data from the .md file
    json_data = extract_json_from_md(md_file_path)
    if not json_data:
        return {"status": "failure", "message": "Failed to extract data from .md file."}

    # Check if the customer email exists in the database
    customer = customer_database.get(email)
    if not customer:
        return {"status": "failure", "message": "Email not found in database."}

    # Compare extracted name with database entry
    if json_data["full_name"] == customer["full_name"]:
        # Success: Update fallback.csv and return response
        update_fallback_csv(customer["customer_id"], "success", "Name matches.")
        return {"status": "success", "message": "Name matches."}
    else:
        # Failure: Update fallback.csv and return response
        update_fallback_csv(customer["customer_id"], "failure", "Name does not match.")
        return {"status": "failure", "message": "Name does not match."}


# Example customer database (simulate as a dictionary)
customer_database = {
    "user@example.com": {
        "customer_id": "A001",
        "full_name": "SIM SZE YU",
        "dob": "2004-04-17",
        "nationality": "MALAYSIA",
        "expiry_date": "2028-04-21",
    }
}

# Example usage
email_from_frontend = "user@example.com"  # This is the email input from the frontend
md_file_path = "passport_data.md"  # The path to the .md file

result = verify_user_data(email_from_frontend, md_file_path, customer_database)
print(result)
