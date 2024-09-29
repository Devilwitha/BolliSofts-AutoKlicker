import psutil

def isrunning_prozess(prozessname):
    for prozess in psutil.process_iter(['pid', 'name']):
        if prozess.info['name'] == prozessname:
            print(f"Prozess '{prozessname}' wurde beendet.")
            return True
    print(f"Prozess '{prozessname}' wurde nicht gefunden.")
    return False

def beende_prozess(prozessname):
    for prozess in psutil.process_iter(['pid', 'name']):
        if prozess.info['name'] == prozessname:
            prozess.kill()
            print(f"Prozess '{prozessname}' wurde beendet.")
            return 

    print(f"Prozess '{prozessname}' wurde nicht gefunden.") 

if __name__ == "__main__":
    exe_name = "main.exe"  # Ersetze dies durch den tatsächlichen Namen der EXE-Datei
    beende_prozess(exe_name)