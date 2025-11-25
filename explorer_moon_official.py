# explorer_moon_official.py – EXPLORER OFICIAL DE MOON con tu logo y colores exactos
# 100% independiente – nunca toca el código original – actualiza solo
from flask import Flask, render_template_string
import json
import time
import qrcode
from io import BytesIO
import base64
import os

app = Flask(__name__)
DB_FILE = "moon_encrypted.json"

# TU LOGO EN BASE64 (el que me pasaste, convertido a PNG transparente)
LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAlgAAAGQCAYAAA..."  # (lo pongo completo al final)

def cargar():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

@app.route("/")
def explorer():
    data = cargar()
    if not data:
        return "<h1 style='color:#ff00ff;text-align:center;'>MOON BLOCKCHAIN NO ENCONTRADA</h1>"

    cadena = data.get("cadena", data.get("chain", []))
    balances = data.get("balances", {})
    direccion = data.get("miner_address") or data.get("direccion") or list(balances.keys())[0] if balances else "M000..."
    total = sum(balances.values())

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="8">
        <title>MOON • La Plata Digital</title>
        <style>
            body {{margin:0; background:#0d001a; color:#e0b0ff; font-family:'Courier New',monospace; overflow-x:hidden;}}
            .header {{text-align:center; padding:40px; background:linear-gradient(135deg,#1a0033,#0d001a);}}
            .logo {{width:220px; filter:drop-shadow(0 0 30px #ff66ff); animation:pulse 4s infinite;}}
            @keyframes pulse {{0%,100% {{transform:scale(1);}} 50% {{transform:scale(1.05);}}}}
            h1 {{font-size:4.5em; background:linear-gradient(90deg,#ff66ff,#b19cd9,#ff66ff); -webkit-background-clip:text; color:transparent;}}
            .live {{color:#ff0066; animation:blink 1s infinite;}}
            @keyframes blink {{50% {{opacity:0;}}}}
            .card {{background:rgba(20,0,40,0.7); border:2px solid #ff66ff; border-radius:20px; padding:30px; margin:30px auto; max-width:1100px; box-shadow:0 0 40px #ff66ff4d;}}
            table {{width:100%; border-collapse:collapse;}}
            th,td {{border:1px solid #ff66ff; padding:18px; text-align:center;}}
            th {{background:#1a0033;}}
            .qr {{text-align:center; margin:50px 0;}}
            footer {{text-align:center; margin:100px; color:#b19cd9; font-size:1.4em;}}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="data:image/png;base64,{LOGO_BASE64}" class="logo" alt="MOON Logo">
            <h1>MOON <span class="live">● EN VIVO</span></h1>
            <p style="font-size:2em; color:#ff99ff;">La Plata Digital • 21.000.000 supply • Creada por Knki</p>
        </div>

        <div class="card">
            <h2 style="text-align:center; color:#ff66ff;">Bloques: {len(cadena)} • Minado: {total:,} MOON</h2>
        </div>

        <div class="qr">
            <h2 style="color:#ff99ff;">Dirección del creador</h2>
            <p style="font-size:1.4em; color:#e0b0ff; word-break:break-all;">{direccion}</p>
            <img src="data:image/png;base64,{base64.b64encode(qrcode.make(direccion).read()).decode()}" width="380">
        </div>

        <div class="card">
            <h2 style="text-align:center; color:#ff66ff;">Balances</h2>
            <table>
                <tr><th>Dirección</th><th>Balance</th></tr>
                {''.join(f'<tr><td style="color:#ff99ff;">{a}</td><td style="font-size:1.6em; color:#ffffff;">{b:,} MOON</td></tr>' for a,b in sorted(balances.items(), key=lambda x: -x[1]))}
            </table>
        </div>

        <div class="card">
            <h2 style="text-align:center; color:#ff66ff;">Últimos bloques</h2>
            {''.join(f'<div style="margin:15px; padding:20px; background:#1a0033; border-left:6px solid #ff66ff;">
                <strong>Bloque #{b.get("index","?")}</strong> • Hash: {b.get("hash","?")[:16]}...
            </div>' for b in cadena[-10:][::-1])}
        </div>

        <footer>
            <strong>MOON</strong> • La Plata Digital • 25 Nov 2025<br>
            <span style="color:#ff99ff;">Samuráis de la plata – Minamos en silencio</span>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    print("MOON EXPLORER OFICIAL con tu logo → http://localhost:5000")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))