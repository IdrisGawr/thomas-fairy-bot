import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
member = discord.Member
bot = commands.Bot(command_prefix='!')


@bot.command(
    name='stress',
    brief='Tirada dado de estrés (ej. !stress)',
    help='El bot te mostrará un resultado aleatorio entre 0 (pifia) y 9'
)
async def roll(ctx):
    multiplicador = 1
    tiradas = []

    while True:
        if multiplicador > 1:
            resultado = random.choice(range(1, 11))
        else:
            resultado = random.choice(range(0, 10))
        if resultado == 1:
            multiplicador = multiplicador * 2
            tiradas = tiradas + [resultado]
        else:
            tiradas = tiradas + [resultado]
            break
    total_stress = tiradas[-1] * multiplicador

    if 0 in tiradas:
        dice = '***¡PIFIA!***\n\n'
    elif 1 in tiradas:
        dice = '***¡CRÍTICO!***\n\n'
    else:
        dice = ''
    await ctx.send(f'```{dice}TOTAL ESTRÉS: {total_stress}\nTIRADAS DADOS: {tiradas}\n```{ctx.author.mention}')


@bot.command(
    name='dados',
    brief='Tirada de dados poliédricos (ej. !dados 2d8)',
    help='Introduce tras !dados los dadosque quieras tirar, por ejemplo 1d10 será igual a tirar un dado de diez caras'
)
async def roll(ctx, dados_poliedricos: str):
    dados = [
        str(random.choice(range(1, int(dados_poliedricos.split("d")[1]) + 1)))
        for _ in range(int(dados_poliedricos.split("d")[0]))
        ]
    dados.sort()
    dados = ', '.join(dados)
    await ctx.send(f'```{dados}\n```{ctx.author.mention}')


@bot.command(
    name='simple',
    brief='Tirada dado simple (ej. !simple)',
    help='El bot te mostrará un resultado aleatorio entre 0 y 9'
)
async def roll(ctx):
    dado_simple = str(random.choice(range(0, 10)))
    await ctx.send(f'```DADO SIMPLE: {dado_simple}\n```{ctx.author.mention}')


@bot.command(
    name='pifia',
    brief='Tirada dados de pifia (ej. !pifia 2)',
    help='Introduce tras !pifia los dados de pifia que quieras tirar, por ejemplo 1 '
         'será igual a tirar un dado de diez caras'
)
async def roll(ctx, dados_pifia: str):
    dado_pifia = [
        str(random.choice(range(0, 10)))
        for _ in range(int(dados_pifia))
    ]
    dado_pifia.sort()
    pifias = 0
    has_pifiado = ''
    for d in dado_pifia:
        if d == '0':
            pifias += 1
            has_pifiado = '*** ¡PIFIASTE! ***\n\n'
        else:
            continue
    dado_pifia = has_pifiado + 'DADOS DE PIFIA: ' + ', '.join(dado_pifia) + '\n(CEROS SACADOS: ' + str(pifias) + ')'
    await ctx.send(f'```{dado_pifia}\n```{ctx.author.mention}')


@bot.command(
    name='envejecimiento',
    brief='Tirada de envejecimiento (ej. !envejecimiento -4)',
    help='Añade el modificador a la tirada de envejecimiento para saber el resultado, por ejemplo !envejecimiento -12'
)
async def roll(ctx, modificador_envejecimiento: str):
    multiplicador = 1
    tiradas = []
    while True:
        if multiplicador > 1:
            resultado = random.choice(range(1, 11))
        else:
            resultado = random.choice(range(0, 10))
        if resultado == 1:
            multiplicador = multiplicador * 2
            tiradas = tiradas + [resultado]
        else:
            tiradas = tiradas + [resultado]
            break
    total_env = tiradas[-1] * multiplicador
    if '-' in modificador_envejecimiento:
        total_env = total_env - int(modificador_envejecimiento.split("-")[1])
    if '+' in modificador_envejecimiento:
        total_env = total_env + int(modificador_envejecimiento.split("+")[1])
    if total_env <= 2:
        resultado_env = 'La edad aparente no aumenta.'
    elif total_env < 10:
        resultado_env = 'La edad aparente aumenta un año.'
    elif total_env < 13:
        resultado_env = 'Gana 1 Punto de Envejecimiento en cualquier Característica.'
    elif total_env == 13:
        resultado_env = 'Gana los suficientes Puntos de Envejecimiento (en cualquier Característica) ' \
                        'para alcanzar el siguiente nivel en Decrepitud, y sufre una Crisis.'
    elif total_env == 14:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Rapidez.'
    elif total_env == 15:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Vitalidad.'
    elif total_env == 16:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Percepcion.'
    elif total_env == 17:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Presencia.'
    elif total_env == 18:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Fuerza y Vitalidad.'
    elif total_env == 19:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Destreza y Rapidez.'
    elif total_env == 20:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Comunicación y Presencia.'
    elif total_env == 21:
        resultado_env = 'Gana 1 Punto de Envejecimiento en Inteligencia y Percepción.'
    else:
        resultado_env = 'Gana los suficientes Puntos de Envejecimiento (en cualquier Característica) ' \
                        'para alcanzar el siguiente nivel en Decrepitud, y sufre una Crisis.'

    await ctx.send(f'```{resultado_env}\nTOTAL ENVEJECIMIENTO: {total_env}\nTIRADAS DE DADOS: {tiradas}\n```{ctx.author.mention}')


@bot.command(
    name='crisis',
    brief='Tirada de crisis por envejecimiento (ej. !crisis +4)',
    help='DADO SIMPLE + EDAD/10 (redondeando hacia arriba) + PUNTUACIÓN DECREPITUD'
)
async def roll(ctx, modificador_crisis: str):
    dado_simple = random.choice(range(0, 10))
    total_crisis = int(modificador_crisis.split("+")[1]) + dado_simple
    if total_crisis <= 8:
        resultado_crisis = 'En cama durante una semana.'
    elif total_crisis < 15:
        resultado_crisis = 'En cama durante un mes.'
    elif total_crisis == 15:
        resultado_crisis = 'Enfermedad menor. Tirada de Vitalidad 3+ o CrCo 20 para sobrevivir.'
    elif total_crisis == 16:
        resultado_crisis = 'Enfermedad seria. Tirada de Vitalidad 6+ o CrCo 25 para sobrevivir.'
    elif total_crisis == 17:
        resultado_crisis = 'Enfermedad grave. Tirada de Vitalidad 9+ o CrCo 30 para sobrevivir.'
    elif total_crisis == 18:
        resultado_crisis = 'Enfermedad crítica. Tirada de Vitalidad 12+ o CrCo 35 para sobrevivir.'
    else:
        resultado_crisis = 'Enfermedad terminal. Necesita de CrCo 40 para sobrevivir.'

    await ctx.send(f'```{resultado_crisis}\nTOTAL CRISIS: {total_crisis}\nTIRADA DE DADOS: {dado_simple}\n```{ctx.author.mention}')

bot.run(TOKEN)
