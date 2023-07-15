import tkinter as tk
from tkinter import ttk
from threading import Thread, Event


class ChatSimulation(Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.stop_event = Event()
        self.history = []

    def run(self):
        def on_submit(event=None):
            user_input = text_input.get()
            if user_input:
                self.callback(user_input)
                text_input.delete(0, tk.END)
                self.history.append(user_input)
                update_history()

        def update_history():
            output_text.config(state=tk.NORMAL)
            output_text.delete("1.0", tk.END)
            for message in list(reversed(self.history)):
                output_text.insert(tk.END, message + "\n")
            output_text.config(state=tk.DISABLED)
            output_text.see(tk.END)

        def stop():
            self.stop_event.set()
            window.quit()

        window = tk.Tk()
        window.title("Input Utente")
        window.geometry("400x300")

        style = ttk.Style()
        style.configure("TFrame", background="#e1d8b9")
        style.configure("TLabel", background="#e1d8b9")
        style.configure("TEntry", background="white")

        input_frame = ttk.Frame(window, style="TFrame")
        input_frame.pack(pady=20)

        history_frame = ttk.Frame(window, style="TFrame")
        history_frame.pack()

        label = ttk.Label(input_frame, text="Invia un messaggio:", style="TLabel")
        label.pack()

        text_input = ttk.Entry(input_frame, width=30)
        text_input.pack(pady=10)

        submit_button = ttk.Button(input_frame, text="Invia", command=on_submit)
        submit_button.pack()

        output_text = tk.Text(history_frame, height=10, width=40, bg="white")
        output_text.pack()

        output_text.config(state=tk.DISABLED)

        window.bind("<Return>", on_submit)

        window.protocol("WM_DELETE_WINDOW", stop)  # Gestione della chiusura della finestra

        window.mainloop()

    def stop(self):
        self.stop_event.set()
