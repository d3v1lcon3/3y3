#!/usr/bin/env python3
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime
import os

# Função para obter o nome do arquivo de log de performance atual
def get_log_filename(prefix):
    data = datetime.now().strftime('%d-%m-%Y')
    return f'{prefix}_{data}.csv'

# Função para carregar os dados do CSV
def load_data(filename):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce')
        df = df.dropna(subset=['Hora'])
        return df
    else:
        return pd.DataFrame()

# Inicializa o app Dash
app = Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Performance de Processos"),
    
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Atualiza a cada 5 segundos
        n_intervals=0
    ),
    
    dcc.Graph(id='system-performance-graph'),
    
    dcc.Dropdown(
        id='process-dropdown',
        options=[],
        placeholder='Selecione um processo'
    ),
    
    dcc.Graph(id='cpu-graph'),
    dcc.Graph(id='ram-graph')
])

# Callback para atualizar o dropdown de processos
@app.callback(
    Output('process-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_dropdown_options(n):
    processes_df = load_data(get_log_filename('processes'))
    return [{'label': name, 'value': name} for name in processes_df['Nome'].unique()]

# Callback para atualizar o gráfico de performance do sistema
@app.callback(
    Output('system-performance-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_system_performance(n):
    performance_df = load_data(get_log_filename('performance'))
    
    system_fig = go.Figure()
    
    system_fig.add_trace(go.Scatter(x=performance_df['Hora'], y=performance_df['CPU'], mode='lines', name='CPU (%)', line=dict(color='blue')))
    system_fig.add_trace(go.Scatter(x=performance_df['Hora'], y=performance_df['RAM'], mode='lines', name='RAM (%)', line=dict(color='green')))
    system_fig.add_trace(go.Scatter(x=performance_df['Hora'], y=performance_df['Disk'], mode='lines', name='Disk (%)', line=dict(color='red')))
    
    system_fig.update_layout(title='Uso de CPU, RAM e Disco Total', xaxis_title='Hora', yaxis_title='Utilização (%)')

    return system_fig

# Callback para atualizar os gráficos de CPU e RAM com base no processo selecionado
@app.callback(
    [Output('cpu-graph', 'figure'),
     Output('ram-graph', 'figure')],
    [Input('process-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graphs(selected_process, n):
    if selected_process is None:
        return {}, {}

    processes_df = load_data(get_log_filename('processes'))
    df_process = processes_df[processes_df['Nome'] == selected_process].sort_values(by='Hora')
    
    cpu_fig = go.Figure()
    cpu_fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['CPU (%)'], mode='lines', name='CPU (%)'))
    cpu_fig.update_layout(title=f'Utilização de CPU para o processo {selected_process}', xaxis_title='Hora', yaxis_title='CPU (%)')

    ram_fig = go.Figure()
    ram_fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['Memoria (%)'], mode='lines', name='RAM (MB)'))
    ram_fig.update_layout(title=f'Utilização de RAM para o processo {selected_process}', xaxis_title='Hora', yaxis_title='RAM (MB)')
    
    return cpu_fig, ram_fig

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)


