#!/usr/bin/env python3
import csv
from datetime import datetime

# Abertura dos arquivos (exemplo)
def open_tables():
    global file_performance, file_processes
    data = datetime.now().strftime('%d-%m-%Y')
    file_performance = open(f'performance_{data}.csv', mode='a', newline='')
    file_processes = open(f'processes_{data}.csv', mode='a', newline='')
    
    # Escrita do cabeçalho se o arquivo estiver vazio
    if file_performance.tell() == 0:
        performance_writer = csv.writer(file_performance)
        performance_writer.writerow(['Hora', 'CPU', 'RAM', 'Disk', 'Net Sent', 'Net Recv'])
    
    if file_processes.tell() == 0:
        processes_writer = csv.writer(file_processes)
        processes_writer.writerow([
            'Hora', 'PID', 'Nome', 'Usuario', 'CPU (%)', 'Memoria (%)', 
            'Disco Lido (bytes)', 'Disco Escrito (bytes)', 
            'Rede Enviada (bytes)', 'Rede Recebida (bytes)', 
            'Cmdline', 'Executável', 'CWD', 'Threads', 'Conexões', 'Arquivos Abertos'
        ])

# Função para registrar o uso do sistema no CSV com a hora atual
def write_performance(current_time, cpu, ram, disk, net_sent, net_recv):
    performance_writer = csv.writer(file_performance)
    performance_writer.writerow([current_time, cpu, ram, disk, net_sent, net_recv])

# Função para registrar a lista de processos no CSV com a hora atual
def write_processes(process_list):
    processes_writer = csv.writer(file_processes)
    for process in process_list:
        processes_writer.writerow([
            process['Hora'], process['pid'], process['name'], process['username'],
            process['cpu_percent'], process['memory_percent'], 
            process.get('disco_lido', 'N/A'), process.get('disco_escrito', 'N/A'),
            process.get('rede_enviada', 'N/A'), process.get('rede_recebida', 'N/A'),
            process.get('cmdline', 'N/A'), process.get('exe', 'N/A'),
            process.get('cwd', 'N/A'), process.get('threads', 'N/A'),
            process.get('connections', 'N/A'), process.get('open_files', 'N/A')
        ])

# Fechar os arquivos CSV (exemplo)
def close_tables():
    file_performance.close()
    file_processes.close()
