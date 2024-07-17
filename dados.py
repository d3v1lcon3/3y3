#!/usr/bin/env python3

import psutil
import time

def list_processes():
	processes = []

	for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
		try:
			process_info = proc.info
			processes.append(process_info)
		except (psutil.NoSuchProcess, psutil.AcessDenied, psutil.ZombieProcess):
			pass
	return processes

def get_system_usage():
	cpu_usage = psutil.cpu_percent(interval=1)

	memory_info = psutil.virtual_memory()
	ram_usage = memory_info.percent

	disk_usage = psutil.disk_usage('/')
	disk_percent = disk_usage.percent

	return cpu_usage, ram_usage, disk_percent

if __name__ == "__main__":
	process_list = list_processes()

	while True:
		cpu, ram, disk = get_system_usage()
		print(f"Uso da CPU: {cpu}%")
		print(f"Uso da RAM: {ram}%")
		print(f"Uso do Disco: {disk}%")
		for process in process_list:
			print(f"PID: {process['pid']}, Nome: {process['name']}, Usuario: {process['username']}, CPU: {process['cpu_percent']}, Memoria: {process['memory_percent']}%")

		time.sleep(5)
