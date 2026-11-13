def validar_texto_obrigatorio(valor: str, campo: str) -> str:
    texto = valor.strip()
    if not texto:
        raise ValueError(f"O campo '{campo}' é obrigatório.")
    return texto
