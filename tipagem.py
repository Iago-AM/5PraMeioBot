import requests

BASE_URL = "https://pokeapi.co/api/v2/type/"

TYPE_TRANSLATIONS = {
    "fire": "Fogo",
    "water": "Água",
    "grass": "Planta",
    "electric": "Elétrico",
    "ice": "Gelo",
    "fighting": "Lutador",
    "poison": "Venenoso",
    "ground": "Terra",
    "flying": "Voador",
    "psychic": "Psíquico",
    "bug": "Inseto",
    "rock": "Pedra",
    "ghost": "Fantasma",
    "dragon": "Dragão",
    "dark": "Sombrio",
    "steel": "Aço",
    "fairy": "Fada",
    "normal": "Normal"
}

TIPOS_PTBR = {
    "Fogo": "Fire",
    "Água": "Water",
    "Planta": "Grass",
    "Elétrico": "Electric",
    "Gelo": "Ice",
    "Lutador": "Fighting",
    "Venenoso": "Poison",
    "Terra": "Ground",
    "Voador": "Flying",
    "Psíquico": "Psychic",
    "Inseto": "Bug",
    "Pedra": "Rock",
    "Fantasma": "Ghost",
    "Dragão": "Dragon",
    "Sombrio": "Dark",
    "Aço": "Steel",
    "Fada": "Fairy",
    "Normal": "Normal"
}

REVERSE_TYPES = {v.lower(): k for k, v in TYPE_TRANSLATIONS.items()}


def traduzir_lista(lista):
    return [TYPE_TRANSLATIONS.get(t, t) for t in lista]


def get_type(tipo: str):
    tipo = tipo.lower()

    # aceita português também
    tipo = REVERSE_TYPES.get(tipo, tipo)

    try:
        res = requests.get(f"{BASE_URL}{tipo}", timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()

        fortes = [t["name"] for t in data["damage_relations"]["double_damage_to"]]
        fracos = [t["name"] for t in data["damage_relations"]["double_damage_from"]]
        imunes = [t["name"] for t in data["damage_relations"]["no_damage_to"]]

        return (
            TYPE_TRANSLATIONS.get(tipo, tipo.capitalize()),
            traduzir_lista(fortes),
            traduzir_lista(fracos),
            traduzir_lista(imunes)
        )

    except:
        return None