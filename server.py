#!/usr/bin/env python3
"""
Serveur HTTP simple pour servir la carte de concurrence ferroviaire.

Usage:
    python3 server.py [port]

Par défaut, le serveur démarre sur le port 8000.
Ouvrez ensuite http://localhost:8000 dans votre navigateur.
"""

import http.server
import socketserver
import sys
import os

def main():
    # Port par défaut
    PORT = 8000

    # Utiliser le port fourni en argument si disponible
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print(f"Erreur: '{sys.argv[1]}' n'est pas un numéro de port valide.")
            sys.exit(1)

    # Changer le répertoire de travail au dossier du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Créer le serveur
    Handler = http.server.SimpleHTTPRequestHandler

    # Activer la réutilisation de l'adresse pour éviter les erreurs "Address already in use"
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("=" * 60)
            print("🚆 Serveur de la carte de concurrence ferroviaire")
            print("=" * 60)
            print(f"\n✓ Serveur démarré sur le port {PORT}")
            print(f"\n🌐 Ouvrez votre navigateur à l'adresse:")
            print(f"   http://localhost:{PORT}")
            print(f"\n📁 Répertoire servi: {os.getcwd()}")
            print(f"\n💡 Appuyez sur Ctrl+C pour arrêter le serveur\n")
            print("=" * 60)

            # Démarrer le serveur
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✓ Serveur arrêté proprement.")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98 or e.errno == 48:  # Address already in use
            print(f"\n❌ Erreur: Le port {PORT} est déjà utilisé.")
            print(f"   Essayez un autre port: python3 server.py {PORT + 1}")
        else:
            print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
