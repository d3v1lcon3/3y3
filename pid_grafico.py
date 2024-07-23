#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Função para obter o nome do arquivo de log de performance atual
def get_log_filename():
    data = datetime.now().strftime('%d-%m-%Y')
    return f'processes_{data}.csv'

# Função para gerar o gráfico para um PID específico
def gerar_grafico_pid(pid):
    # Obtém o nome do arquivo de log
    log_filename = get_log_filename()
    
    # Verifica se o arquivo existe
    if os.path.isfile(log_filename):
        # Lê o CSV
        df = pd.read_csv(log_filename)
        
        # Filtra os dados para o PID específico
        df_pid = df[df['PID'] == pid].copy()
        
        # Verifica se há dados para o PID especificado
        if not df_pid.empty:
            # Converte a coluna 'Hora' para datetime para facilitar a ordenação e plotagem
            df_pid['Hora'] = pd.to_datetime(df_pid['Hora'])
            
            # Ordena os dados pelo horário
            df_pid = df_pid.sort_values(by='Hora')
            
            # Configura o gráfico
            plt.figure(figsize=(10, 6))
            
            # Plot CPU usage
            plt.plot(df_pid['Hora'], df_pid['CPU (%)'], label='CPU (%)', color='blue')
            
            # Plot RAM usage
            plt.plot(df_pid['Hora'], df_pid['Memoria (%)'], label='RAM (MB)', color='green')
            
            # Configurações do gráfico
            plt.xlabel('Hora')
            plt.ylabel('Utilização')
            plt.title(f'Utilização de CPU e RAM para PID {pid}')
            plt.legend()
            
            # Mostra o gráfico
            plt.show()
        else:
            print(f"Nenhum dado encontrado para o PID {pid}")
    else:
        print(f"Arquivo {log_filename} não encontrado")

# Captura o PID desejado e chama a função para gerar o gráfico
pid_desejado = int(input('Digite o PID desejado: '))
gerar_grafico_pid(pid_desejado)
