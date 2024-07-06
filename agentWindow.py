import time
import threading
import tkinter as tk
import agentVision
import agentState

def update_window_data(update_interval, label):
    def refresh():
        while not stop_event.is_set():
            print('Determining State')
            # screenshot = agentVision.take_screenshot()
            screenshot = agentVision.crop_screenshot_to_ypp(agentVision.take_screenshot())
            updated_state = agentState.StateMachine(agentState.ypp_state).determine_state(screenshot)
            alerts = agentState.StateMachine(agentState.ypp_alerts_init_state).determine_state(screenshot)
            print(updated_state)
            update_label(label, updated_state, alerts)
            time.sleep(update_interval)

    stop_event = threading.Event()
    threading.Thread(target=refresh).start()
    return stop_event

def update_label(label, updated_state, alerts):
    display_text = ""
    display_text += "State Detected:\n"
    for state in updated_state:
        display_text += f"{state}\n"

    display_text += "\nAlerts Detected:\n"

    for alert in alerts:
        display_text += f"{alert}\n"

    label.config(text=display_text)

def create_window(update_interval):
    root = tk.Tk()
    root.title("YPP! State Machine")
    label = tk.Label(root, text="", padx=10, pady=10)
    label.pack()

    stop_event = update_window_data(update_interval, label)
    def stop_program():
        stop_event.set()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", stop_program)
    root.bind('<Control-s>', lambda e: stop_program())

    root.mainloop()
