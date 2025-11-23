# 🚆 Carte de la concurrence ferroviaire en France

Visualisation interactive des lignes TER et TET ouvertes à la concurrence en France métropolitaine (hors Île-de-France et Corse).

![Carte de concurrence ferroviaire](https://img.shields.io/badge/status-active-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

## 📋 Description

Cette application web permet de visualiser l'état de l'ouverture à la concurrence du transport ferroviaire régional en France. Elle affiche sur une carte interactive les lignes ferroviaires selon leur statut :

- 🔴 **Attribuées à un concurrent** - Lignes exploitées par un opérateur concurrent de la SNCF
- 🔵 **Attribuées à la SNCF** - Lignes toujours exploitées par la SNCF
- 🟠 **Mises en concurrence** - Lignes en processus d'attribution, pas encore attribuées

## 🎯 Fonctionnalités

- ✅ Carte interactive avec Leaflet.js
- ✅ Visualisation différenciée par statut (code couleur)
- ✅ Informations détaillées au survol de chaque ligne
- ✅ Popup avec détails complets au clic
- ✅ Statistiques globales en temps réel
- ✅ Légende claire et explicite
- ✅ Interface responsive et moderne
- ✅ Indicateur de chargement
- ✅ Gestion d'erreurs explicite

## 🚀 Démarrage rapide

### Prérequis

- Python 3.x (déjà installé sur la plupart des systèmes Linux/macOS)
- Un navigateur web moderne (Chrome, Firefox, Safari, Edge)

### Installation

1. **Cloner ou télécharger ce dépôt**

```bash
git clone <url-du-depot>
cd carto_concurrence_ter
```

2. **Lancer le serveur HTTP**

```bash
python3 server.py
```

Ou avec Python 2/3 :

```bash
python server.py
```

Ou avec le module http.server de Python :

```bash
python3 -m http.server 8000
```

3. **Ouvrir dans le navigateur**

Une fois le serveur démarré, ouvrez votre navigateur à l'adresse :

```
http://localhost:8000
```

## 📁 Structure du projet

```
carto_concurrence_ter/
├── index.html                    # Application web principale
├── etat_lignes_carte.geojson    # Données des lignes ferroviaires
├── server.py                     # Serveur HTTP simple pour développement
└── README.md                     # Ce fichier
```

## 🔧 Utilisation avancée

### Changer le port du serveur

Par défaut, le serveur démarre sur le port 8000. Pour utiliser un autre port :

```bash
python3 server.py 3000
```

Puis ouvrez `http://localhost:3000`

### Déploiement en production

Pour un déploiement en production, vous pouvez :

1. **Hébergement statique** (GitHub Pages, Netlify, Vercel)
   - Simplement pusher les fichiers `index.html` et `etat_lignes_carte.geojson`
   - Ces plateformes servent automatiquement les fichiers via HTTPS

2. **Serveur web (Nginx, Apache)**
   - Configurer un virtual host pointant vers le dossier du projet
   - Exemple Nginx :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    root /chemin/vers/carto_concurrence_ter;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 📊 Données

Les données sont stockées au format GeoJSON dans le fichier `etat_lignes_carte.geojson`.

### Structure des données

Chaque ligne ferroviaire contient les propriétés suivantes :

- `region` : Région administrative
- `relation` : Nom de la relation (origine > destination)
- `statut` : Statut de la ligne (attribue_concurrent, attribue_SNCF, mis_en_concurrence_pas_attribue)
- `operateur` : Nom de l'opérateur (si attribué)
- `type_marche` : Type de marché (TER, TET)
- `lot` : Nom du lot de lignes
- `code_ligne` : Code de la ligne
- `libelle_ligne` : Libellé officiel de la ligne

### Mise à jour des données

Pour mettre à jour les données, remplacez simplement le fichier `etat_lignes_carte.geojson` en conservant la même structure.

## 🎨 Personnalisation

### Modifier les couleurs

Les couleurs sont définies dans la fonction `getColor()` dans `index.html` (lignes 132-143) :

```javascript
function getColor(statut) {
    switch(statut) {
        case 'attribue_concurrent':
            return '#e74c3c'; // Rouge
        case 'attribue_SNCF':
            return '#3498db'; // Bleu
        case 'mis_en_concurrence_pas_attribue':
            return '#f39c12'; // Orange
        default:
            return '#95a5a6'; // Gris
    }
}
```

### Modifier le style de la carte

Le fond de carte utilise OpenStreetMap. Vous pouvez le changer en modifiant l'URL du `tileLayer` (ligne 126) :

```javascript
// Exemples d'autres fonds de carte
// CartoDB Positron (clair et minimaliste)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CartoDB'
}).addTo(map);

// Stamen Terrain (relief)
L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.png', {
    attribution: 'Map tiles by Stamen Design'
}).addTo(map);
```

## ⚠️ Dépannage

### Problème : La carte ne se charge pas

**Solution** : Assurez-vous d'utiliser un serveur HTTP local. Les navigateurs bloquent les requêtes `fetch()` depuis le protocole `file://` pour des raisons de sécurité (CORS).

### Problème : Erreur "Port already in use"

**Solution** : Un autre processus utilise déjà le port 8000. Essayez un autre port :

```bash
python3 server.py 8001
```

### Problème : Le fichier GeoJSON ne se charge pas

**Vérifications** :
1. Le fichier `etat_lignes_carte.geojson` est bien dans le même dossier que `index.html`
2. Le fichier GeoJSON est valide (testez sur [geojson.io](https://geojson.io))
3. Vous utilisez un serveur HTTP local (pas `file://`)

## 📝 Source des données

Données issues de **Contexte** (17/11/2025) concernant l'ouverture à la concurrence du transport ferroviaire régional français.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🔗 Liens utiles

- [Leaflet.js Documentation](https://leafletjs.com/)
- [GeoJSON Specification](https://geojson.org/)
- [OpenStreetMap](https://www.openstreetmap.org/)

## 👤 Auteur

Créé avec ❤️ pour visualiser l'ouverture à la concurrence du rail français.

---

**Note** : Cette visualisation est fournie à titre informatif. Pour des informations officielles sur l'ouverture à la concurrence, consultez les sources gouvernementales et les autorités organisatrices de transport.
