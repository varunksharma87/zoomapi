import os
import requests
import csv
from zoom_oauth import check_access_token

def delete_phone_numbers(phone_numbers, results):
    """Deletes a batch of phone numbers using the Zoom API and updates results."""
    access_token = check_access_token()
    
    phone_numbers_str = ",".join(phone_numbers)
    endpoint = f'https://api.zoom.us/v2/phone/numbers?phone_numbers={phone_numbers_str}'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    print(f"🔹 Sending DELETE request for: {phone_numbers}")
    response = requests.delete(endpoint, headers=headers)
    response_code = response.status_code

    if response_code in [200, 204]:  # Success cases
        print(f"✅ Successfully deleted batch: {phone_numbers}")
        for number in phone_numbers:
            results[number] = {
                "Response": response_code,
                "Result": "Success",
                "Remarks": "Successfully Deleted."
            }
    else:  # Failure case
        print(f"❌ Failed to delete batch: {phone_numbers}")
        print(f"   ⚠️ Error {response_code}: {response.text}")

        error_messages = {}  # Store error messages for each phone number
        
        try:
            error_json = response.json()
            if "errors" in error_json:
                for err in error_json["errors"]:
                    field_value = err.get("field_value", "Unknown")
                    message = err.get("message", "No detailed message provided.")
                    if field_value not in error_messages:
                        error_messages[field_value] = message  # Map phone number to its specific error

        except Exception as e:
            print(f"⚠️ JSON parsing error: {e}")

        # Assign error messages to corresponding phone numbers
        for number in phone_numbers:
            normalized_number = number.lstrip("+")  # Remove '+' for consistency
            results[number] = {
                "Response": response_code,
                "Result": "Failed",
                "Remarks": error_messages.get(normalized_number, "Unknown API Error")
            }

def process_csv_batches(csv_file, batch_size=2):
    """Reads phone numbers from CSV, processes them in batches, and updates the CSV."""
    phone_numbers = []
    results = {}

    print(f"📂 Reading CSV file: {csv_file}")

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        
        # Ensure new columns are added only if they don’t already exist
        new_columns = ["Response", "Result", "Remarks"]
        fieldnames = reader.fieldnames if all(col in reader.fieldnames for col in new_columns) else reader.fieldnames + new_columns
        
        rows = list(reader)  # Store all rows in memory

    for row in rows:
        phone_number = row["PhoneNumber"]
        phone_numbers.append(phone_number)
        results[phone_number] = {"Response": "", "Result": "", "Remarks": ""}  # Default values

    print(f"📊 Total phone numbers found: {len(phone_numbers)}")

    batch_count = 0
    for i in range(0, len(phone_numbers), batch_size):
        batch = phone_numbers[i:i + batch_size]
        batch_count += 1
        print(f"\n🚀 Processing Batch {batch_count}: {batch}")
        delete_phone_numbers(batch, results)  # Send DELETE request

    print("\n💾 Updating CSV file with response details...")
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            phone_number = row["PhoneNumber"]
            row.update(results.get(phone_number, {}))  # Merge results into original rows
            writer.writerow(row)

    print("✅ CSV file updated successfully.")

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "phonenumbers.csv")

process_csv_batches(csv_file_path, batch_size=2)
