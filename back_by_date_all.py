import os
import shutil
import datetime
import socket
import sys
import subprocess

def list_external_drives():
    drives = []
    for drive in range(ord('D'), ord('Z') + 1):
        drive_letter = f"{chr(drive)}:\\"
        if os.path.exists(drive_letter):
            try:
                total, used, free = shutil.disk_usage(drive_letter)
                if free > 10 * (1024**3):  # 10 GB free space check
                    drives.append(drive_letter)
            except:
                pass
    return drives

def select_drive(drives):
    print("Available external drives:")
    for idx, drive in enumerate(drives):
        print(f"{idx + 1}. {drive}")
    choice = int(input("Select the drive number to backup to: ")) - 1
    return drives[choice]

def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
            except FileNotFoundError:
                pass  # Skip missing files during scan
    return total_size

def human_readable_size(size_bytes):
    return f"{size_bytes / (1024**3):.2f} GB"

def estimate_time(size_bytes, speed_mbps=100):
    # Speed in MB/s
    size_mb = size_bytes / (1024 * 1024)
    estimated_seconds = size_mb / speed_mbps
    return f"{int(estimated_seconds // 60)} min {int(estimated_seconds % 60)} sec"

def teracopy_copy(source, dest):
    teracopy_path = r"C:\Program Files\TeraCopy\TeraCopy.exe"
    if not os.path.exists(teracopy_path):
        print("❌ TeraCopy not found! Please check the path.")
        sys.exit(1)
    cmd = f'"{teracopy_path}" Copy "{source}" "{dest}" /OverwriteAll /Close'
    print(f"▶️ Starting TeraCopy: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    pc_name = socket.gethostname()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    user = os.getlogin()

    folders_to_backup = {
        'Downloads': f"C:\\Users\\{user}\\Downloads",
        'Documents': f"C:\\Users\\{user}\\Documents",
        'Pictures': f"C:\\Users\\{user}\\Pictures",
        'Videos': f"C:\\Users\\{user}\\Videos"
    }

    drives = list_external_drives()
    if not drives:
        print("No external drives detected with enough free space.")
        sys.exit(1)

    target_drive = select_drive(drives)
    backup_root = os.path.join(target_drive, f"{pc_name}_{date_str}")
    os.makedirs(backup_root, exist_ok=True)

    print("\n🔎 Calculating folder sizes and estimating time...\n")

    total_data = 0
    for folder_name, folder_path in folders_to_backup.items():
        if os.path.exists(folder_path):
            size = get_folder_size(folder_path)
            total_data += size
            print(f"{folder_name}: {human_readable_size(size)} | Estimated time: {estimate_time(size)}")
        else:
            print(f"⚠️ {folder_name}: Folder does not exist, skipping...")

    print(f"\n📦 Total data to backup: {human_readable_size(total_data)}\n")

    confirm = input("✅ Proceed with the backup using TeraCopy? (y/n): ")
    if confirm.lower() != 'y':
        print("Backup cancelled.")
        sys.exit(0)

    for folder_name, folder_path in folders_to_backup.items():
        if os.path.exists(folder_path):
            dest_folder = os.path.join(backup_root, folder_name)
            os.makedirs(dest_folder, exist_ok=True)
            teracopy_copy(folder_path, dest_folder)

    print(f"\n✅ Backup completed successfully at {backup_root}")

if __name__ == "__main__":
    main()
