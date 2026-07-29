# Alexandre Lasly — Portfolio professionnel

Site statique de présentation du parcours professionnel d’Alexandre Lasly.

## Contenu

- synthèse du profil commercial B2B ;
- expériences professionnelles vérifiées à partir du CV source ;
- compétences, formations, langues et centres d’intérêt ;
- coordonnées révélées uniquement après interaction afin de limiter le scraping naïf ;
- thème clair/sombre et mise en page responsive.

## Confidentialité

Le dépôt ne publie ni adresse personnelle ni PDF complet du CV. L’e-mail et le téléphone ne figurent pas en clair dans le HTML ou les métadonnées ; ils sont reconstruits dans le navigateur après un clic. Cette obfuscation réduit la collecte automatisée simple mais ne constitue pas une protection absolue contre un bot exécutant JavaScript.

## Développement local

Installer les dépendances et reconstruire le bundle Motion :

```bash
npm install
npm run build
```

Puis lancer le site :

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Ouvrir ensuite `http://127.0.0.1:8765/`.

Les animations sont définies dans `src/motion.js` et compilées dans `assets/motion.bundle.js`. Le contenu reste visible sans JavaScript et les animations sont désactivées lorsque `prefers-reduced-motion: reduce` est actif.

## Publication

Le site est conçu pour GitHub Pages depuis la branche `main`, répertoire `/`.

## Stack

HTML5, CSS natif, JavaScript sans framework, Motion 12 et esbuild pour le bundle d’animation.
