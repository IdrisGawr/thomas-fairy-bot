"""
Thomas Module
Ars Magica 5ed Bot
"""

import asyncio
import os
import random

import discord
import psycopg2
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
IP = os.getenv("HOST_IP")
DATABASE = os.getenv("POSTGRES_DATABASE")
USERNAME = os.getenv("POSTGRES_USERNAME")
PASSWORD = os.getenv("POSTGRES_PASSWORD")

client = discord.Client()
Member = discord.Member
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    """
    Print connect to Discord
    """
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_command_error(ctx, error):
    """
    Handle possible errors
    """
    await ctx.send(f"An error occurred: {str(error)}")


@bot.command(
    name="stress",
    brief="Tirada dado de estrés (ej. !stress o !stress +5)",
    help="El bot te mostrará un resultado aleatorio entre 0 y 9 y le sumará "
    "el bono introducido",
)
async def roll_stress(ctx, *args):
    """
    Roll a stress d10 dice assuming Ars Magica 5ed rules
    """
    multiplicador = 1
    tiradas = []
    bono = 0
    operador = "+"

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
    for arg in args:
        if "-" in arg:
            operador = "-"
        if arg is None:
            bono = 0
        else:
            bono = int(arg.replace(" ", "").split(operador)[1])

    if operador == "+":
        total_suma = bono + int(total_stress)
    else:
        total_suma = int(total_stress) - bono

    if 0 in tiradas:
        dice = "***¡POSIBLE PIFIA!***\n\n"
    elif 1 in tiradas:
        dice = "***¡CRÍTICO!***\n\n"
    else:
        dice = ""
    await ctx.send(
        f"```ini\n{dice}TOTAL DE ESTRÉS: {total_suma}\nOPERACIÓN: "
        f"[{total_stress} {operador} {bono}]\nTIRADAS DE DADOS: "
        f"{tiradas}```{ctx.author.mention}"
    )


@bot.command(
    name="dados",
    brief="Tirada de dados poliédricos (ej. !dados 2d8)",
    help="Introduce tras !dados los dadosque quieras tirar, por ejemplo 1d10 "
    "será igual a tirar un dado de diez caras",
)
async def roll_poly(ctx, dados_poliedricos: str):
    """
    Roll a set of polyhedral dices
    """
    dice = [
        str(
            random.choice(
                range(1, int(dados_poliedricos.split("d")[1]) + 1)
            )
        )
        for _ in range(int(dados_poliedricos.split("d")[0]))
    ]
    dice.sort()
    dice = ", ".join(dice)
    await ctx.send(f"```{dice}```{ctx.author.mention}")


@bot.command(
    name="simple",
    brief="Tirada dado simple (ej. !simple o !simple +5)",
    help="El bot te mostrará un resultado aleatorio entre 0 y 9 y le sumará "
    "el bono introducido",
)
async def roll_simple(ctx, *args):
    """
    Roll a simple d10 dice
    """
    bono = 0
    operador = "+"
    for arg in args:
        if "-" in arg:
            operador = "-"
        if arg is None:
            bono = 0
        else:
            bono = int(arg.replace(" ", "").split(operador)[1])
    dice = [str(random.choice(range(0, 10)))]
    dice.sort()
    dice = ", ".join(dice)
    if operador == "+":
        total_suma = int(dice) + bono
    else:
        total_suma = int(dice) - bono

    await ctx.send(
        f"```TOTAL SIMPLE: {total_suma}\nOPERACIÓN: [{dice} {operador} "
        f"{bono}]\nTIRADA DE DADO: {dice}```{ctx.author.mention}"
    )


@bot.command(
    name="pifia",
    brief="Tirada dados de pifia (ej. !pifia 2)",
    help="Introduce tras !pifia los dados de pifia que quieras tirar, por "
    "ejemplo 1 será igual a tirar un dado de diez caras",
)
async def roll_pifia(ctx, dados_pifia: str):
    """
    Roll a set of pifia dice(s) following Ars Magica 5ed rules
    """
    dice = [
        str(random.choice(range(0, 10)))
        for _ in range(int(dados_pifia))
    ]
    dice.sort()
    pifias = 0
    has_pifiado = ""
    for number in dice:
        if number == "0":
            pifias += 1
            has_pifiado = "*** ¡PIFIASTE! ***\n\n"
        else:
            continue
    dice = (
        has_pifiado
        + "DADOS DE PIFIA: "
        + ", ".join(dice)
        + "\n(CEROS SACADOS: "
        + str(pifias)
        + ")"
    )
    await ctx.send(f"```fix\n{dice}```{ctx.author.mention}")


@bot.command(
    name="envejecimiento",
    brief="Tirada de envejecimiento (ej. !envejecimiento -4)",
    help="Añade el modificador a la tirada de envejecimiento para saber el "
    "resultado, por ejemplo !envejecimiento -12",
)
async def roll_age(ctx, modificador_envejecimiento: str):
    """
    Roll a d10 dice following Ars Magica 5ed rules
    """
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
    if "-" in modificador_envejecimiento:
        total_env = total_env - int(
            modificador_envejecimiento.split("-")[1]
        )
    if "+" in modificador_envejecimiento:
        total_env = total_env + int(
            modificador_envejecimiento.split("+")[1]
        )
    if total_env <= 2:
        resultado_env = "La edad aparente no aumenta."
    elif total_env < 10:
        resultado_env = "La edad aparente aumenta un año."
    elif total_env < 13:
        resultado_env = "Gana un punto de envejecimiento en cualquier "\
        "Característica."
    elif total_env == 13:
        resultado_env = (
            "Gana los suficientes puntos de envejecimiento (en cualquier "
            "Característica) para alcanzar el siguiente nivel en Decrepitud, "
            "y sufre una Crisis."
        )
    elif total_env == 14:
        resultado_env = "Gana un punto de envejecimiento en Rapidez."
    elif total_env == 15:
        resultado_env = "Gana un punto de envejecimiento en Vitalidad."
    elif total_env == 16:
        resultado_env = "Gana un punto de envejecimiento en Percepcion."
    elif total_env == 17:
        resultado_env = "Gana un punto de envejecimiento en Presencia."
    elif total_env == 18:
        resultado_env = (
            "Gana un punto de envejecimiento en Fuerza y Vitalidad."
        )
    elif total_env == 19:
        resultado_env = (
            "Gana un punto de envejecimiento en Destreza y Rapidez."
        )
    elif total_env == 20:
        resultado_env = "Gana un punto de envejecimiento en Comunicación y "\
        "Presencia."
    elif total_env == 21:
        resultado_env = "Gana un punto de envejecimiento en Inteligencia y "\
        "Percepción."
    else:
        resultado_env = (
            "Gana los suficientes puntos de envejecimiento (en cualquier "
            "Característica) para alcanzar el siguiente nivel en Decrepitud, "
            "y sufre una Crisis."
        )

    await ctx.send(
        f"```{resultado_env}\nTOTAL DE ENVEJECIMIENTO: {total_env}\nTIRADAS "
        f"DE DADOS: {tiradas}```{ctx.author.mention}"
    )


@bot.command(
    name="crisis",
    brief="Tirada de crisis por envejecimiento (ej. !crisis +4)",
    help="DADO SIMPLE + EDAD/10 (redondeando hacia arriba) + PUNTUACIÓN "
    "DECREPITUD",
)
async def roll_crisis(ctx, modificador_crisis: str):
    """
    Roll a d10 crisis dice following Ars Magica 5ed rules
    """
    dado_simple = random.choice(range(0, 10))
    total_crisis = int(modificador_crisis.split("+")[1]) + dado_simple
    if total_crisis <= 8:
        resultado_crisis = "En cama durante una semana."
    elif total_crisis < 15:
        resultado_crisis = "En cama durante un mes."
    elif total_crisis == 15:
        resultado_crisis = "Enfermedad menor. Tirada de Vitalidad 3+ o CrCo "\
        "20 para sobrevivir."
    elif total_crisis == 16:
        resultado_crisis = "Enfermedad seria. Tirada de Vitalidad 6+ o CrCo "\
        "25 para sobrevivir."
    elif total_crisis == 17:
        resultado_crisis = "Enfermedad grave. Tirada de Vitalidad 9+ o CrCo "\
        "30 para sobrevivir."
    elif total_crisis == 18:
        resultado_crisis = "Enfermedad crítica. Tirada de Vitalidad 12+ o "\
        "CrCo 35 para sobrevivir."
    else:
        resultado_crisis = (
            "Enfermedad terminal. Necesita de CrCo 40 para sobrevivir."
        )

    await ctx.send(
        f"```diff\n-{resultado_crisis}\n\nTOTAL DE CRISIS: "
        f"{total_crisis}\nTIRADA DE DADOS: {dado_simple}```{ctx.author.mention}"
    )


# TBC
@bot.command(
    name="confianza",
    brief="Comprobación de la confianza actual o gasto de confianza",
    help="El bot mostrará la confianza del último año de la partida o gastará "
    "la confianza usada durante una tirada (e.g., !confianza Almasterin -1)",
)
async def confianza(ctx, *, argumento):
    """
    Define confidence operations in the Database
    """
    # Establecer conexión con la base de datos
    connection = psycopg2.connect(
        host=IP, database=DATABASE, user=USERNAME, password=PASSWORD
    )

    # Cursor para interactuar con la BBDD
    cursor = connection.cursor()

    # Añadimos roles que puedan ejecutar el comando
    allowed_roles = ["Administri", "Máximo Poder"]
    if argumento.lower() == 'avance':
        if any(role.name in allowed_roles for role in ctx.author.roles):
            # Solicita confirmación
            await ctx.send("¿Estás seguro de que deseas avanzar al siguiente "
                           "año? Responde con 'sí' para confirmar.")

            def check(answer):
                return answer.content.lower() == 'sí' and answer.channel == \
                    ctx.channel and answer.author == ctx.author

            try:
                _ = await bot.wait_for('message', timeout=10.0,
                                                check=check)
            except asyncio.TimeoutError:
                await ctx.send("No se ha confirmado el avance al año "
                               "siguiente. Operación cancelada.")
                connection.close()

            else:
                cursor.execute("SELECT MAX(año) FROM Confianza")
                año_actual = cursor.fetchone()[0]

                if año_actual is not None:
                    año_siguiente = año_actual + 1

                    cursor.execute("SELECT setval('confianza_id_seq', "
                                "(SELECT MAX(id) FROM confianza))")

                    cursor.execute("""
                        INSERT INTO Confianza (personaje_id, año, anuales,
                                resumenes, otros, gasto, totales)
                        SELECT personaje_id, %s, NULL, NULL, NULL, NULL, NULL
                        FROM Confianza
                        WHERE año = %s
                    """, (año_siguiente, año_actual))

                    connection.commit()

                    cursor.execute("""
                        UPDATE Confianza c1
                        SET iniciales = c2.totales, 
                        totales = c2.totales
                        FROM Confianza c2
                        WHERE c1.personaje_id = c2.personaje_id
                        AND c1.año = %s
                        AND c2.año = %s
                    """, (año_siguiente, año_actual))

                    connection.commit()

                    await ctx.send(f"El año ha avanzado a {año_siguiente}.")
                else:
                    await ctx.send("No hay datos de año en la tabla de "
                                   "confianza.")
        else:
            await ctx.send("No tienes permiso para utilizar este comando.")
        connection.close()
        return

    argumentos = argumento.split()
    if argumentos[-1].startswith('-'):
        gasto_str = argumentos[-1]
        personaje = ' '.join(argumentos[:-1])
        columna = "gasto"
    elif argumentos[-1].startswith('+'):
        gasto_str = argumentos[-1]
        personaje = ' '.join(argumentos[:-2])
        columna = argumentos[-2]
        if columna not in ["anuales", "resumenes", "otros"]:
            await ctx.send(f"Columna no válida: {columna}.")
            connection.close()
            return
    else:
        gasto_str = '0'
        personaje = ' '.join(argumentos)
        columna = None

    # Gastar confianza
    if gasto_str.startswith("-"):
        try:
            gasto = int(gasto_str[1:])
        except ValueError:
            await ctx.send(
                f"Valor de gasto no válido: {gasto_str[1:]}."
            )
            connection.close()
            return

        # Verifica que el gasto no sea mayor a 1
        if gasto > 1:
            await ctx.send(
                "Si no eres Ancaelius, no puedes gastar su confianza de "
                "golpe. Si eres Ancaelius, ejecuta este comando tantas veces "
                "como quieras (bueno hasta tres, todos tenemos límites)."
            )
            connection.close()
            return

        # Realiza la consulta SQL para obtener confianza actual
        cursor.execute(
            """
            SELECT totales FROM Confianza
            WHERE personaje_id = (SELECT id FROM Personajes WHERE nombre = %s)
            ORDER BY año DESC
            LIMIT 1
        """,
            (personaje,),
        )

        # Muestra la consulta
        result = cursor.fetchone()

        # Verifica si no hay confianza o si la confianza es insuficiente
        if result is None or result[0] <= 0:
            await ctx.send(
                f"{personaje}, has perdido la confianza de Ancaelius..."
            )
            connection.close()
            return
        # Actualiza la BBDD
        cursor.execute(
            """
            WITH selected_personaje AS (
               SELECT id FROM Personajes WHERE nombre = %s
            ),
            max_year AS (
                SELECT MAX(año) AS año FROM Confianza WHERE personaje_id =
                (SELECT id FROM selected_personaje)
            )
            UPDATE Confianza
            SET gasto = COALESCE(gasto, 0) + %s,
            totales = COALESCE(totales, 0) - %s
            WHERE año = (SELECT año FROM max_year)
            AND personaje_id = (SELECT id FROM selected_personaje)
        """,
            (personaje, gasto, gasto),
        )

        connection.commit()

        await ctx.send(
            f"{personaje}, has gastado {gasto} punto de la confianza de "
            f"Ancaelius. Úsalo bien."
        )

    elif gasto_str.startswith("+"):
        try:
            gasto = int(gasto_str[1:])
        except ValueError:
            await ctx.send(f"Valor de gasto no válido: {gasto_str[1:]}.")
            return

        # Actualiza la BBDD
        query = """
            WITH selected_personaje AS (
               SELECT id FROM Personajes WHERE nombre = %s
            ),
            max_year AS (
                SELECT MAX(año) AS año FROM Confianza WHERE personaje_id =
                (SELECT id FROM selected_personaje)
            )
            UPDATE Confianza
            SET {column} = COALESCE({column}, 0) + %s, totales =
            COALESCE(totales, 0) + %s
            WHERE año = (SELECT año FROM max_year)
            AND personaje_id = (SELECT id FROM selected_personaje)
        """.format(column=columna)

        cursor.execute(query, (personaje, gasto, gasto))

        connection.commit()

        await ctx.send(f"Se añadieron {gasto} punto(s) de confianza al "
                       f"personaje {personaje}.")

    else:
        # Realiza la consulta SQL
        cursor.execute(
            """
            SELECT totales FROM Confianza
            WHERE personaje_id = (SELECT id FROM Personajes WHERE nombre = %s)
            ORDER BY año DESC
            LIMIT 1
        """,
            (personaje,),
        )

        # Muestra la consulta
        result = cursor.fetchone()

        if result is None:
            await ctx.send(
                f"No se encontró confianza para el personaje {personaje}."
            )
        else:
            await ctx.send(
                f"La confianza total para {personaje} en el último año "
                f"es {result[0]}."
            )

    # Cierra conexión
    connection.close()


bot.run(TOKEN)
