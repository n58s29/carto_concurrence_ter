#!/usr/bin/env python3
"""
Script pour corriger manuellement les trajets restants qui ont des coordonnées fausses
"""

import json

# Coordonnées des villes
CITY_COORDS = {
    "Paris": [2.3522, 48.8566],
    "Maubeuge": [3.9731, 50.2778]
}

def fix_remaining_routes(geojson_file):
    """Corrige les trajets restants"""

    print(f"Lecture de {geojson_file}...")
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Index 29: Paris>Creil>Compiègne>Saint-Quentin>Maubeuge/Cambrai
    feature = data['features'][29]
    relation = feature['properties']['relation']
    old_coords = len(feature['geometry']['coordinates'])

    print(f"\nTrajet à corriger:")
    print(f"Index 29: {relation}")
    print(f"Anciennes coordonnées: {old_coords}")
    print(f"Premier point: {feature['geometry']['coordinates'][0]}")
    print(f"Dernier point: {feature['geometry']['coordinates'][-1]}")

    # Corriger avec une ligne droite Paris -> Maubeuge
    feature['geometry']['coordinates'] = [CITY_COORDS["Paris"], CITY_COORDS["Maubeuge"]]

    print(f"\nNouvelles coordonnées: 2")
    print(f"Premier point (Paris): {CITY_COORDS['Paris']}")
    print(f"Dernier point (Maubeuge): {CITY_COORDS['Maubeuge']}")

    print(f"\nÉcriture de {geojson_file}...")
    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✓ Corrigé!")

if __name__ == '__main__':
    fix_remaining_routes('etat_lignes_carte.geojson')
