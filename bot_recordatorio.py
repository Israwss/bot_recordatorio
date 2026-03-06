import requests
import schedule
import time
import pytz
from datetime import datetime
import os

# --- CONFIGURACIÓN ---
ID_INSTANCE = os.environ["ID_INSTANCE"]
API_TOKEN   = os.environ["API_TOKEN"]
GROUP_ID    = os.environ["GROUP_ID"]

NOMBRES = {
    0: "Ash",    # Lunes
    1: "Isra",   # Martes
    3: "Joshi"   # Jueves
}

# --- ENVÍO ---
def enviar_recordatorio():
    mexico = pytz.timezone("America/Mexico_City")
    ahora = datetime.now(mexico)

    # Verificar que sean exactamente las 5:55 PM
    if not (ahora.hour == 17 and ahora.minute == 55):
        return

    dia_semana = ahora.weekday()
    if dia_semana not in NOMBRES:
        return

    nombre = NOMBRES[dia_semana]

    MENSAJE = f"""*Recordatorio*

Hola equipo
Recuerden que hoy es el turno de *{nombre}* 

¡Buenas tardes!"""

    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    response = requests.post(url, json={"chatId": GROUP_ID, "message": MENSAJE})

    if response.status_code == 200:
        print(f"✅ Mensaje enviado a las {ahora.strftime('%H:%M')} hora México — Turno de {nombre}")
    else:
        print(f"❌ Error: {response.text}")

# --- SCHEDULER (revisa cada minuto) ---
schedule.every().monday.do(enviar_recordatorio)
schedule.every().tuesday.do(enviar_recordatorio)
schedule.every().thursday.do(enviar_recordatorio)

print("🤖 Bot activo — esperando lunes, martes o jueves a las 5:55 PM México...")

while True:
    schedule.run_pending()
    time.sleep(60)
