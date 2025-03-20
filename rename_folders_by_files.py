import os
import re

def sanitize_filename(filename):
    # Erlaubte Zeichen: Buchstaben, Zahlen, Leerzeichen, -, _, +, .
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def rename_folders_by_files(base_path):
    folder_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \(.*\)$")
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        
        if os.path.isdir(folder_path) and folder_pattern.match(folder):
            files = os.listdir(folder_path)
            
            if files:
                # Trennen der Dateinamen mit "+"
                file_names = "+".join(os.path.splitext(f)[0] for f in files)
                new_folder_name = f"{folder} - {file_names}"
                
                # Maximale Länge für Windows begrenzen
                max_length = 255
                if len(new_folder_name) >= max_length:
                    file_names = file_names[:max_length - len(folder) - 10] + "..."
                    new_folder_name = f"{folder} - {file_names}"
                
                # Entfernen von ungültigen Zeichen
                new_folder_name = sanitize_filename(new_folder_name)
                
                new_folder_path = os.path.join(base_path, new_folder_name)
                
                if os.path.exists(folder_path):
                    try:
                        os.rename(folder_path, new_folder_path)
                        print(f"Umbenannt: {folder} -> {new_folder_name}")
                    except Exception as e:
                        print(f"Fehler beim Umbenennen von {folder}: {e}")
                else:
                    print(f"Übersprungen (nicht mehr vorhanden): {folder}")
            else:
                print(f"Übersprungen (Leer): {folder}")

base_directory = "C:\\Users\\nicop\\Documents"
rename_folders_by_files(base_directory)
