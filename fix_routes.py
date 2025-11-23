#!/usr/bin/env python3
"""
Script pour corriger les trajets en remplaçant les fausses routes
par des lignes droites entre les vraies villes
"""

import json
import re

# Dictionnaire des coordonnées GPS des villes françaises
# Format: [longitude, latitude]
CITY_COORDINATES = {
    # Région Bourgogne-Franche-Comté
    "Dijon": [5.0415, 47.3220],
    "Mâcon": [4.8357, 46.3062],
    "Cosne": [2.9271, 47.4130],
    "Moulins": [3.3334, 46.5664],
    "Chagny": [4.7554, 46.9090],
    "Nevers": [3.1592, 46.9903],
    "Montchanin": [4.4676, 46.7603],
    "Paray": [4.1171, 46.4522],
    "Lyon": [4.8357, 45.7640],

    # Région Grand Est
    "Épinal": [6.4499, 48.1735],
    "Saint-Die-des-vosges": [6.9500, 48.2833],
    "Strasbourg": [7.7521, 48.5734],
    "Sélestat": [7.4582, 48.2600],
    "Molsheim": [7.4926, 48.5400],
    "Metz": [6.1757, 49.1193],
    "Trier": [6.6371, 49.7596],
    "Saarbrücken": [6.9967, 49.2401],
    "Wissembourg": [7.9445, 49.0392],
    "Neustadt": [8.1400, 49.3500],
    "Lauterbourg": [8.1764, 48.9753],
    "Wörth": [8.2508, 49.0542],
    "Karlsruhe": [8.4037, 49.0069],
    "Offenburg": [7.9403, 48.4720],
    "Mulhouse": [7.3389, 47.7508],
    "Müllheim": [7.6288, 47.8086],
    "Reims": [4.0317, 49.2583],
    "Epernay": [3.9593, 49.0420],
    "ChâteauThierry": [3.4033, 49.0467],
    "Charleville-Mézières": [4.7197, 49.7631],
    "Charleville-mézières": [4.7197, 49.7631],
    "Givet": [4.8262, 50.1369],
    "Hirson": [4.0819, 49.9214],
    "Longuyon": [5.6086, 49.4467],
    "Longwy": [5.7614, 49.5195],
    "Thionville": [6.1686, 49.3581],
    "Châlons-en-Champagne": [4.3683, 48.9567],
    "Saint-Dizier": [4.9494, 48.6377],
    "Chaumont": [5.1391, 48.1131],
    "Culmont-Chalindrey": [5.3867, 47.8333],
    "Fismes": [3.6781, 49.3086],
    "Laon": [3.6250, 49.5639],

    # Région Hauts-de-France
    "Amiens": [2.2957, 49.8941],
    "Tergnier": [3.2978, 49.6556],
    "Saint-Quentin": [3.2876, 49.8484],
    "Albert": [2.6512, 50.0026],
    "Lille": [3.0573, 50.6292],
    "Abbeville": [1.8342, 50.1058],
    "Beauvais": [2.0810, 49.4294],
    "Abancourt": [1.7694, 49.6925],
    "LeTréport": [1.3769, 50.0608],
    "Creil": [2.4753, 49.2589],
    "Montdidier": [2.5710, 49.6475],
    "Compiègne": [2.8258, 49.4177],
    "Rouen": [1.0993, 49.4432],
    "Paris": [2.3522, 48.8566],
    "Calais": [1.8587, 50.9513],
    "Maubeuge": [3.9731, 50.2778],
    "Cambrai": [3.2358, 50.1761],
    "Roissy": [2.5479, 49.0097],
    "Saint-pol-sur-ternoise": [2.3367, 50.3833],
    "Arras": [2.7772, 50.2920],
    "Béthune": [2.6394, 50.5300],
    "Etaples": [1.6367, 50.5167],

    # Région Pays de la Loire
    "Nantes": [-1.5536, 47.2184],
    "Nort-sur-Erdre": [-1.4986, 47.4381],
    "Chateaubriand": [-1.3764, 47.7167],
    "Clisson": [-1.2811, 47.0867],
    "Pornic": [-2.1025, 47.1158],
    "Saint-Gilles-Croix-de-vie": [-1.9392, 46.6964],
    "LaRoche-sur-yon": [-1.4261, 46.6703],
    "LesSablesd'olonne": [-1.7833, 46.4967],
    "LaRochelle": [-1.1508, 46.1603],
    "Cholet": [-0.8792, 47.0608],
    "Angers": [-0.5633, 47.4784],

    # Région PACA
    "Marseille": [5.3698, 43.2965],
    "Toulon": [5.9280, 43.1242],
    "Nice": [7.2619, 43.7102],
    "LesArcsDraguignan": [6.4700, 43.4633],
    "Vintimille": [7.5086, 43.7856],
    "Cannes": [7.0169, 43.5528],
    "Grasse": [6.9225, 43.6583],
    "Breil-sur-Roya": [7.5175, 43.9358],
    "Tende": [7.5953, 44.0892],
    "Aubagne": [5.5708, 43.2925],
    "Hyères": [6.1294, 43.1203],
    "Aix-en-provence": [5.4474, 43.5297],
    "Pertuis": [5.5022, 43.6936],
    "Gap": [6.0786, 44.5589],
    "Briançon": [6.6367, 44.8978],
    "Valence": [4.8920, 44.9334],
    "Romans": [5.0514, 45.0444],
    "Miramas": [5.0058, 43.5858],
    "Avignon": [4.8108, 43.9493],
    "Nîmes": [4.3601, 43.8367],
    "Montpellier": [3.8767, 43.6108],
    "Carpentras": [5.0481, 44.0558],

    # Région Normandie
    "Caen": [-0.3706, 49.1829],
    "Coutances": [-1.4456, 49.0475],
    "Saint-Lô": [-1.0914, 49.1158],
    "Evreux": [1.1508, 49.0250],
    "Cherbourg": [-1.6228, 49.6393],
    "Lisieux": [0.2258, 49.1464],
    "Granville": [-1.5978, 48.8367],
    "Rennes": [-1.6778, 48.1173],
    "Trouville-Deauville": [0.0808, 49.3658],
    "Dives-Cabourg": [-0.1172, 49.2875],

    # Région Nouvelle-Aquitaine
    "Rochefort": [-0.9619, 45.9367],
    "Saintes": [-0.6333, 45.7467],
    "Bordeaux": [-0.5792, 44.8378],
    "Angoulême": [0.1578, 45.6500],
    "Royan": [-1.0281, 45.6250],
    "Niort": [-0.4594, 46.3236],
    "Poitiers": [0.3333, 46.5803],
    "Tours": [0.6833, 47.3941],
    "Châtellerault": [0.5461, 46.8178],
    "Limoges": [1.2611, 45.8336],
    "Toulouse": [1.4442, 43.6047],

    # Région Auvergne-Rhône-Alpes
    "Clermont": [3.0869, 45.7772]
}

def normalize_city_name(city):
    """Normalise le nom d'une ville pour la recherche"""
    # Supprimer les espaces en début/fin
    city = city.strip()
    # Remplacer les variations
    replacements = {
        "Saint-Die-des-vosges": "Saint-Die-des-vosges",
        "Château Thierry": "ChâteauThierry",
        "Les Arcs Draguignan": "LesArcsDraguignan",
        "Les Sables d'olonne": "LesSablesd'olonne",
        "La Roche-sur-yon": "LaRoche-sur-yon",
        "La Rochelle": "LaRochelle",
        "Le Tréport": "LeTréport",
        "Aix-en-Provence": "Aix-en-provence"
    }
    return replacements.get(city, city)

def parse_relation(relation):
    """Parse une relation pour extraire les villes de départ et d'arrivée"""
    # Séparer par '>'
    cities = [c.strip() for c in relation.split('>')]

    if len(cities) >= 2:
        # Prendre la première et la dernière ville
        start_city = normalize_city_name(cities[0])
        end_city_raw = cities[-1]

        # Gérer les cas où la destination est "Ville1/Ville2"
        if '/' in end_city_raw:
            # Prendre la première ville de la liste
            end_city = normalize_city_name(end_city_raw.split('/')[0].strip())
        else:
            end_city = normalize_city_name(end_city_raw)

        return start_city, end_city

    return None, None

def get_coordinates(city_name):
    """Récupère les coordonnées d'une ville"""
    if city_name in CITY_COORDINATES:
        return CITY_COORDINATES[city_name]

    # Essayer des variations
    variations = [
        city_name.replace('-', ' '),
        city_name.replace(' ', '-'),
        city_name.replace('é', 'e').replace('è', 'e').replace('ê', 'e'),
        city_name.lower().title()
    ]

    for var in variations:
        if var in CITY_COORDINATES:
            return CITY_COORDINATES[var]

    return None

def should_replace_with_straight_line(feature, routes_by_coords):
    """Détermine si un trajet doit être remplacé par une ligne droite"""
    coords = feature['geometry']['coordinates']
    num_coords = len(coords)

    # Créer un hash des coordonnées
    first_point = tuple(coords[0])
    last_point = tuple(coords[-1])
    coord_hash = (first_point, last_point, num_coords)

    # Si plusieurs trajets partagent exactement les mêmes coordonnées (départ, arrivée, nombre)
    # alors ce sont probablement des fausses routes
    if coord_hash in routes_by_coords and len(routes_by_coords[coord_hash]) > 1:
        return True

    # Si le trajet a très peu de coordonnées (< 15) et semble suspect
    if num_coords < 15:
        return True

    return False

def fix_routes(input_file, output_file):
    """Corrige les routes en remplaçant les fausses par des lignes droites"""

    print(f"Lecture de {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # D'abord, identifier tous les groupes de coordonnées dupliquées
    routes_by_coords = {}
    for i, feature in enumerate(data['features']):
        coords = feature['geometry']['coordinates']
        first_point = tuple(coords[0])
        last_point = tuple(coords[-1])
        coord_hash = (first_point, last_point, len(coords))

        if coord_hash not in routes_by_coords:
            routes_by_coords[coord_hash] = []
        routes_by_coords[coord_hash].append(i)

    print(f"\nTraitement de {len(data['features'])} features...")

    replaced_count = 0
    not_found_count = 0
    kept_count = 0

    for i, feature in enumerate(data['features']):
        relation = feature['properties'].get('relation', 'N/A')

        if should_replace_with_straight_line(feature, routes_by_coords):
            # Parser la relation pour extraire départ et arrivée
            start_city, end_city = parse_relation(relation)

            if start_city and end_city:
                start_coords = get_coordinates(start_city)
                end_coords = get_coordinates(end_city)

                if start_coords and end_coords:
                    # Remplacer par une ligne droite
                    old_coords_count = len(feature['geometry']['coordinates'])
                    feature['geometry']['coordinates'] = [start_coords, end_coords]
                    print(f"✓ {i:3d}: {relation:50s} ({old_coords_count} -> 2 coords)")
                    replaced_count += 1
                else:
                    print(f"✗ {i:3d}: {relation:50s} - Coordonnées non trouvées: {start_city} ou {end_city}")
                    not_found_count += 1
            else:
                print(f"✗ {i:3d}: {relation:50s} - Impossible de parser la relation")
                not_found_count += 1
        else:
            kept_count += 1

    print(f"\n{'='*80}")
    print(f"RÉSUMÉ")
    print(f"{'='*80}")
    print(f"Trajets remplacés par des lignes droites: {replaced_count}")
    print(f"Trajets conservés (itinéraires détaillés): {kept_count}")
    print(f"Trajets non traités (coordonnées non trouvées): {not_found_count}")

    print(f"\nÉcriture de {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Terminé!")

if __name__ == '__main__':
    fix_routes('etat_lignes_carte.geojson', 'etat_lignes_carte.geojson')
