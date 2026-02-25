import os
import json
import gspread
from datetime import datetime

# Credenciais Google vindas do Secret
google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

gc = gspread.service_account_from_dict(google_creds)
sheet = gc.open("Radar_Agritech_Prospects").sheet1

def buscar_empresas_mock():
    # Dados simulados (MOCK)
    return [
        {
            "empresa": "AgroTech Robotics",
            "site": "https://agrotechrobotics.com.br",
            "cidade": "Ribeirão Preto - SP",
            "funcionarios": "45",
            "receita": "R$ 12M",
            "cto": "João Silva",
            "produto": "Robô autônomo para pulverização inteligente",
            "crescimento": "Captação Série A em 2025",
            "complexidade": "Alta"
        },
        {
            "empresa": "SmartFarm AI",
            "site": "https://smartfarmai.com.br",
            "cidade": "Londrina - PR",
            "funcionarios": "32",
            "receita": "R$ 8M",
            "cto": "Maria Souza",
            "produto": "Plataforma de IA para monitoramento agrícola",
            "crescimento": "Expansão nacional 2025",
            "complexidade": "Alta"
        }
    ]

def atualizar_planilha(empresas):
    for empresa in empresas:
        row = [
            datetime.today().strftime('%Y-%m-%d'),
            empresa["empresa"],
            empresa["site"],
            empresa["cidade"],
            empresa["funcionarios"],
            empresa["receita"],
            empresa["cto"],
            empresa["produto"],
            empresa["crescimento"],
            empresa["complexidade"],
            "10",
            "Mock Test"
        ]

        sheet.append_row(row)

if __name__ == "__main__":
    dados = buscar_empresas_mock()
    atualizar_planilha(dados)
