# EXPLORER_LIVE.PY – MOON EXPLORER MUNDIAL ETERNO by Knki
# Funciona con cualquier versión de tu blockchain para siempre
from flask import Flask, render_template_string
import json
import time
import qrcode
from io import BytesIO
import base64
import os

app = Flask(__name__)
DB_FILE = "moon_encrypted.json"  # tu archivo actual
FALLBACK_FILE = "moon_plata_digital.json"  # por si usas el otro

def cargar_datos():
    # Intenta cargar el archivo principal
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f), DB_FILE
        except:
            pass
    
    # Intenta el archivo alternativo
    if os.path.exists(FALLBACK_FILE):
        try:
            with open(FALLBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f), FALLBACK_FILE
        except:
            pass
    
    return None, None

def obtener_direccion(data):
    # Funciona con cualquier nombre de clave que hayas usado
    claves_posibles = ["direccion", "miner_address", "creator_address", "address", "wallet"]
    for clave in claves_posibles:
        if clave in data:
            return data[clave]
    # Si no hay ninguna, toma la primera dirección del balance
    if "balances" in data and data["balances"]:
        return list(data["balances"].keys())[0]
    return "M000000000000000000000000000000000"

@app.route("/")
def explorer():
    data, archivo_usado = cargar_datos()
    if not data:
        return "<h1 style='color:#f00;text-align:center;'>MOON BLOCKCHAIN NO ENCONTRADA<br>Archivos buscados: moon_encrypted.json o moon_plata_digital.json</h1>"

    cadena = data.get("cadena", data.get("chain", []))
    balances = data.get("balances", {})
    direccion = obtener_direccion(data)

    # QR de la dirección principal
    qr = qrcode.QRCode()
    qr.add_data(direccion)
    img = qrcode.make(qr)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_img = base64.b64encode(buffered.getvalue()).decode()

    ultimo_bloque = cadena[-1] if cadena else {}
    ultimo_hash = ultimo_bloque.get("hash", "génesis")[:16] + "..." if ultimo_bloque else "génesis"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MOON EXPLORER • Knki</title>
        <meta http-equiv="refresh" content="8">
        <style>
            body {{font-family: 'Courier New', monospace; background:#000; color:#0f0; padding:20px;}}
            h1 {{text-align:center; color:#0ff; font-size:3.5em;}}
            h2 {{text-align:center; color:#0f8;}}
            .live {{color:#f00; animation:blink 1s infinite;}}
            @keyframes blink {{50% {{opacity:0.3;}}}}
            table, .block {{border:2px solid #0f0; margin:20px 0; padding:15px; background:#111; border-radius:10px;}}
            .addr {{color:#f0f; font-weight:bold;}}
            footer {{text-align:center; margin-top:100px; color:#0f0; font-size:1.3em;}}
        </style>
    </head>
    <body>
        <h1>MOON EXPLORER <span class="live">● EN VIVO</span></h1>
        <h2>Bloques: {len(cadena)} • Último hash: {ultimo_hash}</h2>

        <div style="text-align:center;">
            <h3>Dirección del creador (Knki)</h3>
            <p class="addr"><b>{direccion}</b></p>
            <img src="data:image/png;base64,{qr_img}" width="300">
        </div>

        <h2>Balances actuales</h2>
        <table width="100%">
            <tr><th>Dirección</th><th>Balance</th></tr>
            {''.join(f'<tr><td class="addr">{a}</td><td>{b:,} MOON</td></tr>' for a,b in sorted(balances.items(), key=lambda x: -x[1]))}
        </table>

        <h2>Últimos 10 bloques</h2>
        {''.join(f'<div class="block">Bloque #{b.get("index", "?")} • Hash: {b.get("hash","?")[:16]}... • Tx: {len(b.get("transacciones", b.get("transactions", [])))}</div>' for b in cadena[-10:][::-1])}

        <footer>
            <strong>MOON</strong> • Creada 100% por <strong>Knki</strong><br>
            La Plata Digital – Fair Launch 2025<br>
            <span style="color:#0ff;">EXPLORER INMORTAL – Funciona para siempre</span>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    print("═" * 80)
    print("           MOON EXPLORER MUNDIAL ETERNO – by Knki")
    print("           https://moon-knki-explorer-live.onrender.com")
    print("           Se actualiza cada 8 segundos – Funciona con cualquier versión de tu blockchain")
    print("═" * 80)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))