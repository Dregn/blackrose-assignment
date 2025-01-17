"""
File service for reading, writing, and managing backend_table.csv.
Includes error handling and file backup functionality.
"""

import pandas as pd
from app.utils.lock import lock_file
import shutil
import os

CSV_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend_table.csv"))
BACKUP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend_table_backup.csv"))



def read_csv():
    """
    Reads all records from the CSV file and returns them as a list of dictionaries.
    Ensures the file exists before reading and adds sequential IDs to rows without one.
    Returns:
        list: A list of dictionaries representing the records in the CSV file.
    """
    try:
        # Ensure file exists before attempting to read
        if not os.path.exists(CSV_FILE):
            return []

        with lock_file(CSV_FILE):
            df = pd.read_csv(CSV_FILE)

        # Add a sequential 'id' column if it doesn't exist
        if "id" not in df.columns:
            df["id"] = range(0, len(df))

        # Ensure all rows have a valid sequential ID
        df["id"] = pd.Series(range(0, len(df)))

        return df.to_dict(orient="records")
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        # Handle empty CSV file
        return []
    except Exception as e:
        # Generic error handling
        raise RuntimeError(f"Error reading CSV file: {e}")


def write_to_csv(record: dict):
    """
    Appends a new record to the CSV file.
    Ensures the record format matches the schema before adding.
    Args:
        record (dict): The record to append to the CSV file.
    """
    try:
        if not os.path.exists(CSV_FILE):
            # Create a new DataFrame with the record
            df = pd.DataFrame([record])
        else:
            with lock_file(CSV_FILE):
                # Read the existing data
                df = pd.read_csv(CSV_FILE)
                # Create a DataFrame from the new record
                new_record_df = pd.DataFrame([record])
                # Validate column names and structure
                if not all(col in df.columns for col in new_record_df.columns):
                    raise ValueError("Record structure does not match the existing CSV format")
                # Concatenate the new record with the existing DataFrame
                df = pd.concat([df, new_record_df], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        with lock_file(CSV_FILE):
            df.to_csv(CSV_FILE, index=False)
    except Exception as e:
        raise RuntimeError(f"Error writing to CSV file: {e}")


def delete_from_csv(record_id: int):
    """
    Deletes a record from the CSV file by its index.
    Ensures the file is properly locked and handles errors during deletion.
    Args:
        record_id (int): The index of the record to delete.
    Raises:
        ValueError: If the record ID is invalid or not found.
    """
    try:
        with lock_file(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            if record_id < 0 or record_id >= len(df):
                raise ValueError(f"Record with ID {record_id} not found")
            # Drop the record by index
            df = df.drop(index=record_id)
            df.reset_index(drop=True, inplace=True)
            df.to_csv(CSV_FILE, index=False)
    except FileNotFoundError:
        raise ValueError("CSV file not found")
    except Exception as e:
        raise RuntimeError(f"Error deleting from CSV file: {e}")

def update_csv_row(row_id: int, updated_record: dict):
    """
    Updates a specific row in the CSV file based on the row ID.
    Ensures the record format matches the schema before updating.
    
    Args:
        row_id (int): The ID of the row to update (zero-based index).
        updated_record (dict): The updated record data.
    """
    try:
        if not os.path.exists(CSV_FILE):
            raise IndexError(f"CSV file not found. Cannot update row with ID {row_id}.")

        with lock_file(CSV_FILE):
            # Read the existing data
            df = pd.read_csv(CSV_FILE)

            # Check if the ID exists
            if row_id < 0 or row_id >= len(df):
                raise IndexError(f"Row ID {row_id} is out of bounds.")

            # Validate column names and structure
            if not all(col in df.columns for col in updated_record.keys()):
                raise ValueError("Record structure does not match the existing CSV format")

            # Update the specific row
            for key, value in updated_record.items():
                df.at[row_id, key] = value
            print("writ to csv")
            # Write the updated DataFrame back to the CSV file
            df.to_csv(CSV_FILE, index=False)

    except Exception as e:
        print(f"Error updating CSV row: {e}")
        raise RuntimeError(f"Error updating CSV row: {e}")


def create_backup():
    """
    Creates a backup of the CSV file.
    Ensures the backup file is safely created and handles errors during the process.
    """
    try:
        print(CSV_FILE)
        if not os.path.exists(CSV_FILE):
            raise FileNotFoundError("Cannot create backup; CSV file does not exist")
        with lock_file(CSV_FILE):
            if os.path.exists(CSV_FILE):
                shutil.copy(CSV_FILE, BACKUP_FILE)
            else:
                raise FileNotFoundError("Cannot create backup; CSV file does not exist")
    except Exception as e:
        raise RuntimeError(f"Error creating backup: {e}")
