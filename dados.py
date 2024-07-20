#!/usr/bin/env python3

import psutil
import time
import relatorio

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            process_info = proc.info
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
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
    # Abrir os arquivos CSV
    relatorio.open_tables()

    try:
        while True:
            # Obter uso do sistema
            cpu, ram, disk = get_system_usage()
            
            # Registrar uso do sistema no CSV
            relatorio.write_performance(cpu, ram, disk)
            # Forçar gravação no disco
            relatorio.performance_file.flush()
            
            # Obter e registrar lista de processos no CSV
            process_list = list_processes()
            relatorio.write_processes(process_list)
            # Forçar gravação no disco
            relatorio.processes_file.flush()

            # Print para visualização (opcional)
            print(f"Uso da CPU: {cpu}%")
            print(f"Uso da RAM: {ram}%")
            print(f"Uso do Disco: {disk}%")
            for process in process_list:
                print(f"PID: {process['pid']}, Nome: {process['name']}, Usuario: {process['username']}, CPU: {process['cpu_percent']}, Memoria: {process['memory_percent']}%")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Encerrando o monitoramento.")
    finally:
        # Fechar os arquivos CSV
        relatorio.close_tables()
