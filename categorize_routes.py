#!/usr/bin/env python3
"""
Script pour catégoriser les trajets entre lignes droites et itinéraires détaillés
"""

import json

def categorize_routes(geojson_file):
    """Catégorise les trajets"""

    print(f"Lecture de {geojson_file}...")
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    straight_lines = []
    detailed_routes = []

    for i, feature in enumerate(data['features']):
        relation = feature['properties'].get('relation', 'N/A')
        coords = feature['geometry']['coordinates']
        num_coords = len(coords)
        operateur = feature['properties'].get('operateur', 'N/A')
        statut = feature['properties'].get('statut', 'N/A')

        route_info = {
            'index': i,
            'relation': relation,
            'num_coords': num_coords,
            'operateur': operateur,
            'statut': statut
        }

        if num_coords == 2:
            straight_lines.append(route_info)
        else:
            detailed_routes.append(route_info)

    print(f"\n{'='*80}")
    print(f"STATISTIQUES")
    print(f"{'='*80}")
    print(f"Total de trajets: {len(data['features'])}")
    print(f"Lignes droites (2 coordonnées): {len(straight_lines)}")
    print(f"Itinéraires détaillés (>2 coordonnées): {len(detailed_routes)}")

    print(f"\n{'='*80}")
    print(f"LIGNES DROITES ({len(straight_lines)} trajets)")
    print(f"{'='*80}")
    for route in straight_lines:
        print(f"Index {route['index']:3d}: {route['relation']:40s} - {route['operateur']:15s} - {route['statut']}")

    print(f"\n{'='*80}")
    print(f"ITINÉRAIRES DÉTAILLÉS ({len(detailed_routes)} trajets)")
    print(f"{'='*80}")
    for route in detailed_routes:
        print(f"Index {route['index']:3d}: {route['relation']:40s} ({route['num_coords']:4d} coords) - {route['operateur']:15s} - {route['statut']}")

if __name__ == '__main__':
    categorize_routes('etat_lignes_carte.geojson')
