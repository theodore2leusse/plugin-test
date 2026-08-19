---
name: menu-tasting-plan
description: Compose un menu dégustation en trois services à partir de la carte d'un restaurant — un accord de saveurs justifié plus une fourchette de budget par personne calculée sur les prix affichés. À utiliser quand l'utilisateur a fourni une carte ou un menu (PDF, photo, capture ou texte) et demande une sélection, une suggestion, un choix de plats, un accord ou un menu dégustation. À ne pas utiliser s'il demande un résumé, une synthèse ou une présentation de la carte, qui relève de la skill menu-summary.
---

# Menu dégustation en trois services

Le menu fourni est déjà lisible : lis-le directement. N'écris ni n'exécute aucun code pour en
extraire le texte.

Compose **un** accord en trois services — une entrée, un plat, un dessert — choisis uniquement
parmi les plats réellement présents sur la carte.

## Marche à suivre

1. Relève tous les plats de la carte avec leur prix affiché, catégorie par catégorie.
2. Lis `references/pairing-rules.md` **avant de composer l'accord**, et seulement à ce
   moment-là : ce fichier porte les règles de progression et d'équilibre à appliquer.
3. Choisis les trois services en appliquant ces règles.
4. Calcule la fourchette de budget avec `scripts/price_range.py` (voir plus bas). Ne calcule
   jamais les prix de tête.
5. Rends la réponse au format ci-dessous.

## Fidélité

- Ne propose que des plats figurant sur la carte, avec leur nom **verbatim** en langue d'origine.
- N'invente jamais un prix, un ingrédient ou une provenance. Le prix vient de la carte, jamais
  d'une estimation ni d'une moyenne de marché.
- Si un plat est affiché sans prix, garde-le tel quel et signale que son prix n'est pas affiché.
- Réponds dans la langue de la conversation.

## Budget — appel du script

Passe les trois services retenus sur l'entrée standard, en JSON :

```bash
echo '{"courses":[{"name":"Poireaux vinaigrette","price":12},{"name":"Quasi de veau","price":26},{"name":"Paris-brest","price":9}]}' | python3 scripts/price_range.py
```

Le script renvoie le total, le prix minimum, maximum et médian des services, et le budget par
personne. Ajoute `"guests": 4` au JSON pour obtenir en plus le budget du groupe. Omets la clé
`price` d'un service dont le prix n'est pas affiché : le script l'exclut du calcul et le signale.
Reprends les chiffres du script sans les retoucher.

## Format de sortie

```markdown
## L'accord proposé
1. **Entrée** — <nom verbatim> (<prix>)
2. **Plat** — <nom verbatim> (<prix>)
3. **Dessert** — <nom verbatim> (<prix>)

## Pourquoi cet accord
<3 à 5 phrases : progression des saveurs, absence de redondance, montée en richesse>

## Budget
<les chiffres renvoyés par le script, en une ou deux phrases>
```

## Cas limites

- **Pas de dessert à la carte** : dis-le, et propose à sa place un fromage ou un service sucré
  effectivement présent. Ne complète jamais par un plat absent de la carte.
- **Pas d'entrée, ou carte à formules imposées** : respecte le découpage réel de la carte et
  explique en une phrase l'écart avec le format en trois services.
- **Demande végétarienne, sans alcool ou allergie** : n'écarte que les plats dont la carte permet
  de conclure. Si la composition d'un plat est incertaine, propose-le en le signalant comme
  à vérifier auprès du restaurant.
- **Aucun prix sur la carte** : compose l'accord et indique que le budget n'est pas calculable.
  N'estime rien.
- **Vins et boissons** : ne les compte pas comme un service. Une suggestion d'accord est
  possible dans « Pourquoi cet accord » si la carte des vins est visible.
- **Plusieurs services ou plusieurs restaurants** dans le document : demande lequel viser, ou
  compose un accord par offre en les étiquetant clairement.
