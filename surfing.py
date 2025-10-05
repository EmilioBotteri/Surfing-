
import requests
from datetime import datetime, timedelta

# ------------------------
# CONFIGURACIÓN
# ------------------------
UMBRAL = 0.8  # metros, altura mínima para avisar

# Coordenadas de los spots
spots = {
    "Masnou": (41.483, 2.317),
    "Vilassar": (41.490, 2.430)
}

# Tu bot de Telegram
TELEGRAM_TOKEN = "8204580135:AAGJYiVHCNMCASuKzchqKl5IvGwx6kNXl7Q"
CHAT_ID = 6809954781

# ------------------------
# FUNCIONES
# ------------------------

def enviar_telegram(mensaje):
    """
    Envía un mensaje de Telegram usando tu bot.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Error al enviar Telegram:", e)

def consultar_ola(lat, lon):
    """
    Consulta la API de Open-Meteo y devuelve los arrays horarios de altura, dirección y periodo.
    """
    url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height,wave_direction,wave_period&timezone=Europe/Madrid"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["hourly"]

# ------------------------
# LÓGICA PRINCIPAL
# ------------------------

# Fecha objetivo: 4 días adelante
hoy = datetime.now()
fecha_objetivo = (hoy + timedelta(days=4)).date()

for spot, (lat, lon) in spots.items():
    datos = consultar_ola(lat, lon)
    
    # Recorremos cada hora
    for i, t in enumerate(datos["time"]):
        hora = datetime.fromisoformat(t)
        if hora.date() == fecha_objetivo:
            altura = datos["wave_height"][i]
            direccion = datos["wave_direction"][i]
            periodo = datos["wave_period"][i]
            
            if altura >= UMBRAL:
                mensaje = (f"Ola en {spot} {hora.strftime('%Y-%m-%d %H:%M')}:\n"
                           f"Altura: {altura} m\n"
                           f"Dirección: {direccion}°\n"
                           f"Periodo: {periodo} s")
                enviar_telegram(mensaje)

