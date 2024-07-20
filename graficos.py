#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from datetime import datetime

# Função para obter o nome do arquivo de log de performance atual
def get_performance_log_filename():
    data = datetime.now().strftime('%d-%m-%Y')
    return f'performance_{data}.csv'

# Função para ler os logs de performance e atualizar os gráficos
def update_logs(i, cpu_line, ram_line, disk_line):
    log_filename = get_performance_log_filename()
    if os.path.isfile(log_filename):
        df = pd.read_csv(log_filename)
        print(f"Lendo arquivo {log_filename}")
        if not df.empty:
            print("Atualizando gráfico com novos dados")
            # Atualiza as linhas dos gráficos com os novos dados
            cpu_line.set_xdata(df.index)
            cpu_line.set_ydata(df['CPU'])
            ram_line.set_xdata(df.index)
            ram_line.set_ydata(df['RAM'])
            disk_line.set_xdata(df.index)
            disk_line.set_ydata(df['Disk'])
            
            # Ajusta os limites do gráfico para os novos dados
            ax.relim()
            ax.autoscale_view()
        else:
            print("DataFrame vazio")
            # Se o DataFrame estiver vazio, garante que o gráfico não mostre dados antigos
            cpu_line.set_xdata([])
            cpu_line.set_ydata([])
            ram_line.set_xdata([])
            ram_line.set_ydata([])
            disk_line.set_xdata([])
            disk_line.set_ydata([])
    else:
        print(f"Arquivo {log_filename} não encontrado")

# Configurar o gráfico
fig, ax = plt.subplots()
cpu_line, = ax.plot([], [], label='CPU')
ram_line, = ax.plot([], [], label='RAM')
disk_line, = ax.plot([], [], label='Disk')

# Definir os limites iniciais e rótulos
ax.set_xlim(0, 100)  # Limite inicial, será ajustado dinamicamente
ax.set_ylim(0, 100)
ax.set_xlabel('Tempo')
ax.set_ylabel('Uso (%)')
ax.legend()

# Função de animação para atualizar o gráfico
ani = FuncAnimation(fig, update_logs, fargs=(cpu_line, ram_line, disk_line), interval=1000)

plt.show()
