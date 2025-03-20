import os
import shutil
from datetime import datetime
from collections import defaultdict

def get_creation_date(file_path):
    return datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d")

def get_destination_folder(file_extension):
    file_types = {
        "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"},
        "documents": {".pdf", ".zip", ".html", ".py", ".txt", ".docx", ".xlsx"},
        "videos": {".mp4", ".mkv", ".avi", ".mov"},
        "music": {".mp3", ".wav", ".flac"}
    }
    
    for category, extensions in file_types.items():
        if file_extension in extensions:
            return category
    return "others"

def sort_files(base_folder):
    destination_folders = {
        "images": r"C:\\Users\\nicop\\Pictures",
        "documents": r"C:\\Users\\nicop\\Documents",
        "videos": r"C:\\Users\\nicop\\Videos",
        "music": r"C:\\Users\\nicop\\Music",
        "others": r"C:\\Users\\nicop\\Documents\\Others"
    }
    
    files_by_date_and_type = defaultdict(list)
    file_extensions_by_date_and_type = defaultdict(set)
    
    for file in os.listdir(base_folder):
        file_path = os.path.join(base_folder, file)
        
        if os.path.isfile(file_path):
            creation_date = get_creation_date(file_path)
            file_extension = os.path.splitext(file)[-1].lower()
            category = get_destination_folder(file_extension)
            
            files_by_date_and_type[(creation_date, category)].append(file_path)
            file_extensions_by_date_and_type[(creation_date, category)].add(file_extension.strip('.'))
    
    for (creation_date, category), files in files_by_date_and_type.items():
        dest_base = destination_folders.get(category, destination_folders["others"])
        extensions_note = "+".join(sorted(file_extensions_by_date_and_type[(creation_date, category)]))
        folder_name = f"{creation_date} ({extensions_note})"
        date_folder = os.path.join(dest_base, folder_name)
        
        os.makedirs(date_folder, exist_ok=True)
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(date_folder, file_name)
            
            shutil.move(file_path, dest_path)
            print(f"Moved: {file_path} -> {dest_path}")

if __name__ == "__main__":
    download_folder = r"C:\\Users\\nicop\\Downloads"
    sort_files(download_folder)
