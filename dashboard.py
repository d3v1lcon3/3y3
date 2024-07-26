#!/usr/bin/env python3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import os
from datetime import datetime
import psutil

# Função para obter o nome do arquivo de log de performance atual
def get_log_filename():
    data = datetime.now().strftime('%d-%m-%Y')
    return f'performance_{data}.csv', f'processes_{data}.csv'

# Função para ler os dados de desempenho
def read_performance_data():
    performance_file, _ = get_log_filename()
    if os.path.exists(performance_file):
        return pd.read_csv(performance_file)
    else:
        return pd.DataFrame(columns=['Hora', 'CPU', 'RAM', 'Disk', 'Net Sent', 'Net Recv'])

# Função para ler os dados de processos
def read_process_data():
    _, process_file = get_log_filename()
    if os.path.exists(process_file):
        return pd.read_csv(process_file)
    else:
        return pd.DataFrame(columns=['Hora', 'PID', 'Nome', 'Usuario', 'CPU (%)', 'Memoria (%)', 'Disco Lido (bytes)', 'Disco Escrito (bytes)', 'Rede Enviada (bytes)', 'Rede Recebida (bytes)'])

# Função para obter detalhes adicionais do processo
def get_process_details(process_name):
    details = {}
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                process = psutil.Process(proc.info['pid'])
                details['cmdline'] = ' '.join(process.cmdline())
                details['exe'] = process.exe()
                details['cwd'] = process.cwd()
                details['threads'] = [thread.id for thread in process.threads()]
                details['connections'] = [conn._asdict() for conn in process.connections()]
                details['open_files'] = [file.path for file in process.open_files()]
                break
    except psutil.NoSuchProcess:
        pass
    return details

# Inicializando o app Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Monitoramento de Desempenho"),

    dcc.Graph(id='performance-graph'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),

    html.Div([
        html.Label('Selecione o Nome do Processo:'),
        dcc.Dropdown(id='process-name-dropdown')
    ]),

    dcc.Graph(id='process-graph'),

    html.Div(id='process-details', style={'white-space': 'pre-line'})
])

@app.callback(
    Output('performance-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_performance_graph(n_intervals):
    df_performance = read_performance_data()

    if df_performance.empty:
        return go.Figure()

    df_performance['Hora'] = pd.to_datetime(df_performance['Hora'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_performance['Hora'], y=df_performance['CPU'], mode='lines', name='CPU (%)'))
    fig.add_trace(go.Scatter(x=df_performance['Hora'], y=df_performance['RAM'], mode='lines', name='RAM (%)'))
    fig.add_trace(go.Scatter(x=df_performance['Hora'], y=df_performance['Disk'], mode='lines', name='Disco (%)'))
    fig.add_trace(go.Scatter(x=df_performance['Hora'], y=df_performance['Net Sent'], mode='lines', name='Net Sent (bytes)'))
    fig.add_trace(go.Scatter(x=df_performance['Hora'], y=df_performance['Net Recv'], mode='lines', name='Net Recv (bytes)'))

    fig.update_layout(title='Desempenho do Sistema', xaxis_title='Hora', yaxis_title='Uso (%)')

    return fig

@app.callback(
    Output('process-name-dropdown', 'options'),
    Input('interval-component', 'n_intervals')
)
def update_process_dropdown(n_intervals):
    df_process = read_process_data()
    process_names = df_process['Nome'].unique()
    return [{'label': name, 'value': name} for name in process_names]

@app.callback(
    Output('process-graph', 'figure'),
    [Input('process-name-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_process_graph(selected_name, n_intervals):
    df_process = read_process_data()

    if selected_name is None or df_process.empty:
        return go.Figure()

    df_process = df_process[df_process['Nome'] == selected_name]

    if df_process.empty:
        return go.Figure()

    df_process['Hora'] = pd.to_datetime(df_process['Hora'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['CPU (%)'], mode='lines', name='CPU (%)'))
    fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['Memoria (%)'], mode='lines', name='Memoria (%)'))
    fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['Disco Lido (bytes)'], mode='lines', name='Disco Lido (bytes)'))
    fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['Disco Escrito (bytes)'], mode='lines', name='Disco Escrito (bytes)'))
    fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['Rede Enviada (bytes)'], mode='lines', name='Rede Enviada (bytes)'))
    fig.add_trace(go.Scatter(x=df_process['Hora'], y=df_process['Rede Recebida (bytes)'], mode='lines', name='Rede Recebida (bytes)'))

    fig.update_layout(title=f'Dados do Processo: {selected_name}', xaxis_title='Hora', yaxis_title='Uso')

    return fig

@app.callback(
    Output('process-details', 'children'),
    Input('process-name-dropdown', 'value')
)
def update_process_details(selected_name):
    if selected_name is None:
        return "Selecione um processo para ver os detalhes."

    details = get_process_details(selected_name)

    if not details:
        return "Detalhes do processo não disponíveis."

    details_text = (
        f"Comando: {details.get('cmdline', 'N/A')}\n"
        f"Executável: {details.get('exe', 'N/A')}\n"
        f"Diretório de Trabalho: {details.get('cwd', 'N/A')}\n"
        f"Threads: {', '.join(map(str, details.get('threads', [])))}\n"
        f"Conexões: {', '.join(map(str, details.get('connections', [])))}\n"
        f"Arquivos Abertos: {', '.join(details.get('open_files', []))}"
    )

    return details_text

if __name__ == '__main__':
    app.run_server(debug=True)
