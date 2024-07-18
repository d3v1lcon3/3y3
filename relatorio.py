#!/usr/env/bin python3

import csv

data = datetime.now().strftime('%d-%m-%Y')
data_performance_name = f'performance_{data}.csv'
data_processes_name = f'processes_{data}.csv'

#abrir os arquivos
def open_tables():
	with open(data_performance_name, mode='a' if exist else 'w', newline='', encoding='utf-8')
		writer_performance = csv.DictWriter(file, fieldnames=['CPU', 'RAM', 'Disk'])

		if not exist:
			writer.writeheader()
	with open(data_processes_name, mode='a' if exist else 'w', newline='', encode='utf-8'])
		writer_processes = csv.DictWriter(file_performance, fieldnames=['PID', 'Nome', 'Usuario', 'CPU', 'Memoria'])

		if not exist:
			writer_processes,writeheader()
#registrar os dados de performance
def write_performance(cpu, ram, disk):
	writer_performance.writerow(cpu,ram,disk)
#registrar arvore de processos
def write_processes(procs):
	for proc in procs:
		writer_processes.writerow(proc)
