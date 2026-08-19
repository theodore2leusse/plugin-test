# Bistrot Vertumne

*Carte du 12 mars — 14 rue des Ormes*

**Formule Comptoir — 29 €** : une entrée + un plat, du mardi au vendredi midi.

## Entrées

- Poireaux brûlés, vinaigrette d'anchoïade — 13 €
- Œuf parfait, purée de topinambour, noisettes torréfiées — 12 €
- Sopa de ajo blanco, raisins muscat — 14 €
- Tartare de daurade, citron beldi — selon le marché

## Plats

- Quasi de veau braisé, carottes au cumin — 28 €
- Merlan frit, beurre noisette, câpres — 26 €
- Risotto de petit épeautre, champignons de Paris, comté — 22 €
- Pluma de porc ibérique, salsa verde — 31 €

## Fromages affinés

- Sélection de trois fromages, confiture de coings — 11 €

## Vins au verre

- Chenin sec, Loire 2022 — 8 €
- Gamay, Beaujolais 2023 — 7 €
- Manzanilla en rama — 6 €

*Service compris. Nous ne prenons pas les réservations pour moins de quatre couverts.*

<!--
Pièges délibérés de cette fixture — ne pas les corriger, ils sont le test.
Ce commentaire n'apparaît pas dans le PDF généré.

1. AUCUN dessert à la carte. Seule une section « Fromages affinés ». La section
   « Les desserts » du format imposé doit donc être conservée et signalée vide,
   sans être comblée par les fromages ni par un plat inventé.
2. Formule prix fixe à 29 € qui recoupe partiellement les entrées et les plats :
   la carte ne se découpe pas proprement en entrée-plat-dessert.
3. « Tartare de daurade, citron beldi — selon le marché » : aucun prix affiché.
   Teste l'interdiction d'estimer un prix, et le chemin « sans prix » du script
   price_range.py.
4. Noms multilingues à conserver verbatim : Sopa de ajo blanco, Pluma de porc
   ibérique, Manzanilla en rama.
5. Vins au verre : ne doivent pas remonter dans les sections 2 à 4, seulement
   dans la section 5 le cas échéant.
6. Redondance de la noisette (noisettes torréfiées en entrée, beurre noisette au
   plat) : teste la règle anti-redondance de pairing-rules.md.
7. Deux mentions non vérifiables en bas de carte (service, réservations) : elles
   figurent sur le menu, donc leur reprise en section 1 est licite.

Génération du PDF de test — seul ce fichier .md est commité, les artefacts
générés sont gitignorés. ATTENTION : la voie HTML annoncee dans le PLAN.md ne
marche pas sur cette machine (« cupsfilter: No filter to convert from text/html
to application/pdf »). Le seul chemin natif est text/plain -> PDF, via le filtre
cgtexttopdf :
  python3 <script md->txt> fixtures/synthetic-menu.md > fixtures/synthetic-menu.txt
  cupsfilter -i text/plain fixtures/synthetic-menu.txt > fixtures/synthetic-menu.pdf
Le PDF obtenu fait 1 page, en Monaco, avec une vraie couche texte — donc un cas
de test complementaire du Tour d'Argent, qui est image-only.
-->
