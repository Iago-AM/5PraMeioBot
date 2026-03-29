import requests
from datetime import datetime
import time

BASE_URL = "https://worldtimeapi.org/api/timezone/"

TIMEZONES = {
    "Kiribati": "Pacific/Kiritimati",
    "Wellington": "Pacific/Auckland",
    "Sydney": "Australia/Sydney",
    "Busan": "Asia/Seoul",
    "Tóquio": "Asia/Tokyo",
    "Singapura": "Asia/Singapore",
    "Taipei": "Asia/Taipei",
    "Mumbai": "Asia/Colombo",
    "Dubai": "Asia/Dubai",
    "Moscow": "Europe/Moscow",
    "Izmir": "Europe/Istanbul",
    "Tessalônica": "Europe/Athens",
    "Zaragoza": "Europe/Madrid",
    "Budapeste": "Europe/Budapest",
    "Ilhas Canárias": "Atlantic/Canary",
    "Londres": "Europe/London",
    "Parque Ibirapuera": "America/Sao_Paulo",
    "Santo Domingo": "America/Santo_Domingo",
    "New York": "America/New_York",
    "Cidade do México": "America/Mexico_City",
    "Calgary": "America/Edmonton",
    "Pier 39": "America/Los_Angeles",
    "Alasca": "America/Sitka",
    "Honolulu": "Pacific/Honolulu",
    "Pago Pago": "Pacific/Pago_Pago"
}


import requests
import time

def horalocal(cidade: str) -> str:
    timezone = TIMEZONES.get(cidade)

    if not timezone:
        return "Cidade não encontrada."

    url = f"{BASE_URL}{timezone}"

    for tentativa in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            return formatar_data(data["datetime"])

        except requests.RequestException:
            if tentativa < 2:
                time.sleep(1)
            else:
                return "Erro ao obter horário. Caso deseje essa informação, tente novamente. A API de horário pode estar instável ou indisponível no momento."


def formatar_data(datetime_str: str) -> str:

    dt = datetime.fromisoformat(datetime_str)

    return dt.strftime("%d/%m/%Y - %H:%M:%S")