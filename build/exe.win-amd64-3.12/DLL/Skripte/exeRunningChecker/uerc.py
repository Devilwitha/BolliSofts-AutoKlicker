import psutil
import subprocess

def beende_unterprozess(prozessname):
    for prozess in psutil.process_iter(['pid', 'name', 'cmdline']):
        if prozess.info['name'] == prozessname:
            try:
                parent_pid = prozess.ppid()
                parent_process = psutil.Process(parent_pid)
                if parent_process.cmdline() and 'python' in parent_process.cmdline()[0]:  # Überprüfen, ob der Elternprozess ein Python-Prozess ist
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(prozess.info['pid'])])
                    print(f"Unterprozess '{prozessname}' wurde beendet.")
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    print(f"Unterprozess '{prozessname}' wurde nicht gefunden oder konnte nicht beendet werden.")

if __name__ == "__main__":
    unterprozess_name = "main.exe"  # Ersetze dies durch den tatsächlichen Namen des Unterprozesses
    beende_unterprozess(unterprozess_name)