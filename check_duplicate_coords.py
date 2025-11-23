#!/usr/bin/env python3
"""
Script pour identifier les trajets qui partagent les mêmes coordonnées
"""

import json
from collections import defaultdict

def check_duplicate_coords(geojson_file):
    """Identifie les trajets avec des coordonnées dupliquées ou suspectes"""

    print(f"Lecture de {geojson_file}...")
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Grouper par nombre de coordonnées
    coords_count_groups = defaultdict(list)

    # Grouper par coordonnées identiques (hash du premier et dernier point)
    coords_hash_groups = defaultdict(list)

    for i, feature in enumerate(data['features']):
        relation = feature['properties'].get('relation', 'N/A')
        coords = feature['geometry']['coordinates']
        num_coords = len(coords)

        coords_count_groups[num_coords].append({
            'index': i,
            'relation': relation,
            'coords': coords,
            'operateur': feature['properties'].get('operateur', 'N/A')
        })

        # Hash basé sur premier et dernier point
        first_point = tuple(coords[0])
        last_point = tuple(coords[-1])
        coord_hash = (first_point, last_point, num_coords)

        coords_hash_groups[coord_hash].append({
            'index': i,
            'relation': relation
        })

    # Afficher les groupes suspects
    print(f"\n{'='*80}")
    print(f"TRAJETS GROUPÉS PAR NOMBRE DE COORDONNÉES")
    print(f"{'='*80}")

    for num_coords in sorted(coords_count_groups.keys()):
        routes = coords_count_groups[num_coords]
        if len(routes) > 1 or num_coords < 20:
            print(f"\n{num_coords} coordonnées: {len(routes)} trajets")
            for route in routes:
                print(f"  - Index {route['index']:3d}: {route['relation']}")

    print(f"\n{'='*80}")
    print(f"TRAJETS SUSPECTS (< 20 coordonnées)")
    print(f"{'='*80}")

    suspicious = []
    for num_coords, routes in coords_count_groups.items():
        if num_coords < 20:
            for route in routes:
                suspicious.append(route)

    for route in sorted(suspicious, key=lambda x: x['index']):
        print(f"\nIndex {route['index']:3d}: {route['relation']}")
        print(f"  Opérateur: {route['operateur']}")
        print(f"  Nombre de coordonnées: {len(route['coords'])}")
        print(f"  Premier point: {route['coords'][0]}")
        print(f"  Dernier point: {route['coords'][-1]}")

        # Vérifier si c'est une ligne droite ou quasi-droite
        if len(route['coords']) <= 10:
            print(f"  Toutes les coordonnées:")
            for j, coord in enumerate(route['coords']):
                print(f"    {j}: {coord}")

    # Vérifier les doublons exacts de coordonnées
    print(f"\n{'='*80}")
    print(f"GROUPES DE TRAJETS AVEC MÊMES POINTS DE DÉPART/ARRIVÉE")
    print(f"{'='*80}")

    for coord_hash, routes in coords_hash_groups.items():
        if len(routes) > 1:
            first, last, num = coord_hash
            print(f"\n{len(routes)} trajets partageant {num} coords: {first} -> {last}")
            for route in routes:
                print(f"  - Index {route['index']:3d}: {route['relation']}")

if __name__ == '__main__':
    check_duplicate_coords('etat_lignes_carte.geojson')
