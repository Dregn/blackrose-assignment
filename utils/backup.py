"""
Utility for managing file backups and recovery.
"""

import shutil

def create_backup(file_path: str, backup_path: str):
    """
    Creates a backup of the given file.
    """
    shutil.copy(file_path, backup_path)

def restore_backup(backup_path: str, file_path: str):
    """
    Restores a file from its backup.
    """
    shutil.copy(backup_path, file_path)
