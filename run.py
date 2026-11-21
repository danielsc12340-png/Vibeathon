"""Inicia la plataforma EIRA.

    python run.py                 # solo este equipo (http://localhost:8000)
    python run.py --red           # accesible desde otros equipos de la red local
    python run.py --demo          # carga datos sintéticos si la base está vacía
"""
import argparse
import os
import socket
import sys
import threading
import webbrowser

from eira import create_app


def _port_free(host, port, family=socket.AF_INET):
    try:
        with socket.socket(family, socket.SOCK_STREAM) as s:
            if os.name != "nt":  # como waitress: ignora conexiones en TIME_WAIT de un arranque anterior
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
        return True
    except OSError:
        return False


def _ipv6_loopback():
    return socket.has_ipv6 and _port_free("::1", 0, socket.AF_INET6)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Plataforma EIRA (local-first)")
    parser.add_argument("--red", action="store_true", help="Escuchar en la red local (0.0.0.0)")
    parser.add_argument("--puerto", type=int, default=8000)
    parser.add_argument("--demo", action="store_true", help="Cargar datos de demostración si la base está vacía")
    parser.add_argument("--sin-navegador", action="store_true", help="No abrir el navegador al iniciar")
    parser.add_argument("--central", action="store_true", help="Modo base general en línea (recibe lo que suben las laptops)")
    args = parser.parse_args()
    if args.central:
        os.environ["EIRA_MODO"] = "central"

    app = create_app()
    with app.app_context():
        from eira.db import get_db
        from eira.demo import seed
        if not get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            if args.demo:
                seed()
                print("Cargando los datos sintéticos de campañas rurales (puede tardar 1 o 2 minutos)...")
                from eira.demo import cargar_sinteticos
                cargar_sinteticos(app)
            elif args.central:
                print("Base general sin cuentas. Crea la cuenta de Administración con:\n"
                      "  flask --app eira create-admin")
            else:
                from eira.demo import seed_accounts
                seed_accounts()

    host = "0.0.0.0" if args.red else "127.0.0.1"
    port = args.puerto
    while port <= 65535 and not _port_free(host, port):
        print(f"El puerto {port} está ocupado; probando {port + 1}...")
        port += 1
    if port > 65535:
        raise SystemExit("Error: no se encontró ningún puerto libre disponible.")
    listen = [f"{host}:{port}"]
    if not args.red and _ipv6_loopback() and _port_free("::1", port, socket.AF_INET6):
        listen.append(f"[::1]:{port}")
    url = f"http://localhost:{port}"
    print(f"EIRA disponible en {url}  (también http://127.0.0.1:{port})")
    if args.red:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 1))
            print(f"En la red local: http://{s.getsockname()[0]}:{port}")
            s.close()
        except OSError:
            pass
    print("Para detener: Ctrl+C")
    if not args.sin_navegador:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    try:
        from waitress import serve
        serve(app, listen=" ".join(listen), threads=8)
    except ImportError:
        app.run(host=host, port=port)


if __name__ == "__main__":
    main()
