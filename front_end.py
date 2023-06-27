import streamlit as st
from custom_fun import CpuMonitor
import time
import pandas as pd
import altair as alt

st.set_page_config(page_title="CPU Usage Monitor", page_icon=":chart_with_upwards_trend:")

st.title("CPU Usage Monitor")

monitor = CpuMonitor()
monitor.start_monitoring()

data = pd.DataFrame(columns=["timestamp", "cpu_usage"])

chart = st.empty()

while True:
    time.sleep(1)
    data = monitor.get_data()
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    chart.altair_chart(alt.Chart(data).mark_line().encode(
        x=alt.X('timestamp:T', axis=alt.Axis(title='Timestamp', labelAngle=-45)),
        y=alt.Y('cpu_usage:Q', axis=alt.Axis(title='CPU Usage (%)'))
    ).properties(width=800, height=400))
