#!/usr/bin/env python3

import psutil
import time

def get_system_usage():
	cpu_usage = psutil.cpu_percent(interval=1)

	memory_info = psutil.virtual_memory()
	ram_usage = memory_info.percent

	disk_usage = psutil.disk_usage('/')
	disk_percent = disk_usage.percent

	return cpu_usage, ram_usage, disk_percent

if __name__ == "__main__":
	while True:
		cpu, ram, disk = get_system_usage()
		print(f"Uso da CPU: {cpu}%")
		print(f"Uso da RAM: {ram}%")
		print(f"Uso do Disco: {disk}%")

		time.sleep(5)
