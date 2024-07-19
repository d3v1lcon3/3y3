#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from datetime import datetime

# Função para obter o nome do arquivo de log atual
def get_log_filename(log_type):
    data = datetime.now().strftime('%d-%m-%Y')
    return f'{log_type}_{data}.csv'

# Função para ler os logs e atualizar os gráficos
def update_logs(i, cpu_line, ram_line, disk_line, log_type):
    log_filename = get_log_filename(log_type)
    if os.path.isfile(log_filename):
        df = pd.read_csv(log_filename)
        if log_type == 'performance':
            if not df.empty:
                cpu_line.set_data(df.index, df['CPU'])
                ram_line.set_data(df.index, df['RAM'])
                disk_line.set_data(df.index, df['Disk'])
                ax.relim()
                ax.autoscale_view()
        elif log_type == 'processes':
            # Adicione o código para processar os logs de processos se necessário
            pass

# Configurar o gráfico
fig, ax = plt.subplots()
cpu_line, = ax.plot([], [], label='CPU')
ram_line, = ax.plot([], [], label='RAM')
disk_line, = ax.plot([], [], label='Disk')

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_xlabel('Time')
ax.set_ylabel('Usage (%)')
ax.legend()

# Função de animação para atualizar o gráfico
ani = FuncAnimation(fig, update_logs, fargs=(cpu_line, ram_line, disk_line, 'performance'), interval=1000)

plt.show()
