import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = "ChinookDatabase/DataSources/Chinook_Sqlite_AutoIncrementPKs.sqlite"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("""
            SELECT t.TrackId, ar.Name, al.Title, t.Name, t.UnitPrice
            FROM Track t
            JOIN Album al ON t.AlbumId = al.AlbumId
            JOIN Artist ar ON al.ArtistId = ar.ArtistId
            ORDER BY t.TrackId DESC
            LIMIT 15
        """).fetchall()
        conn.close()

        filas_html = "".join(
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>${r[4]}</td></tr>"
            for r in rows
        )
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Chinook DB - Local</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; background: #f4f4f9; }}
        table {{ border-collapse: collapse; width: 100%; background: #fff; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #1e293b; color: #fff; }}
    </style>
</head>
<body>
    <h2>Chinook Database corriendo en local</h2>
    <p>Últimos 15 registros insertados en la base de datos:</p>
    <table>
        <tr><th>ID</th><th>Artista</th><th>Álbum</th><th>Canción</th><th>Precio</th></tr>
        {filas_html}
    </table>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

print("Servidor activo en http://127.0.0.1:5500 (Presiona Ctrl + C para detenerlo)")
HTTPServer(("127.0.0.1", 5500), Handler).serve_forever()
