import time
import schedule
import threading

stop_flag = threading.Event()  # Definiere stop_flag global


def meine_methode():
    # Hier kommt der Code deiner Methode hin
    print("Es ist 4:20 Uhr! Meine Methode wird ausgeführt.")

def schedule_task():
    schedule.every().day.at("04:20").do(meine_methode)

    global stop_flag  # Greife auf die globale Variable zu

    while not stop_flag.is_set():
        schedule.run_pending()
        time.sleep(1)

# Starte den Scheduler in einem separaten Thread
def start_schedule():
    global t  # Damit wir den Thread global zugreifen können
    t = threading.Thread(target=schedule_task)
    t.start()
    print("Automation wurde gestartet")

# Beende den Thread
def stop_schedule():
    global t, stop_flag  # Greife auf die globalen Variablen zu
    stop_flag.set()
    t.join()
    print("Automation wurde gestopt")