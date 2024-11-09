import json
import pandas as pd
from datetime import datetime, timedelta


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


def update_fallback_csv(email, status, message, alert=""):
    """
    Update the 'data/fallback.csv' with the customer's verification attempt.
    Email is the primary key, status indicates verification result.
    """
    try:
        # Load existing fallback.csv if it exists
        fallback_path = "data/fallback.csv"
        fallback_df = (
            pd.read_csv(fallback_path)
            if pd.io.common.file_exists(fallback_path)
            else pd.DataFrame(columns=["Email", "Status", "Message", "Alert"])
        )

        # Create new data entry
        new_data = pd.DataFrame(
            {
                "Email": [email],
                "Status": [status],
                "Message": [message],
                "Alert": [alert],
            }
        )

        # Remove existing entry with same email if exists
        fallback_df = fallback_df[fallback_df["Email"] != email]

        # Append new data
        fallback_df = pd.concat([fallback_df, new_data], ignore_index=True)
        fallback_df.to_csv(fallback_path, index=False)
    except Exception as e:
        print(f"Error updating fallback.csv: {e}")


def verify_user_data(email):
    """
    Verify user data from the JSON in the passport.md file and compare it with the database.
    """
    passport_md_path = "output_test/passport.md"
    customer_data_path = "data/customer_data.csv"

    # Extract JSON data from the .md file
    json_data = extract_json_from_md(passport_md_path)
    if not json_data:
        update_fallback_csv(
            email, "failure", "Failed to extract data from .md file.", "rejected"
        )
        return {"status": "failure", "message": "Failed to extract data from .md file."}

    # Load customer data
    try:
        customer_df = pd.read_csv(customer_data_path)
    except Exception as e:
        print(f"Error loading customer data: {e}")
        update_fallback_csv(
            email, "failure", "Customer database inaccessible.", "rejected"
        )
        return {"status": "failure", "message": "Customer database inaccessible."}

    # Check if the customer email exists in the database
    customer = customer_df.loc[customer_df["Email"] == email]
    if customer.empty:
        update_fallback_csv(
            email, "failure", "Email not found in database.", "rejected"
        )
        return {"status": "failure", "message": "Email not found in database."}

    customer_info = customer.iloc[0]

    # 1. Compare full_name
    if (
        json_data.get("full_name", "").strip().lower()
        == customer_info["Name"].strip().lower()
    ):
        update_fallback_csv(email, "success", "Name matches.", "")
        status_response = {"status": "success", "message": "Name matches."}
    else:
        update_fallback_csv(email, "failure", "Name does not match.", "Suspicious")
        return {"status": "failure", "message": "Name does not match."}

    # 2. Check passport expiry date
    try:
        expiry_date = datetime.strptime(json_data.get("expiry_date", ""), "%Y-%m-%d")
        if expiry_date < datetime.now() + timedelta(days=180):
            update_fallback_csv(
                email, "failure", "Passport expiring soon or expired.", "rejected"
            )
            return {
                "status": "failure",
                "message": "Passport expiring soon or expired.",
            }
    except ValueError:
        update_fallback_csv(email, "failure", "Invalid expiry date format.", "rejected")
        return {"status": "failure", "message": "Invalid expiry date format."}

    # 3. Calculate age
    try:
        dob = datetime.strptime(json_data.get("DOB", ""), "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            update_fallback_csv(
                email, "failure", "Does not meet age requirement.", "rejected"
            )
            return {"status": "failure", "message": "Does not meet age requirement."}
    except ValueError:
        update_fallback_csv(
            email, "failure", "Invalid date of birth format.", "rejected"
        )
        return {"status": "failure", "message": "Invalid date of birth format."}

    return status_response


# Example usage
email_from_frontend = "user@example.com"  # This is the email input from the frontend

result = verify_user_data(email_from_frontend)
print(result)
