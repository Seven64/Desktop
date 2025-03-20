import psutil
import os

def get_startup_folder_apps():
    startup_apps = set()

    # Getting the startup folder path
    startup_folder = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
    
    # Collecting the executable names from the Startup folder
    if os.path.exists(startup_folder):
        for file in os.listdir(startup_folder):
            if file.lower().endswith('.lnk'):
                startup_apps.add(file.lower())
    
    return startup_apps

def is_system_process(proc):
    try:
        exe_path = proc.exe().lower()
        name = proc.name().lower()
        # Check if it's a system process
        if ('windows' in exe_path or 'microsoft' in exe_path or 
            name in ('system', 'system idle process', 'wininit.exe', 'csrss.exe', 'smss.exe', 'winlogon.exe')):
            return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return True
    return False

def get_background_processes():
    background_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # Skip system processes and startup apps
            if is_system_process(proc):
                continue
            
            # Check if it's in the startup folder or Thonny
            name = proc.info['name'].lower()
            if name in startup_safe or name == 'thonny.exe':
                continue
            
            # If it's not a system process or a startup app, it's considered a background app
            background_processes.append(proc)
        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return background_processes

def main():
    # Getting the list of safe startup apps (including Thonny)
    global startup_safe
    startup_safe = get_startup_folder_apps()
    startup_safe.add('thonny.exe')  # Always safe to keep Thonny

    # Getting a list of background processes
    background_processes = get_background_processes()

    # If no background processes, just print a message
    if not background_processes:
        print("✅ No non-system, non-startup background apps running!")
        return

    # Displaying non-system, non-startup apps
    print("\n🔎 The following background apps are running and are not on the safe list:\n")
    for i, proc in enumerate(background_processes, 1):
        print(f"{i}. {proc.info['name']} (PID: {proc.pid})")

    # Asking to confirm killing all processes
    choice = input("\n❓ Do you want to kill all the listed processes? [y/N]: ").strip().lower()

    if choice == 'y':
        # Kill all the processes
        for proc in background_processes:
            try:
                proc.kill()
                print(f"✅ Killed {proc.info['name']} (PID {proc.pid})")
            except Exception as e:
                print(f"⚠️ Could not kill {proc.info['name']}: {e}")
    else:
        print("⏩ Skipped killing processes.")

if __name__ == "__main__":
    main()
