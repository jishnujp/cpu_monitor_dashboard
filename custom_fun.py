import psutil
import time
import pandas as pd
from threading import Thread

class CpuMonitor:
    def __init__(self):
        self.df = pd.DataFrame(columns=["timestamp", "cpu_usage", "cpu_temperature"])
        self.monitoring = False

    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_cpu_temperature(self):
        temperatures = psutil.sensors_temperatures()
        if not temperatures:
            return float('nan')
        else:
            for name, entries in temperatures.items():
                for entry in entries:
                    if name == "coretemp" and "Package id 0" in entry.label:
                        return entry.current
        return float('nan')


    def start_monitoring(self):
        self.monitoring = True
        thread = Thread(target=self.record_data)
        thread.start()

    def stop_monitoring(self):
        self.monitoring = False

    def record_data(self):
        start_time = time.time()
        while self.monitoring and time.time() - start_time < 600:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cpu_usage = self.get_cpu_usage()
            cpu_temperature = self.get_cpu_temperature()
            new_data = pd.DataFrame({"timestamp": [timestamp], "cpu_usage": [cpu_usage], "cpu_temperature": [cpu_temperature]})
            self.df = pd.concat([self.df, new_data], ignore_index=True)
            time.sleep(1)

    def get_data(self):
        return self.df
