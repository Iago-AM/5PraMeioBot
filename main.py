import discord
from discord import app_commands
import random
import os

import timezone
import data
import uniteapidev
import tipagem
import asyncio

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await tree.sync()
            self.synced = True

        print(f'Logado como {self.user}')


client = Client()
tree = app_commands.CommandTree(client)

LOCATIONS = list(timezone.TIMEZONES.keys())
TIPOS = list(tipagem.TIPOS_PTBR.keys())

@tree.command(name='coordenada', description='Descubra hora e coordenadas.')
@app_commands.describe(localizacao='Escolha a cidade')
@app_commands.choices(
    localizacao=[app_commands.Choice(name=loc, value=loc) for loc in LOCATIONS]
)
async def coordenada(interaction: discord.Interaction, localizacao: app_commands.Choice[str]):

    cidade = localizacao.value
    hora = timezone.horalocal(cidade)
    info = data.DATA.get(cidade)

    if not info:
        await interaction.response.send_message("Dados não encontrados.")
        return

    await interaction.response.send_message(
        f'{info["flag"]} **{cidade} ({info["code"]})** {info["flag"]}\n'
        f'🗓 {hora}\n'
        f'📍 {info["coords"]}'
    )

    print(f'{info["flag"]} **{cidade} ({info["code"]})** {info["flag"]}\n')
    print(f'🗓 {hora}\n')
    print(f'📍 {info["coords"]}')


@tree.command(name='moeda', description='Gire uma moeda.')
async def moeda(interaction: discord.Interaction):
    resultado = random.choice(['Cara', 'Coroa'])
    await interaction.response.send_message(f'🪙 Resultado: **{resultado}**')

@tree.command(name='unite', description='Procure seu perfil do Pokémon Unite')
@app_commands.describe(nick='Seu nick completo e exato')
async def unite(interaction: discord.Interaction, nick: str):

    await interaction.response.defer()

    try:
        result = await asyncio.to_thread(uniteapidev.uniteapi, nick)

        if not result:
            await interaction.followup.send("❌ Perfil não encontrado.")
            return

        (profile_name, profile_level, last_login,
         rank_name, rank_points, total_battles,
         wins, win_rate, fpp, avatar_url) = result

        embed = discord.Embed(
            title=f"🎮 {profile_name}",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="📊 Perfil",
            value=(
                f"Level: {profile_level}\n"
                f"Último login: {last_login}"
            ),
            inline=False
        )

        embed.add_field(
            name="🏆 Rank",
            value=f"{rank_name} ({rank_points})",
            inline=False
        )

        embed.add_field(
            name="⚔️ Estatísticas",
            value=(
                f"Batalhas: {total_battles}\n"
                f"Vitórias: {wins}\n"
                f"Winrate: {win_rate}"
            ),
            inline=False
        )

        embed.add_field(
            name="💯 Fair Play",
            value=fpp,
            inline=False
        )

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        embed.set_footer(text="Dados coletados de uniteapi.dev")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        print(e)
        await interaction.followup.send("❌ Erro ao buscar perfil.")

@tree.command(name="tipo", description="Veja a efetividade de um tipo Pokémon")
@app_commands.describe(tipo="Escolha o tipo")
@app_commands.choices(
    tipo=[app_commands.Choice(name=t, value=t) for t in TIPOS]
)
async def type_cmd(interaction: discord.Interaction, tipo: app_commands.Choice[str]):

    await interaction.response.defer()

    tipo_escolhido = tipo.value

    result = await asyncio.to_thread(tipagem.get_type, tipo_escolhido)

    if not result:
        await interaction.followup.send("❌ Tipo inválido.")
        return

    nome_tipo, fortes, fracos, imunes = result

    embed = discord.Embed(
        title=f"⚔️ Tipo: {nome_tipo}",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="✅ Forte contra",
        value=", ".join(fortes) if fortes else "Nenhum",
        inline=False
    )

    embed.add_field(
        name="❌ Fraco contra",
        value=", ".join(fracos) if fracos else "Nenhum",
        inline=False
    )

    embed.add_field(
        name="🚫 Não afeta",
        value=", ".join(imunes) if imunes else "Nenhum",
        inline=False
    )

    await interaction.followup.send(embed=embed)

with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

client.run(TOKEN)