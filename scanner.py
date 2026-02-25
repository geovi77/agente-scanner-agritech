import os
import json
import gspread
from google import genai
from datetime import datetime

# =========================
# CONFIG GEMINI (NOVA API)
# =========================
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# =========================
# GOOGLE SHEETS
# =========================
google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
gc = gspread.service_account_from_dict(google_creds)

PLANILHA_NOME = "Radar_Agritech_Prospects"
sheet = gc.open(PLANILHA_NOME).sheet1


def buscar_empresas():
    prompt = """
    Liste 2 empresas brasileiras do setor agritech
    focadas em robótica ou IA aplicada
    que tiveram crescimento recente.

    Retorne SOMENTE JSON válido.
    Não use markdown.
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=prompt
    )

    texto = response.text.strip()

    print("=== RESPOSTA GEMINI ===")
    print(texto)
    print("=======================")

    # Limpeza básica
    if "```" in texto:
        texto = texto.replace("```json", "").replace("```", "").strip()

    inicio = texto.find("[")
    fim = texto.rfind("]")

    if inicio != -1 and fim != -1:
        texto = texto[inicio:fim+1]

    try:
        return json.loads(texto)
    except:
        return []


def atualizar_planilha(empresas):
    if not empresas:
        print("Nenhuma empresa encontrada.")
        return

    for empresa in empresas:
        row = [
            datetime.today().strftime('%Y-%m-%d'),
            empresa.get("empresa", ""),
            empresa.get("site", ""),
            empresa.get("cidade", ""),
            empresa.get("funcionarios", ""),
            empresa.get("receita", ""),
            empresa.get("cto", ""),
            empresa.get("produto", ""),
            empresa.get("crescimento", ""),
            empresa.get("complexidade", ""),
            "10",
            "Gemini Scan"
        ]

        sheet.append_row(row)

    print(f"{len(empresas)} empresas adicionadas.")


if __name__ == "__main__":
    print("Iniciando scanner...")
    empresas = buscar_empresas()
    atualizar_planilha(empresas)
    print("Finalizado.")
