import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote, urljoin

BASE_URL = "https://uniteapi.dev"


def get_text_safe(tag):
    return tag.get_text(strip=True) if tag else "-"


def uniteapi(nick):
    url = f"{BASE_URL}/p/{nick}"

    try:
        page = requests.get(url, timeout=10)

        if page.status_code != 200:
            return None

        soup = BeautifulSoup(page.content, 'html.parser')

        elements = soup.find_all(class_="sc-6d6ea15e-1 gpvunk")

        if len(elements) < 4:
            return None

        profile_name = get_text_safe(elements[0])
        total_battles = get_text_safe(elements[1])
        wins = get_text_safe(elements[2])
        win_rate = get_text_safe(elements[3])

        # 🔹 level
        profile_level = get_text_safe(
            soup.find(class_='sc-af604853-1 JFESd')
        )

        # 🔹 último login
        last_login_tag = soup.find(class_='sc-6d6ea15e-2 ckgDBX')
        text = get_text_safe(last_login_tag)

        last_login = (
            text.replace("Last online:", "").strip()
            if text and "Last online:" in text
            else (text or "Online")
)
        # 🔹 rank
        rank_name = get_text_safe(soup.find(class_='sc-6d6ea15e-3 hxGuyl'))
        rank_points = (
            get_text_safe(soup.find(class_='sc-6d6ea15e-1 iucKOC'))
            if rank_name == "Legend"
            else "-"
)
        # 🔹 fair play
        fpp = get_text_safe(
            soup.find(class_='CircularProgressbar-text')
        )

        # 🔹 avatar
        avatar_url = None
        avatar_tag = soup.find("img", alt="Avatar frame")

        if avatar_tag:
            src = avatar_tag.get("src", "")

            if "url=" in src:
                parsed = urlparse(src)
                query = parse_qs(parsed.query)
                raw_url = query.get("url", [""])[0]

                if raw_url:
                    decoded_path = unquote(raw_url)
                    avatar_url = urljoin(BASE_URL, decoded_path)
            else:
                avatar_url = src

        return (
            profile_name,
            profile_level,
            last_login,
            rank_name,
            rank_points,
            total_battles,
            wins,
            win_rate,
            fpp,
            avatar_url
        )

    except Exception as e:
        print(f"Erro uniteapi: {e}")
        return None