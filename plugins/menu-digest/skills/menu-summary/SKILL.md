---
name: menu-summary
description: Résume la carte d'un restaurant en cinq sections imposées — présentation du restaurant, entrées, plats, desserts, puis conseils pour profiter du repas. À utiliser dès que l'utilisateur fournit un menu ou une carte de restaurant (PDF, photo, capture d'écran ou texte) et demande un résumé, une synthèse, une présentation ou une explication de ce menu.
---

# Résumé de carte de restaurant

Le menu fourni est déjà lisible : lis-le directement. N'écris ni n'exécute aucun code, et
n'utilise aucun outil pour en extraire le texte.

Produis un résumé en cinq sections, toujours les mêmes, toujours dans le même ordre.

## Format de sortie

Reproduis exactement ces cinq titres, en titres markdown de niveau 2, dans cet ordre :

```markdown
## Le restaurant
## Les entrées
## Les plats
## Les desserts
## Pour profiter au mieux du repas
```

N'ajoute aucune section, n'en omets aucune, ne renomme aucun titre. Ne place ni préambule ni
conclusion autour du bloc. Une catégorie vide se signale **dans** sa section, elle ne se
supprime pas.

## Règles de fidélité

### Sections « Les entrées », « Les plats », « Les desserts » — fidélité stricte

- Ne liste que des plats effectivement présents sur la carte.
- Reprends les noms de plats **verbatim**, dans leur langue d'origine. Ajoute au besoin une
  glose courte entre parenthèses, sans jamais remplacer le nom original.
- N'invente jamais un prix, un ingrédient, une provenance ni une allergie. Ne cite un prix que
  s'il figure sur la carte.
- Si une catégorie est absente, écris-le explicitement (« ce menu ne propose pas de desserts »)
  et ne comble pas le vide avec des plats d'une autre catégorie.
- Si un passage est illisible, signale-le plutôt que de deviner.

### Sections « Le restaurant » et « Pour profiter au mieux du repas » — inférence balisée

- La culture générale est autorisée (type de cuisine, région, tradition culinaire), mais chaque
  affirmation doit être rattachable à un élément visible du menu.
- N'affirme rien sur l'ambiance, le service, les prix pratiqués ou la réputation, sauf mention
  explicite sur le menu.
- Appuie les conseils sur la composition réelle de la carte — redondances d'ingrédients, plats à
  partager, ordre suggéré, formules avantageuses. Pas de généralités interchangeables du type
  « réservez à l'avance » ou « demandez conseil au sommelier ».

### Langue

Réponds dans la langue de la conversation. Les noms de plats restent en langue d'origine.

## Cas limites

- **Catégorie absente de la carte** : conserve la section et indique en une phrase que la carte
  ne propose pas cette catégorie.
- **Menu à formules ou prix fixe** qui ne se découpe pas en entrée-plat-dessert : garde les cinq
  sections, répartis les plats dans la catégorie qui leur correspond, et décris la mécanique des
  formules (nombre de services, prix, choix imposés) dans « Le restaurant ».
- **Carte des vins et boissons** : exclue des sections 2 à 4. Elle peut être mentionnée dans
  « Pour profiter au mieux du repas » si elle éclaire un choix.
- **Plusieurs restaurants ou plusieurs services** (déjeuner / dîner, carte et menu dégustation)
  dans un même document : ne mélange pas les offres. Annonce le découpage dans « Le restaurant »,
  puis étiquette chaque plat par son service dans les sections concernées.
- **Passages illisibles** : mentionne-les à l'endroit concerné (« deux plats illisibles en bas de
  la page 3 »). Ne reconstitue rien par déduction.
- **Menu multilingue** : choisis la version qui correspond à la langue de la conversation pour la
  glose, et garde le nom du plat dans sa langue d'origine.

## Longueur cible

- « Le restaurant » : 3 à 5 phrases.
- « Les entrées », « Les plats », « Les desserts » : une ligne par plat, en liste à puces —
  nom verbatim, puis une brève description si la carte en fournit une, puis le prix s'il figure.
- « Pour profiter au mieux du repas » : 3 à 5 conseils, en liste à puces.

## Exemple de sortie

Pour une carte fictive de six plats affichant « Menu du marché — 34 € : entrée + plat » :

```markdown
## Le restaurant

Une petite carte de bistrot français contemporain, construite autour de six plats seulement,
signe d'une cuisine resserrée sur des produits de saison. Les intitulés mettent en avant les
légumes (poireau, courge) autant que les viandes, et deux plats sont annoncés au beurre noisette.
Une formule « Menu du marché » à 34 € couvre une entrée et un plat, mais pas le dessert.

## Les entrées

- **Poireaux vinaigrette, œuf mimosa** — 12 €
- **Velouté de courge, huile de noisette** — 11 €

## Les plats

- **Quasi de veau, jus au romarin** — 26 €
- **Merlan colbert, beurre noisette** — 24 €
- **Risotto de petit épeautre aux champignons** — 21 €

## Les desserts

- **Paris-brest** — 9 €

## Pour profiter au mieux du repas

- La formule à 34 € rend l'entrée quasi gratuite si vous prenez le quasi de veau à 26 € ;
  elle est en revanche sans intérêt sur le risotto à 21 €.
- Le beurre noisette du merlan revient dans l'huile de noisette du velouté : alternez plutôt
  avec les poireaux vinaigrette pour ouvrir le repas sur une note acide.
- Un seul dessert à la carte, et il n'entre pas dans la formule : à commander dès le début si
  vous y tenez.
- Le risotto de petit épeautre est le seul plat sans viande ni poisson.
```
