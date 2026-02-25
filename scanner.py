def buscar_empresas():
    prompt = """
    Liste 2 empresas brasileiras do setor agritech
    focadas em robótica ou IA aplicada
    que tiveram crescimento recente.

    Retorne APENAS JSON puro.
    Não use markdown.
    Não use ```json.
    """

    response = model.generate_content(prompt)
    texto = response.text.strip()

    # Remove possíveis blocos markdown
    if texto.startswith("```"):
        texto = texto.replace("```json", "").replace("```", "").strip()

    return texto
