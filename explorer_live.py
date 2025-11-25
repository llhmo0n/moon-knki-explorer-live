# explorer_live.py – MOON EXPLORER EN VIVO by Knki
from flask import Flask, render_template_string
import json
import time
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
ARCHIVO = "moon_encrypted.json"

def cargar():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

@app.route("/")
def explorer():
    data = cargar()
    if not data:
        return "<h1 style='color:red'>MOON BLINDADA no está encendida o archivo no encontrado</h1>"

    cadena = data["cadena"]
    balances = data["balances"]
    direccion = data["direccion"]

    # QR
    qr = qrcode.QRCode()
    qr.add_data(direccion)
    img = qrcode.make(qr)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_img = base64.b64encode(buffered.getvalue()).decode()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MOON EXPLORER • Knki</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{font-family: 'Courier New'; background:#000; color:#0f0; padding:20px;}}
            h1 {{text-align:center; color:#0ff; font-size:3em;}}
            .live {{color:#f00; animation:blink 1s infinite;}}
            @keyframes blink {{50% {{opacity:0.3;}}}}
            table, .block {{border:2px solid #0f0; margin:20px 0; padding:15px; background:#111;}}
            .addr {{color:#f0f;}}
        </style>
    </head>
    <body>
        <h1>MOON EXPLORER <span class="live">● EN VIVO</span></h1>
        <h2>Bloques: {len(cadena)} • Último: {time.strftime("%H:%M:%S", time.localtime(cadena[-1]["timestamp"]))}</h2>

        <div style="text-align:center;">
            <h3>Dirección oficial Knki</h3>
            <p class="addr"><b>{direccion}</b></p>
            <img src="data:image/png;base64,{qr_img}" width="280">
        </div>

        <h2>Balances</h2>
        <table width="100%">
            <tr><th>Dirección</th><th>Balance</th></tr>
            {''.join(f'<tr><td class="addr">{a}</td><td>{b:,} MOON</td></tr>' for a,b in sorted(balances.items(), key=lambda x: -x[1]))}
        </table>

        <h2>Últimos 10 bloques</h2>
        {''.join(f'<div class="block">Bloque #{b["indice"]} • Hash: {b["hash"][:16]}... • {len(b["transacciones"])} tx</div>' for b in cadena[-10:][::-1])}

        <footer style="text-align:center; margin-top:80px; color:#0f0;">
            MOON • Creada 100% por <strong>Knki</strong><br>
            Blockchain blindada • Explorer en tiempo real
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    print("EXPLORER EN VIVO DE MOON BLINDADA")
    print("http://localhost:5000  →  Se actualiza cada 5 segundos")
    app.run(host="0.0.0.0", port=5000)