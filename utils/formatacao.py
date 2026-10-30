from datetime import date


def formatar_data_br(data: date) -> str:
    return data.strftime("%d/%m/%Y")
