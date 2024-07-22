import pandas as pd
import matplotlib.pyplot as plt

# Carrega o arquivo CSV
file_path = 'caminho/para/seu_arquivo.csv'
df = pd.read_csv(file_path)

# Função para gerar o gráfico para um PID específico
def gerar_grafico_pid(pid):
    # Filtra os dados para o PID específico
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
pid_desejado = 1234  # Substitua pelo PID que você deseja visualizar
gerar_grafico_pid(pid_desejado)
