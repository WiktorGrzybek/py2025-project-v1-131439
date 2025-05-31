# gui/app.py

import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
from datetime import datetime, timedelta

from sensors.temperature_sensor  import TemperatureSensor
from sensors.humidity_sensor     import HumiditySensor
from sensors.pressure_sensor     import PressureSensor
from sensors.light_sensor        import LightSensor
from sensors.air_quality_sensor  import AirQualitySensor

from logger.logger import Logger


class App(tk.Tk):
    """
    Główne okno aplikacji: sterowanie symulacją, wizualizacja odczytów,
    statystyki i status serwera.
    """
    def __init__(self):
        super().__init__()
        self.title("🔌 Network Server GUI")
        self.geometry("920x550")
        self.configure(background="#f0f0f0")

        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure("Treeview.Heading",
                        background="#4a6984",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        style.map("Treeview",
                  background=[("selected", "#aae0ff")])

        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=24,
                        fieldbackground="#ffffff",
                        background="#ffffff")

        style.configure("TButton",
                        font=("Segoe UI", 10),
                        padding=6)
        style.configure("TEntry",
                        font=("Segoe UI", 10),
                        padding=4)

        style.configure("TLabel",
                        font=("Segoe UI", 10),
                        background="#f0f0f0")

        header_lbl = ttk.Label(self,
                               text="🛰️  System Monitoringu – Live Sensor Dashboard",
                               font=("Segoe UI", 14, "bold"))
        header_lbl.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        ctrl_frame = ttk.LabelFrame(self, text="Sterowanie Serwerem", padding=(10, 10))
        ctrl_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))

        ttk.Label(ctrl_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 5))
        self.port_var = tk.StringVar(value="9999")
        self.port_entry = ttk.Entry(ctrl_frame, textvariable=self.port_var, width=6)
        self.port_entry.pack(side=tk.LEFT, padx=(0, 15))

        self.start_btn = ttk.Button(ctrl_frame, text="▶️ Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(ctrl_frame, text="⏹️ Stop", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=(5, 0))

        table_frame = ttk.LabelFrame(self, text="Odczyty Czujników (Live)", padding=(10, 10))
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        columns = ("Sensor", "Wartość", "Jednostka", "Timestamp", "Śr. 1h", "Śr. 12h")
        self.tree = ttk.Treeview(table_frame,
                                 columns=columns,
                                 show="headings",
                                 selectmode="none")
        col_widths = [100, 80, 80, 180, 80, 80]
        for idx, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[idx], anchor=tk.CENTER)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 2))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        status_bar = ttk.Frame(self)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status = tk.StringVar(value="Status: Stopped")
        status_lbl = ttk.Label(status_bar,
                               textvariable=self.status,
                               relief=tk.SUNKEN,
                               anchor=tk.W,
                               font=("Segoe UI", 9))
        status_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

        self.sensors = {
            'temp1'  : TemperatureSensor('temp1'),
            'hum1'   : HumiditySensor('hum1'),
            'pres1'  : PressureSensor('pres1'),
            'light1' : LightSensor('light1'),
            'airq1'  : AirQualitySensor('airq1')
        }
        self.logger = Logger()
        self.running = False

        self.history = {sid: [] for sid in self.sensors}

    def start(self):
        if not self.running:
            port_str = self.port_var.get().strip()
            if not port_str.isdigit():
                self.status.set("⚠️ Błąd: Port musi być liczbą.")
                return

            self.running = True
            self.status.set(f"Listening on port {port_str}")
            Thread(target=self._update_loop, daemon=True).start()

    def _update_loop(self):
        """
        Co sekundę pobiera odczyty ze wszystkich czujników, loguje je i odświeża tabelę.
        Oblicza średnie w oknach 1h i 12h.
        """
        while self.running:
            now = datetime.now()
            for sid, sensor in self.sensors.items():
                try:
                    val = sensor.read_value()
                except Exception as e:
                    self.status.set(f"⚠️ Błąd w {sid}: {e}")
                    continue
                unit = sensor.unit

                self.history[sid].append((now, val))
                cutoff1  = now - timedelta(hours=1)
                cutoff12 = now - timedelta(hours=12)

                last1  = [v for t, v in self.history[sid] if t >= cutoff1]
                last12 = [v for t, v in self.history[sid] if t >= cutoff12]

                avg1  = sum(last1) / len(last1) if last1 else 0
                avg12 = sum(last12) / len(last12) if last12 else 0

                self.logger.log_reading(sid, now, val, unit)

                vals = (
                    sid,
                    f"{val:.2f}",
                    unit,
                    now.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{avg1:.2f}",
                    f"{avg12:.2f}"
                )
                if self.tree.exists(sid):
                    self.tree.item(sid, values=vals)
                else:

                    index = len(self.tree.get_children())
                    tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                    self.tree.insert("", tk.END, iid=sid, values=vals, tags=(tag,))

            time.sleep(1)

    def stop(self):
        self.running = False
        self.status.set("Status: Stopped")


def configure_row_colors(tree: ttk.Treeview):
    """
    Dodaje style dla tagów 'oddrow' i 'evenrow', aby wiersze w tabeli miały
    naprzemiennie jasne i nieco ciemniejsze tło.
    """
    tree.tag_configure('oddrow', background='#f9f9f9')
    tree.tag_configure('evenrow', background='#ffffff')


if __name__ == '__main__':
    app = App()
    configure_row_colors(app.tree)
    app.mainloop()
