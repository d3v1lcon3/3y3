#!/usr/bin/env python3

import psutil
import time
from datetime import datetime
import relatorio

def list_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            process_info = proc.info
            # Adiciona a coleta de uso de disco dos processos
            with proc.oneshot():
                io_counters = proc.io_counters()
                process_info['disk_read_bytes'] = io_counters.read_bytes
                process_info['disk_write_bytes'] = io_counters.write_bytes
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
    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent
    net_recv = net_io.bytes_recv
    return cpu_usage, ram_usage, disk_percent, net_sent, net_recv

if __name__ == "__main__":
    # Abrir os arquivos CSV
    relatorio.open_tables()

    try:
        while True:
            # Captura a hora atual
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Obter uso do sistema
            cpu, ram, disk, net_sent, net_recv = get_system_usage()
            
            # Registrar uso do sistema no CSV com a hora atual
            relatorio.write_performance(current_time, cpu, ram, disk, net_sent, net_recv)
            # Forçar gravação no disco
            relatorio.file_performance.flush()
            
            # Obter e registrar lista de processos no CSV com a hora atual
            process_list = list_processes()
            for process in process_list:
                process['Hora'] = current_time
            relatorio.write_processes(process_list)
            # Forçar gravação no disco
            relatorio.file_processes.flush()

            # Print para visualização (opcional)
            print(f"Hora: {current_time}")
            print(f"Uso da CPU: {cpu}%")
            print(f"Uso da RAM: {ram}%")
            print(f"Uso do Disco: {disk}%")
            print(f"Rede Enviada: {net_sent} bytes")
            print(f"Rede Recebida: {net_recv} bytes")
            for process in process_list:
                print(f"Hora: {process['Hora']}, PID: {process['pid']}, Nome: {process['name']}, Usuario: {process['username']}, CPU: {process['cpu_percent']}%, Memoria: {process['memory_percent']}%, Disco Lido: {process['disk_read_bytes']} bytes, Disco Escrito: {process['disk_write_bytes']} bytes")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Encerrando o monitoramento.")
    finally:
        # Fechar os arquivos CSV
        relatorio.close_tables()
