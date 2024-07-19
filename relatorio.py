#!/usr/bin/env python3

import csv
import os
from datetime import datetime

data = datetime.now().strftime('%d-%m-%Y')
data_performance_name = f'performance_{data}.csv'
data_processes_name = f'processes_{data}.csv'

# Variáveis globais para os escritores
writer_performance = None
writer_processes = None

# Abrir os arquivos
def open_tables():
    global writer_performance, writer_processes

    # Verificar se os arquivos existem
    performance_exist = os.path.isfile(data_performance_name)
    processes_exist = os.path.isfile(data_processes_name)

    # Abrir e configurar o arquivo de performance
    with open(data_performance_name, mode='a' if performance_exist else 'w', newline='', encoding='utf-8') as file:
        writer_performance = csv.DictWriter(file, fieldnames=['CPU', 'RAM', 'Disk'])
        if not performance_exist:
            writer_performance.writeheader()

    # Abrir e configurar o arquivo de processos
    with open(data_processes_name, mode='a' if processes_exist else 'w', newline='', encoding='utf-8') as file:
        writer_processes = csv.DictWriter(file, fieldnames=['PID', 'Nome', 'Usuario', 'CPU', 'Memoria'])
        if not processes_exist:
            writer_processes.writeheader()

# Registrar os dados de performance
def write_performance(cpu, ram, disk):
    if writer_performance:
        writer_performance.writerow({'CPU': cpu, 'RAM': ram, 'Disk': disk})

# Registrar árvore de processos
def write_processes(procs):
    if writer_processes:
        for proc in procs:
            writer_processes.writerow(proc)
