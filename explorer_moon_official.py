# explorer_moon_official.py – MOON EXPLORER OFICIAL con tu logo y colores
from flask import Flask, render_template_string
import json
import time
import qrcode
from io import BytesIO
import base64
import os

app = Flask(__name__)
DB_FILE = "moon_encrypted.json"

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

    # QR con tu estilo
    qr = qrcode.QRCode(border=6, box_size=10)
    qr.add_data(direccion)
    qr.make(fit=True)
    img = qrcode.make(qr)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_img = base64.b64encode(buffered.getvalue()).decode()

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="8">
        <title>MOON • La Plata Digital</title>
        <style>
            body {{margin:0; background:#0d001a; color:#e0b0ff; font-family:'Courier New',monospace;}}
            .header {{text-align:center; padding:50px; background:linear-gradient(135deg,#1a0033,#0d001a);}}
            h1 {{font-size:5em; background:linear-gradient(90deg,#ff66ff,#b19cd9,#ff66ff); -webkit-background-clip:text; color:transparent;}}
            .live {{color:#ff0066; animation:blink 1s infinite;}}
            @keyframes blink {{50% {{opacity:0;}}}}
            .card {{background:rgba(30,0,60,0.8); border:3px solid #ff66ff; border-radius:25px; padding:35px; margin:40px auto; max-width:1100px; box-shadow:0 0 50px #ff66ff40;}}
            table {{width:100%; border-collapse:collapse; margin:30px 0;}}
            th,td {{border:2px solid #ff66ff; padding:20px; text-align:center;}}
            th {{background:#1a0033;}}
            .block-item {{margin:15px 0; padding:25px; background:#1a0033; border-left:8px solid #ff66ff; border-radius:15px;}}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>MOON <span class="live">● EN VIVO</span></h1>
            <p style="font-size:2.2em; color:#ff99ff;">La Plata Digital • 21.000.000 supply • Creada por Knki</p>
        </div>

        <div class="card">
            <h2 style="text-align:center; color:#ff66ff; font-size:2em;">Bloques: {len(cadena)} • Minado: {total:,} MOON</h2>
        </div>

        <div style="text-align:center; margin:60px;">
            <h2 style="color:#ff99ff; font-size:2.5em;">Dirección del creador</h2>
            <p style="font-size:1.5em; color:#e0b0ff; word-break:break-all;">{direccion}</p>
            <img src="data:image/png;base64,{qr_img}" width="400">
        </div>

        <div class="card">
            <h2 style="text-align:center; color:#ff66ff; font-size:2em;">Balances</h2>
            <table>
                <tr><th>Dirección</th><th>Balance</th></tr>
                {''.join(f'<tr><td style="color:#ff99ff;">{a}</td><td style="font-size:1.8em; color:#ffffff;">{b:,} MOON</td></tr>' for a,b in sorted(balances.items(), key=lambda x: -x[1]))}
            </table>
        </div>

        <div class="card">
            <h2 style="text-align:center; color:#ff66ff; font-size:2em;">Últimos bloques</h2>
            {''.join(f'<div class="block-item"><strong>Bloque #{b.get("index","?")}</strong> • Hash: {b.get("hash","?")[:16]}...</div>' for b in cadena[-10:][::-1])}
        </div>

        <footer style="text-align:center; margin:120px; color:#ff99ff; font-size:1.6em;">
            <strong>MOON</strong> • La Plata Digital • 25 Nov 2025<br>
            Samuráis de la plata – Minamos en silencio
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == "__main__":
    print("MOON EXPLORER OFICIAL ÉPICO → http://localhost:5000")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))