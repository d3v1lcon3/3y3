#!/usr/bin/env python3

import json
import sys
import os
from aiohttp import ClientSession, BasicAuth
import asyncio

# --- Configuração - Altere estas variáveis ---
THEHIVE_URL = "https://192.168.24.100:9000"  # IMPORTANTE: Use a URL base do seu TheHive
THEHIVE_API_KEY = "RvgVZqcRWoK6C2QkjpOy1b7Ufgho0BJ9" # IMPORTANTE: Cole a chave que você gerou
# --- Fim da Configuração ---

# Função para ler o alerta do Wazuh
def read_alert( ):
    alert_file = open(sys.argv[1])
    alert_json = json.load(alert_file)
    alert_file.close()
    return alert_json

# Função assíncrona para criar o caso no TheHive
async def create_thehive_case(alert):
    # Extrai informações do alerta do Wazuh para criar o caso
    rule_id = alert['rule']['id']
    rule_description = alert['rule']['description']
    agent_name = alert.get('agent', {}).get('name', 'N/A')
    agent_id = alert.get('agent', {}).get('id', 'N/A')
    full_log = alert.get('full_log', 'No full log available.')

    # Título do caso no TheHive
    case_title = f"Wazuh Alert: {rule_description} on {agent_name}"

    # Descrição do caso (em formato Markdown)
    case_description = f"""
**Wazuh Alert Details**

- **Rule ID:** {rule_id}
- **Rule Description:** {rule_description}
- **Agent Name:** {agent_name}
- **Agent ID:** {agent_id}

---
**Full Log:**
{full_log}
"""
    # Monta o corpo da requisição para a API do TheHive
    case_data = {
        "title": case_title,
        "description": case_description,
        "tags": ["Wazuh", f"rule:{rule_id}", f"agent:{agent_name}"],
        "severity": 2,  # 1=Low, 2=Medium, 3=High, 4=Critical
        "tlp": 2, # TLP:AMBER
    }

    # Ajusta a severidade do caso com base no nível do alerta do Wazuh
    alert_level = alert['rule']['level']
    if alert_level >= 12:
        case_data['severity'] = 4 # Critical
    elif alert_level >= 9:
        case_data['severity'] = 3 # High
    elif alert_level >= 6:
        case_data['severity'] = 2 # Medium
    else:
        case_data['severity'] = 1 # Low

    # Cria a sessão HTTP e envia a requisição para a API
    # O verify_ssl=False é usado para certificados autoassinados. Em produção, use um certificado válido.
    async with ClientSession(auth=BasicAuth(login=THEHIVE_API_KEY, password=''), connector_owner=False) as session:
        try:
            async with session.post(f"{THEHIVE_URL}/api/v1/case", json=case_data, verify_ssl=False) as response:
                if response.status == 201:
                    print(f"Successfully created TheHive case for alert {alert['id']}")
                else:
                    response_text = await response.text()
                    print(f"Error creating TheHive case. Status: {response.status}, Response: {response_text}")
        except Exception as e:
            print(f"An exception occurred: {e}")

# Função principal
if __name__ == "__main__":
    # Lê o alerta passado pelo Wazuh
    alert_data = read_alert()
    # Cria o caso no TheHive
    asyncio.run(create_thehive_case(alert_data))




