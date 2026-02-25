import os
import json
from openai import OpenAI
import gspread
from datetime import datetime

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Credenciais Google vindas do Secret
google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

gc = gspread.service_account_from_dict(google_creds)
sheet = gc.open("Radar_Agritech_Prospects").sheet1

def buscar_empresas():
    prompt = """
    Liste 3 empresas brasileiras do setor agritech
    focadas em robótica, sensores ou IA aplicada,
    que apresentaram crescimento ou investimento recente.

    Retorne apenas JSON válido neste formato:
    [
      {
        "empresa": "",
        "site": "",
        "cidade": "",
        "funcionarios": "",
        "receita": "",
        "cto": "",
        "produto": "",
        "crescimento": "",
        "complexidade": ""
      }
    ]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def atualizar_planilha(dados_json):
    empresas = json.loads(dados_json)

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
            "",
            "IA Scan"
        ]

        sheet.append_row(row)

if __name__ == "__main__":
    dados = buscar_empresas()
    atualizar_planilha(dados)
