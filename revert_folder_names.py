import os
import re

def revert_folder_names(base_path):
    folder_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \(.*?\)) - .+$")
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        
        match = folder_pattern.match(folder)
        if os.path.isdir(folder_path) and match:
            original_name = match.group(1)  # Nur den ursprünglichen Ordnernamen extrahieren
            new_folder_path = os.path.join(base_path, original_name)
            
            if os.path.exists(folder_path) and not os.path.exists(new_folder_path):
                try:
                    os.rename(folder_path, new_folder_path)
                    print(f"Umbenannt: {folder} -> {original_name}")
                except Exception as e:
                    print(f"Fehler beim Umbenennen von {folder}: {e}")
            else:
                print(f"Übersprungen (nicht vorhanden oder Ziel existiert bereits): {folder}")

base_directory = "C:\\Users\\nicop\\Documents"
revert_folder_names(base_directory)
