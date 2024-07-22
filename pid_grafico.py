#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Função para obter o nome do arquivo de log de performance atual
def get_log_filename():
    data = datetime.now().strftime('%d-%m-%Y')
    return f'processes_{data}.csv'

# Função para gerar o gráfico para um PID específico
def gerar_grafico_pid(pid):
    # Filtra os dados para o PID específico
    df = get_log_filename()
    df_pid = df[df['PID'] == pid]
    
    # Converte a coluna 'Hora' para datetime para facilitar a ordenação e plotagem
    df_pid['Hora'] = pd.to_datetime(df_pid['Hora'])
    
    # Ordena os dados pelo horário
    df_pid = df_pid.sort_values(by='Hora')
    
    # Configura o gráfico
    plt.figure(figsize=(10, 6))
    
    # Plot CPU usage
    plt.plot(df_pid['Hora'], df_pid['cpu'], label='CPU (%)', color='blue')
    
    # Plot RAM usage
    plt.plot(df_pid['Hora'], df_pid['ram'], label='RAM (MB)', color='green')
    
    # Configurações do gráfico
    plt.xlabel('Hora')
    plt.ylabel('Utilização')
    plt.title(f'Utilização de CPU e RAM para PID {pid}')
    plt.legend()
    
    # Mostra o gráfico
    plt.show()

# Chama a função para gerar o gráfico para o PID desejado
pid_desejado = int(input('PID'))
gerar_grafico_pid(pid_desejado)
