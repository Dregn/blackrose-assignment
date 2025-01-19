"""
Utility for file locking to ensure safe concurrent access.
"""

from filelock import FileLock

def lock_file(file_path: str):
    """
    Returns a context manager for locking a file.
    """
    return FileLock(f"{file_path}.lock")
