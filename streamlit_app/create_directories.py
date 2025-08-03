import os
from pathlib import Path

def create_required_directories():
    """Create all required directories for the application."""
    # List of directories to create
    directories = [
        "uploads",
        "generated",
        "templates",
        "static/css",
        "static/js"
    ]
    
    # Create each directory if it doesn't exist
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path.absolute()}")
    
    # Create .gitkeep files in empty directories
    for dir_path in ["uploads", "generated"]:
        gitkeep = Path(dir_path) / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
            print(f"Created file: {gitkeep.absolute()}")
    
    print("\nDirectory setup complete!")

if __name__ == "__main__":
    create_required_directories()
