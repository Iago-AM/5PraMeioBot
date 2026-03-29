# 🤖 Discord Pokémon & Utility Bot

Um bot para Discord com funcionalidades de:
- 🌍 Coordenadas e horários pelo mundo
- 🎮 Integração com Pokémon Unite
- ⚔️ Tipagens Pokémon (efetividade)
- 🎲 Comandos interativos

---

## 🚀 Funcionalidades

### 🌍 Coordenadas
Use `/coordenada` para ver:
- Data e hora local
- Coordenadas geográficas

---

### ⚔️ Tipagens Pokémon
Use `/type` para descobrir:
- Tipos fortes contra outros
- Tipos fracos
- Imunidades

---

### 🎮 Pokémon Unite
Use `/unite` para buscar:
- Perfil do jogador
- Rank
- Estatísticas

---

### 🎲 Extras
- `/moeda` → Cara ou coroa

---

## 🧠 Tecnologias

- Python 3.11+
- discord.py
- requests
- BeautifulSoup

---

## 📁 Estrutura

- main.py # Bot principal
- timezone.py # Horários globais
- tipagem.py # Efetividade de tipos Pokémon
- uniteapidev.py # Scraper Pokémon Unite
- data.py # Dados (bandeiras, coords)
