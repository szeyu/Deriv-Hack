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
    Adds DateTime column with current datetime.
    """
    try:
        from datetime import datetime

        # Load existing fallback.csv if it exists
        fallback_path = "data/fallback.csv"
        if pd.io.common.file_exists(fallback_path):
            fallback_df = pd.read_csv(fallback_path)
        else:
            fallback_df = pd.DataFrame(
                columns=["Email", "DateTime", "Status", "Message", "Alert"]
            )

        # Get current datetime in the format 'YYYY-MM-DD HH:MM:SS'
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create new data entry
        new_data = pd.DataFrame(
            {
                "Email": [email],
                "DateTime": [current_datetime],
                "Status": [status],
                "Message": [message],
                "Alert": [alert],
            }
        )

        # Append new data without removing previous entries
        fallback_df = pd.concat([fallback_df, new_data], ignore_index=True)

        # Save updated fallback.csv
        fallback_df.to_csv(fallback_path, index=False)
    except Exception as e:
        print(f"Error updating fallback.csv: {e}")


def verify_user_data(email):
    """
    Verify user data from the JSON in the identity.md file and compare it with the database.
    """
    identity_md_path = "output_test/identity.md"
    customer_data_path = "data/customer_data.csv"

    # Extract JSON data from the .md file
    json_data = extract_json_from_md(identity_md_path)
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
        status_response = {
            "status": "success",
            "message": "Passport name matches & age requirements met.",
        }
    else:
        update_fallback_csv(email, "failure", "Passport name mismatch.", "Suspicious")
        return {"status": "failure", "message": "Passport name mismatch.."}

    # 2. Check identity expiry date
    try:
        expiry_date = datetime.strptime(json_data.get("expiry_date", ""), "%Y-%m-%d")
        if expiry_date < datetime.now() + timedelta(days=180):
            update_fallback_csv(
                email, "failure", "identity expiring soon or expired.", "rejected"
            )
            return {
                "status": "failure",
                "message": "identity expiring soon or expired.",
            }
    except ValueError:
        # update_fallback_csv(email, "failure", "Invalid expiry date format.", "rejected")
        # return {"status": "failure", "message": "Invalid expiry date format."}
        pass  # Ignore invalid expiry date format

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


def verify_user_data_2(email):
    """
    Verify bank statement data against customer database.
    """
    bank_statement_md_path = "output_test/bank_statement.md"
    customer_data_path = "data/customer_data.csv"

    # Extract JSON data from bank statement
    json_data = extract_json_from_md(bank_statement_md_path)
    if not json_data:
        update_fallback_csv(
            email, "failure", "Failed to extract data from bank statement.", "rejected"
        )
        return {
            "status": "failure",
            "message": "Failed to extract data from bank statement.",
        }

    # Load customer data
    try:
        customer_df = pd.read_csv(customer_data_path)
    except Exception as e:
        print(f"Error loading customer data: {e}")
        update_fallback_csv(
            email, "failure", "Customer database inaccessible.", "rejected"
        )
        return {"status": "failure", "message": "Customer database inaccessible."}

    # Check if customer exists
    customer = customer_df.loc[customer_df["Email"] == email]
    if customer.empty:
        update_fallback_csv(
            email, "failure", "Email not found in database.", "rejected"
        )
        return {"status": "failure", "message": "Email not found in database."}

    customer_info = customer.iloc[0]

    # Compare account holder name
    if (
        json_data.get("account_holder_name", "").strip().lower()
        != customer_info["Name"].strip().lower()
    ):
        update_fallback_csv(
            email, "failure", "Account holder name does not match.", "Suspicious"
        )
        return {
            "status": "failure",
            "message": "Account holder name does not match.",
            "alert": "Suspicious",
        }

    # Compare address
    if (
        json_data.get("address", "").strip().lower()
        != customer_info["Address"].strip().lower()
    ):
        update_fallback_csv(
            email,
            "failure",
            "Address does not match.",
            "Rejected (Contact Support to update address)",
        )
        return {
            "status": "failure",
            "message": "Address does not match.",
            "alert": "Rejected (Contact Support to update address)",
        }

    # If all checks pass
    update_fallback_csv(email, "success", "Bank statement verified successfully.", "")
    return {"status": "success", "message": "Bank statement verified successfully."}


def sucess_bank_statement_fallback(email, bank_name):
    """
    update the fallback CSV after successfully verifying bank statement.
    """
    # Here you can add more specific checks for the bank statement if needed
    update_fallback_csv(
        email, "success", f"Bank statement from {bank_name} verified.", ""
    )
    return {
        "status": "success",
        "message": f"Bank statement from {bank_name} verified.",
    }


def invalid_bank_statement_fallback(email):
    """
    update the fallback CSV if there is an error on verifying bank statement.
    """
    update_fallback_csv(
        email, "failure", "Error verifying bank statement.", "Suspicious"
    )
    return {"status": "failure", "message": "Error verifying bank statement."}


# Example usage
# email_from_frontend = "user@example.com"  # This is the email input from the frontend

# result = verify_user_data(email_from_frontend)
# print(result)
