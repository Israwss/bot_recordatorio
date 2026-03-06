import requests
import schedule
import time
from datetime import datetime

import os
ID_INSTANCE = os.environ["ID_INSTANCE"]
API_TOKEN   = os.environ["API_TOKEN"]
GROUP_ID    = os.environ["GROUP_ID"]

NOMBRES = {
    0: "Ash",
    1: "Isra",
    3: "Joshi"
}

def enviar_recordatorio():
    dia_semana = datetime.now().weekday()
    if dia_semana not in NOMBRES:
        print("Hoy no toca, saliendo.")
        return

    nombre = NOMBRES[dia_semana]
    
    MENSAJE = f"""*Recordatorio*

Hola equipo 
Recuerden que hoy es el turno de *{nombre}*

¡Buenas tardes!"""

    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    response = requests.post(url, json={"chatId": GROUP_ID, "message": MENSAJE})
    print("✅ Enviado!" if response.status_code == 200 else f"❌ Error: {response.text}")

schedule.every().monday.at("23:55").do(enviar_recordatorio)
schedule.every().tuesday.at("23:55").do(enviar_recordatorio)
schedule.every().thursday.at("23:55").do(enviar_recordatorio)

print("🤖 Bot activo...")
while True:
    schedule.run_pending()
    time.sleep(60)