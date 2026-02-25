import os
import json
import gspread
import google.generativeai as genai
from datetime import datetime

# =========================
# CONFIGURAÇÃO GEMINI
# =========================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.0-pro")

# =========================
# CONFIGURAÇÃO GOOGLE SHEETS
# =========================
google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
gc = gspread.service_account_from_dict(google_creds)

# Nome EXATO da planilha
PLANILHA_NOME = "Radar_Agritech_Prospects"

sheet = gc.open(PLANILHA_NOME).sheet1


# =========================
# FUNÇÃO BUSCAR EMPRESAS
# =========================
def buscar_empresas():
    prompt = """
    Liste 2 empresas brasileiras do setor agritech
    focadas em robótica ou IA aplicada
    que tiveram crescimento recente.

    Retorne SOMENTE JSON válido.
    Não use markdown.
    Não escreva explicações.
    """

    response = model.generate_content(prompt)
    texto = response.text.strip()

    print("=== RESPOSTA BRUTA DO GEMINI ===")
    print(texto)
    print("=== FIM RESPOSTA ===")

    # Remove blocos markdown se existirem
    if "```" in texto:
        texto = texto.replace("```json", "").replace("```", "").strip()

    # Extrair somente parte JSON (entre [ e ])
    inicio = texto.find("[")
    fim = texto.rfind("]")

    if inicio != -1 and fim != -1:
        texto = texto[inicio:fim+1]

    try:
        empresas = json.loads(texto)
        return empresas
    except Exception as e:
        print("Erro ao converter JSON:", e)
        return []


# =========================
# FUNÇÃO ATUALIZAR PLANILHA
# =========================
def atualizar_planilha(empresas):
    if not empresas:
        print("Nenhuma empresa válida encontrada.")
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

    print(f"{len(empresas)} empresas adicionadas com sucesso.")


# =========================
# EXECUÇÃO PRINCIPAL
# =========================
if __name__ == "__main__":
    print("Iniciando scanner...")
    empresas = buscar_empresas()
    atualizar_planilha(empresas)
    print("Scanner finalizado.")
