#!/usr/bin/env python3
"""
Script pour corriger les coordonnées mal imbriquées dans le fichier GeoJSON.
"""

import json
import sys

def flatten_coordinates(coords):
    """
    Aplatit les coordonnées mal imbriquées.

    Une coordonnée correcte est [lon, lat] où lon et lat sont des nombres.
    Une coordonnée incorrecte est [[lon, lat], [lon, lat], ...].
    """
    flattened = []

    for coord in coords:
        if not isinstance(coord, list):
            print(f"Erreur: coordonnée n'est pas une liste: {coord}")
            continue

        # Vérifier si c'est une paire [lon, lat] correcte
        if len(coord) == 2 and isinstance(coord[0], (int, float)) and isinstance(coord[1], (int, float)):
            # Coordonnée correcte
            flattened.append(coord)
        else:
            # Coordonnée incorrecte - probablement une liste de paires
            # On aplatit récursivement
            print(f"Aplatissement de coordonnée incorrecte avec {len(coord)} éléments")
            for sub_coord in coord:
                if isinstance(sub_coord, list) and len(sub_coord) == 2:
                    if isinstance(sub_coord[0], (int, float)) and isinstance(sub_coord[1], (int, float)):
                        flattened.append(sub_coord)

    return flattened

def fix_geojson(input_file, output_file):
    """Corrige le fichier GeoJSON en aplatissant les coordonnées incorrectes."""
    print(f"Lecture de {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Traitement de {len(data['features'])} features...")

    fixed_count = 0
    for i, feature in enumerate(data['features']):
        geometry = feature['geometry']

        if geometry['type'] == 'LineString':
            original_coords = geometry['coordinates']
            fixed_coords = flatten_coordinates(original_coords)

            if len(fixed_coords) != len(original_coords):
                print(f"\nFeature {i} ({feature['properties'].get('relation', 'N/A')}): "
                      f"{len(original_coords)} -> {len(fixed_coords)} coordonnées")
                fixed_count += 1

            geometry['coordinates'] = fixed_coords

    print(f"\n{fixed_count} features corrigées")

    print(f"\nÉcriture de {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Terminé!")

if __name__ == '__main__':
    input_file = 'etat_lignes_carte.geojson'
    output_file = 'etat_lignes_carte.geojson'

    fix_geojson(input_file, output_file)
