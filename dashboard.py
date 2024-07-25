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

# Carrega os dados de desempenho do sistema e processos
performance_df = load_data(get_log_filename('performance'))
processes_df = load_data(get_log_filename('processes'))

# Inicializa o app Dash
app = Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Performance de Processos"),
    
    html.Div([
        dcc.Graph(id='system-cpu-graph'),
        dcc.Graph(id='system-ram-graph'),
        dcc.Graph(id='system-disk-graph')
    ]),
    
    dcc.Dropdown(
        id='pid-dropdown',
        options=[{'label': str(pid), 'value': pid} for pid in processes_df['PID'].unique()],
        placeholder='Selecione um PID'
    ),
    
    dcc.Graph(id='cpu-graph'),
    dcc.Graph(id='ram-graph')
])

# Callback para atualizar os gráficos de performance do sistema
@app.callback(
    [Output('system-cpu-graph', 'figure'),
     Output('system-ram-graph', 'figure'),
     Output('system-disk-graph', 'figure')],
    [Input('pid-dropdown', 'value')]
)
def update_system_performance(_):
    cpu_fig = go.Figure()
    cpu_fig.add_trace(go.Scatter(x=performance_df['Hora'], y=performance_df['CPU'], mode='lines', name='CPU (%)'))
    cpu_fig.update_layout(title='Uso de CPU Total', xaxis_title='Hora', yaxis_title='CPU (%)')

    ram_fig = go.Figure()
    ram_fig.add_trace(go.Scatter(x=performance_df['Hora'], y=performance_df['RAM'], mode='lines', name='RAM (%)'))
    ram_fig.update_layout(title='Uso de RAM Total', xaxis_title='Hora', yaxis_title='RAM (%)')

    disk_fig = go.Figure()
    disk_fig.add_trace(go.Scatter(x=performance_df['Hora'], y=performance_df['Disk'], mode='lines', name='Disk (%)'))
    disk_fig.update_layout(title='Uso de Disco Total', xaxis_title='Hora', yaxis_title='Disk (%)')

    return cpu_fig, ram_fig, disk_fig

# Callback para atualizar os gráficos com base no PID selecionado
@app.callback(
    [Output('cpu-graph', 'figure'),
     Output('ram-graph', 'figure')],
    [Input('pid-dropdown', 'value')]
)
def update_graphs(selected_pid):
    if selected_pid is None:
        return {}, {}

    df_pid = processes_df[processes_df['PID'] == selected_pid].sort_values(by='Hora')
    
    cpu_fig = go.Figure()
    cpu_fig.add_trace(go.Scatter(x=df_pid['Hora'], y=df_pid['CPU (%)'], mode='lines', name='CPU (%)'))
    cpu_fig.update_layout(title=f'Utilização de CPU para PID {selected_pid}', xaxis_title='Hora', yaxis_title='CPU (%)')

    ram_fig = go.Figure()
    ram_fig.add_trace(go.Scatter(x=df_pid['Hora'], y=df_pid['Memoria (%)'], mode='lines', name='RAM (MB)'))
    ram_fig.update_layout(title=f'Utilização de RAM para PID {selected_pid}', xaxis_title='Hora', yaxis_title='RAM (MB)')
    
    return cpu_fig, ram_fig

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
