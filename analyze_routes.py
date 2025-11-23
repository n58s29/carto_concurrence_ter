#!/usr/bin/env python3
"""
Script pour analyser les trajets et identifier les doublons
(trajets qui ont à la fois une ligne droite et un vrai itinéraire)
"""

import json
from collections import defaultdict

def analyze_routes(geojson_file):
    """Analyse les trajets dans le fichier GeoJSON"""

    print(f"Lecture de {geojson_file}...")
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Grouper les features par relation
    routes_by_relation = defaultdict(list)

    for i, feature in enumerate(data['features']):
        relation = feature['properties'].get('relation', 'N/A')
        coords = feature['geometry']['coordinates']
        num_coords = len(coords)

        routes_by_relation[relation].append({
            'index': i,
            'num_coords': num_coords,
            'is_straight_line': num_coords == 2,
            'feature': feature
        })

    print(f"\nNombre total de features: {len(data['features'])}")
    print(f"Nombre de relations uniques: {len(routes_by_relation)}")

    # Identifier les relations qui ont plusieurs features
    duplicates = []
    mixed_routes = []

    for relation, routes in routes_by_relation.items():
        if len(routes) > 1:
            duplicates.append({
                'relation': relation,
                'routes': routes,
                'count': len(routes)
            })

            # Vérifier si certaines sont des lignes droites et d'autres des vrais itinéraires
            has_straight = any(r['is_straight_line'] for r in routes)
            has_detailed = any(not r['is_straight_line'] for r in routes)

            if has_straight and has_detailed:
                mixed_routes.append({
                    'relation': relation,
                    'routes': routes
                })

    # Afficher les résultats
    print(f"\n{'='*80}")
    print(f"RELATIONS AVEC PLUSIEURS FEATURES: {len(duplicates)}")
    print(f"{'='*80}")

    for dup in sorted(duplicates, key=lambda x: x['count'], reverse=True):
        print(f"\n{dup['relation']}: {dup['count']} features")
        for route in dup['routes']:
            route_type = "LIGNE DROITE" if route['is_straight_line'] else "ITINÉRAIRE DÉTAILLÉ"
            print(f"  - Index {route['index']}: {route['num_coords']} coordonnées ({route_type})")

    print(f"\n{'='*80}")
    print(f"RELATIONS AVEC LIGNE DROITE ET ITINÉRAIRE DÉTAILLÉ: {len(mixed_routes)}")
    print(f"{'='*80}")

    if mixed_routes:
        print("\n⚠️  CES RELATIONS ONT DES DOUBLONS À CORRIGER:")
        for item in sorted(mixed_routes, key=lambda x: x['relation']):
            print(f"\n❌ {item['relation']}")
            for route in item['routes']:
                route_type = "LIGNE DROITE" if route['is_straight_line'] else "ITINÉRAIRE DÉTAILLÉ"
                operateur = route['feature']['properties'].get('operateur', 'N/A')
                statut = route['feature']['properties'].get('statut', 'N/A')
                print(f"  - Index {route['index']}: {route['num_coords']} coords ({route_type}) - {operateur} - {statut}")

    return {
        'duplicates': duplicates,
        'mixed_routes': mixed_routes,
        'routes_by_relation': routes_by_relation
    }

if __name__ == '__main__':
    result = analyze_routes('etat_lignes_carte.geojson')

    print(f"\n{'='*80}")
    print(f"RÉSUMÉ")
    print(f"{'='*80}")
    print(f"Total de relations avec doublons: {len(result['duplicates'])}")
    print(f"Relations à corriger (ligne droite + itinéraire): {len(result['mixed_routes'])}")
