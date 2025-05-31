# gui/app.py
import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
from datetime import datetime, timedelta
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor
from logger.logger import Logger

class App(tk.Tk):
    """
    Główne okno aplikacji: sterowanie symulacją, wizualizacja odczytów,
    statystyki i status serwera.
    """
    def __init__(self):
        super().__init__()
        self.title("Network Server GUI")
        self.geometry("900x500")
        # Stylizacja
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', rowheight=25)
        style.configure('TButton', padding=6)
        style.configure('TEntry', padding=4)
        # Górny panel: port i przyciski
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        ttk.Label(top_frame, text="Port:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="9999")
        self.port_entry = ttk.Entry(top_frame, textvariable=self.port_var, width=6)
        self.port_entry.pack(side=tk.LEFT, padx=(5, 15))
        self.start_btn = ttk.Button(top_frame, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(top_frame, text="Stop", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        # Tabela z odczytami
        columns = ("Sensor", "Wartość", "Jednostka", "Timestamp", "Śr. 1h", "Śr. 12h")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # Pasek statusu
        self.status = tk.StringVar(value="Stopped")
        status_bar = ttk.Label(self, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        # Przygotowanie czujników i loggera
        self.sensors = {
            'temp1': TemperatureSensor('temp1'),
            'hum1': HumiditySensor('hum1'),
            'pres1': PressureSensor('pres1')
        }
        self.logger = Logger()
        self.running = False
        # Historia do obliczeń średnich
        self.history = {sid: [] for sid in self.sensors}

    def start(self):
        if not self.running:
            self.running = True
            port = self.port_var.get()
            self.status.set(f"Listening on port {port}")
            Thread(target=self._update_loop, daemon=True).start()

    def _update_loop(self):
        while self.running:
            now = datetime.now()
            for sid, sensor in self.sensors.items():
                val = sensor.read_value()
                unit = sensor.unit
                # Zapisywanie do historii
                self.history[sid].append((now, val))
                # Przycinanie historii
                cutoff1 = now - timedelta(hours=1)
                cutoff12 = now - timedelta(hours=12)
                last1 = [v for t, v in self.history[sid] if t >= cutoff1]
                last12 = [v for t, v in self.history[sid] if t >= cutoff12]
                avg1 = sum(last1) / len(last1) if last1 else 0
                avg12 = sum(last12) / len(last12) if last12 else 0
                # Logowanie
                self.logger.log_reading(sid, now, val, unit)
                # Aktualizacja tabeli
                vals = (sid, f"{val:.2f}", unit, now.strftime("%Y-%m-%d %H:%M:%S"),
                        f"{avg1:.2f}", f"{avg12:.2f}")
                if self.tree.exists(sid):
                    self.tree.item(sid, values=vals)
                else:
                    self.tree.insert("", tk.END, iid=sid, values=vals)
            time.sleep(1)

    def stop(self):
        self.running = False
        self.status.set("Stopped")

if __name__ == '__main__':
    App().mainloop()