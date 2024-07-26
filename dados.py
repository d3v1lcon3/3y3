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
            process = psutil.Process(process_info['pid'])
            process_info['cmdline'] = ' '.join(process.cmdline())
            process_info['exe'] = process.exe()
            process_info['cwd'] = process.cwd()
            process_info['threads'] = [thread.id for thread in process.threads()]
            process_info['connections'] = [conn._asdict() for conn in process.connections()]
            process_info['open_files'] = [file.path for file in process.open_files()]
            # Adicione outros dados que você deseja coletar
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
    # Adicionando dados de rede
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
                print(f"Hora: {process['Hora']}, PID: {process['pid']}, Nome: {process['name']}, Usuario: {process['username']}, CPU: {process['cpu_percent']}%, Memoria: {process['memory_percent']}%, Cmdline: {process['cmdline']}, Executável: {process['exe']}, CWD: {process['cwd']}, Threads: {process['threads']}, Conexões: {process['connections']}, Arquivos Abertos: {process['open_files']}")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("Encerrando o monitoramento.")
    finally:
        # Fechar os arquivos CSV
        relatorio.close_tables()
