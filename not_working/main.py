from pynput.mouse import Listener
import threading, time
import queue
import tkinter as tk

# Kolejka do komunikacji między wątkami
alert_queue = queue.Queue()

signal = threading.Event()


def on_move(x, y):
    signal.set()

def update_font(event=None):
    width = root.winfo_width()
    height = root.winfo_height()
    new_size = min(width, height) // 10
    label.config(font=("Arial", new_size))

def alert():
    root = tk.Tk()
    root.title("Nie obijamy się")
    root.attributes("-fullscreen", True)
    root.attributes('-topmost', True)
    label = tk.Label(root, text="Uprasza się o nie opierdalanie się na lekcji", font=("Arial", 72), anchor="center")
    label.pack(fill=tk.BOTH, expand=True)
    root.bind("<Configure>", update_font)
    root.mainloop()

def listener():
    with Listener(on_move=on_move) as listener:
        listener.join()

def worker():
    last = time.time()
    while True:
        if time.time() - last > 10:
            alert_queue.put('ALERT')
            last = time.time()
        if signal.is_set():
            last = time.time()
            signal.clear()
        time.sleep(1)

def process_alerts():
    try:
        message = alert_queue.get_nowait()
        if message == 'ALERT':
            alert()
    except queue.Empty:
        pass

def main():
    t1 = threading.Thread(target=listener, daemon=True)
    t2 = threading.Thread(target=worker, daemon=True)
    
    t1.start()
    t2.start()

    def check_alerts():
        process_alerts()
        time.sleep(5)
    
    while True:
        check_alerts()

if __name__ == "__main__":
    main()
