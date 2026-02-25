import os
import json
import gspread
import google.generativeai as genai
from datetime import datetime

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Google Sheets
google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
gc = gspread.service_account_from_dict(google_creds)
sheet = gc.open("Radar_Agritech_Prospects").sheet1

def buscar_empresas():
    prompt = """
    Liste 2 empresas brasileiras do setor agritech
    focadas em robótica ou IA aplicada
    que tiveram crescimento recente.

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

    response = model.generate_content(prompt)
    return response.text

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
            "Gemini Scan"
        ]

        sheet.append_row(row)

if __name__ == "__main__":
    dados = buscar_empresas()
    atualizar_planilha(dados)
