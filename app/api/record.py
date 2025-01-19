"""
CRUD API endpoints for managing backend_table.csv.
Includes error handling and backup management.
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.models.random_number import ExcelRecord
from app.services.file_service import read_csv, write_to_csv, delete_from_csv, create_backup,update_csv_row
from app.services.auth_service import get_current_user

router = APIRouter()
CSV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend_table.csv"))

@router.get("/", summary="Fetch all records from the CSV file")
def fetch_records(user=Depends(get_current_user)):
    """
    Reads all records from the CSV file and returns them.
    Returns:
        list: A list of dictionaries representing the records in the CSV file.
    Raises:
        HTTPException: If an unexpected error occurs during the read operation.
    """
    try:
        return read_csv()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching records: {e}")


@router.get("/download/", summary="Download the backend_table.csv file")
def download_csv(username=Depends(get_current_user)):
    """
    Allows authenticated users to download the backend_table.csv file.
    Args:
        username (str): The username extracted from the token for authentication.
    Returns:
        FileResponse: A downloadable CSV file.
    Raises:
        HTTPException: If the file does not exist.
    """
    if not os.path.exists(CSV_FILE_PATH):
        raise HTTPException(status_code=404, detail="File not found")

    # Log the user accessing the file
    print(f"User {username} is downloading the file.")

    return FileResponse(
        path=CSV_FILE_PATH,
        media_type="text/csv",
        filename="backend_table.csv"
    )

@router.post("/", summary="Add a new record for the current user")
def add_record(record: ExcelRecord, username: str = Depends(get_current_user)):
    print("hello")
    print("Endpoint hit: add_record")  # Debugging
    print(f"Username: {username}")  # Debugging

    try:
        # Debugging: Print the record before processing
        print(f"Record before adding user: {record.dict(by_alias=True)}")

        # Associate the user with the record
        record_dict = record.dict(by_alias=True)
        record_dict["user"] = username

        # Debugging: Print the final record
        print(f"Final record with user: {record_dict}")

        # Backup and write to CSV
        create_backup()
        write_to_csv(record_dict)

        return {"message": "Record added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid record format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding record: {e}")


@router.put("/{id}/", summary="Update a record by ID")
def update_record(
    id: int,
    updated_record: ExcelRecord,
    username: str = Depends(get_current_user)
):
    print(f"Endpoint hit: update_record for ID: {id}")  # Debugging
    print(f"Username: {username}")  # Debugging

    try:
        # Debugging: Print the record before processing


        # Update the CSV row based on the ID
        updated_record_dict = updated_record.dict(by_alias=True)
        updated_record_dict["user"] = username

        create_backup()
        update_csv_row(id, updated_record_dict)

        return {"message": f"Record with ID {id} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid record format: {e}")
    except IndexError as e:
        raise HTTPException(status_code=404, detail=f"Record with ID {id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating record: {e}")


@router.delete("/{record_id}/", summary="Delete a record from the CSV file")
def delete_record(record_id: int, user=Depends(get_current_user)):
    """
    Deletes a record from the CSV file by its index.
    Args:
        record_id (int): The index of the record to delete.
    Returns:
        dict: A success message upon successful deletion.
    Raises:
        HTTPException: If the record ID is invalid or an error occurs during deletion.
    """
    try:
        records = read_csv()

        if record_id < 0 or record_id >= len(records):
            raise HTTPException(status_code=404, detail="Record not found")

        create_backup()
        delete_from_csv(record_id)
        return {"message": "Record deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting record: {e}")

# Fetch a specific record by ID
@router.get("/{record_id}/", summary="Fetch a specific record by its ID from the CSV file")
def fetch_record_by_id(record_id: int, user=Depends(get_current_user)):
    try:
        records = read_csv()
        if record_id < 0 or record_id >= len(records):
            raise HTTPException(status_code=404, detail="Record not found")
        return records[record_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching record: {e}")