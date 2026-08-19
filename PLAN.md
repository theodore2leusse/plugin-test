# Plan de réalisation — plugin Claude « menu-digest »

> Document de spécification destiné à être exécuté par un agent de code lors d'une session
> ultérieure. Rédigé le 2026-08-19. Les décisions ci-dessous sont **arrêtées** : ne pas les
> rouvrir sans instruction explicite de l'utilisateur.

---

## 1. Objectif

Construire un **plugin Claude bidon mais structurellement réaliste**, installable dans un
Claude Enterprise et consommable **dans le chat et dans Cowork**. Le but n'est pas le plugin
lui-même : c'est d'apprendre la mécanique de packaging et de distribution, pour livrer ensuite
un vrai plugin dans l'org Enterprise d'un client en réutilisant l'ossature.

Cas d'usage bidon retenu : **résumer un menu de restaurant déposé en PDF** selon un format
éditorial imposé en 5 sections.

---

## 2. Décisions arrêtées

| Sujet | Décision |
|---|---|
| Type d'artefact | **Plugin** (bundle `.claude-plugin/` + `skills/`), pas une skill isolée |
| Surfaces cibles | chat web + onglet Chat de Claude Desktop + Cowork |
| Charge utile | Essentiellement des **skills** (markdown), + 1 sub-agent + 1 hook |
| Hébergement | Repo **GitHub public** sous le compte `theodore2leusse` |
| Auth git | **SSH** (déjà fonctionnel, testé) |
| Sortie du résumé | **Markdown dans la réponse de chat**, aucun fichier généré |
| Langue de sortie | Langue de la conversation ; noms de plats **verbatim** dans leur langue d'origine |
| Fidélité au PDF | Strict sur les sections 2-4, inférence balisée sur 1 et 5 (cf. §5) |
| Fixtures PDF | **Gitignorées**. Seule la source markdown du menu synthétique est commitée |
| Arborescence | Marketplace catalogue + `plugins/<nom>/` (extensible à N plugins) |
| Nom du marketplace | `theodo-lab` |
| Nom du plugin | `menu-digest` |
| Découpage | Phase 1 = squelette minimal validé de bout en bout, PUIS phase 2 |

---

## 3. Faits techniques vérifiés — ne pas re-chercher

Ces points ont été vérifiés dans la documentation officielle pendant la session de cadrage.

1. **Claude lit nativement les PDF déposés en chat.** La skill ne doit contenir **aucun** code
   d'extraction PDF (`pdfplumber` & co). Sa seule valeur est le format de sortie et les règles
   de rédaction.
2. **Répartition des composants par surface :**
   - *skills* → fonctionnent en chat **et** en Cowork ;
   - *hooks* et *sub-agents* → **Cowork uniquement**, grisés en chat ;
   - *commands* → mécanique Claude Code, non consommée en chat/Cowork → **on n'en crée aucune** ;
   - *serveurs MCP locaux* → chat et Cowork, hors périmètre ici.
3. **Structure d'un plugin :** seul `plugin.json` vit dans `.claude-plugin/`. Tous les autres
   répertoires (`skills/`, `agents/`, `hooks/`, `.mcp.json`) sont au **root du plugin**.
4. **Chemins de découverte par défaut** : `skills/<nom>/SKILL.md`, `agents/*.md`,
   `hooks/hooks.json`. Ils suffisent → **ne pas déclarer** les champs `skills`/`agents`/`hooks`
   dans `plugin.json`. Piège : les champs `commands` et `agents` **remplacent** le défaut au lieu
   de s'y ajouter.
5. **Sources relatives** (`"source": "./plugins/menu-digest"`) : résolues par rapport au
   répertoire contenant `.claude-plugin/`. Elles fonctionnent si le marketplace est ajouté
   **depuis un dépôt git**, mais **PAS** si l'utilisateur pointe directement l'URL du fichier
   `marketplace.json` (seul ce fichier est alors téléchargé).
6. **Contraintes de frontmatter d'une skill** : `name` et `description` obligatoires.
   `name` ≤ 64 car., minuscules/chiffres/tirets uniquement, interdiction des mots réservés
   `anthropic` et `claude`. `description` ≤ 1024 car., doit dire **ce que fait** la skill **et
   quand l'utiliser** (c'est sur elle que se joue le déclenchement).
7. **Divulgation progressive** : niveau 1 = frontmatter (toujours chargé, ~100 tokens) ;
   niveau 2 = corps du SKILL.md (au déclenchement, viser < 5k tokens) ; niveau 3 = fichiers de
   référence et scripts (lus/exécutés à la demande — le code d'un script n'entre **jamais** en
   contexte, seule sa sortie compte).
8. **Provisioning org-wide** : réservé aux rôles Owner / Primary Owner via
   `Organization settings > Plugins` (Team/Enterprise). Modes de diffusion par plugin :
   *installed by default*, *available for install*, *not available*, *required* ; override par
   groupe en Enterprise. Prérequis org : **Cowork ET Skills activés**.
9. **Rôles custom Enterprise** : ils pilotent des capabilities (chat, Cowork, Claude Code) et des
   zones admin (Identity & Access, Billing, Analytics, Privacy, User Management, Libraries).
   **Aucune zone « Plugins »** n'y figure → un rôle custom peut permettre d'*installer* un plugin
   sans permettre d'en *provisionner*.
10. **⚠️ Documentation périmée à ignorer** : la page
    `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` affirme encore que les
    skills claude.ai sont « individual only, pas d'administration centralisée ». C'est faux
    depuis l'arrivée du provisioning org-wide. Se fier au Help Center.
11. **Validation locale** : `claude plugin validate .` (ou `/plugin validate .`) depuis la racine
    du marketplace.
12. **Noms de marketplace réservés** (interdits) : `claude-code-marketplace`, `claude-code-plugins`,
    `claude-plugins-official`, `anthropic-marketplace`, `agent-skills`, `knowledge-work-plugins`,
    etc. `theodo-lab` est libre.

### État de la machine (vérifié)

- `git` configuré : `theodore2leusse` — SSH GitHub **authentifié et fonctionnel**.
- **`gh` CLI absent** → la création du dépôt GitHub est une **étape humaine**.
- Aucun remote configuré sur le repo local, aucun commit.
- **Aucun outil de lecture PDF en local** (`poppler`, `pypdf`, `pdfplumber`, `PIL` : absents).
  → Un agent de code **ne peut pas** auto-évaluer la qualité d'un résumé. Cette vérification est
  **manuelle**, via la grille du §7. Ne pas installer `poppler` : inutile au projet.
- `cupsfilter` (natif macOS) : **la voie HTML est fausse** — vérifiée le 2026-08-19,
  `cupsfilter: No filter to convert from text/html to application/pdf`. Les filtres présents
  ne couvrent que `text/plain`, `image/*` et `application/pdf` (`cgtexttopdf`, `cgimagetopdf`).
  Seul chemin natif retenu : `cupsfilter -i text/plain fichier.txt > fichier.pdf`.

### Fixture disponible

`Tourd Argent Menu April 2025.pdf` (943 Ko), présent à la racine, **à déplacer dans `fixtures/`**.
Analysé : **4 pages, 311×1106 pt** (format ~4×15 pouces = capture de page web), **aucune police,
~1012 objets image → PDF image-only, sans couche texte**. Le test reposera donc entièrement sur la
vision/OCR de Claude. C'est un menu gastronomique : sa carte ne se découpera probablement pas
proprement en entrées/plats/desserts, ce qui en fait un bon cas de stress pour le format imposé.

---

## 4. Arborescence cible

```
plugin-test/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── menu-digest/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── menu-summary/
│       │   │   └── SKILL.md
│       │   └── menu-tasting-plan/          # phase 2
│       │       ├── SKILL.md
│       │       ├── references/
│       │       │   └── pairing-rules.md
│       │       └── scripts/
│       │           └── price_range.py
│       ├── agents/
│       │   └── menu-critic.md              # phase 2
│       ├── hooks/
│       │   └── hooks.json                  # phase 2
│       └── README.md
├── fixtures/
│   ├── .gitignore                          # ignore *.pdf
│   └── synthetic-menu.md                   # commité (source du menu bidon)
├── .gitignore
├── PLAN.md
└── README.md
```

---

## Phase 0 — Prérequis (STOP-HUMAIN)

Rien ne sert de coder si l'installation est impossible. À faire **avant** la phase 1.

- [ ] **H0.1** Dans claude.ai, ouvrir `Customize` (barre latérale) → onglet `Plugins`. Vérifier
      que l'action « **Add marketplace** » / « Add from a repository » est **présente et non
      grisée**. Si absente → le rôle custom ou la configuration org bloque les marketplaces.
      *Branche de repli :* tester la skill seule via un ZIP dans `Settings > Capabilities`
      (skills personnelles), ce qui valide la rédaction de la skill mais **pas** le packaging
      plugin. Signaler le blocage à un Owner de l'org Theodo.
- [ ] **H0.2** Vérifier que **Cowork** est accessible pour le compte (onglet Cowork visible).
      Si non : la phase 2 (hook + sub-agent) sera **non testable** — la livrer quand même, mais
      ne pas chercher à la valider.
- [ ] **H0.3** Vérifier que l'exécution de code / création de fichiers est active (nécessaire au
      script de la phase 2). Si inactive : le script `price_range.py` sera inerte, le noter.
- [ ] **H0.4** Créer sur github.com un dépôt **public** vide nommé `plugin-test` sous le compte
      `theodore2leusse`. **Ne pas** l'initialiser avec un README (le local n'a aucun commit).
      Communiquer l'URL SSH à l'agent.

**Critère de sortie :** l'URL du dépôt distant est connue et l'ajout de marketplace est possible
dans claude.ai.

---

## Phase 1 — Squelette marchant de bout en bout

Objectif : valider **toute la chaîne** repo → marketplace → install → usage, avec le minimum de
contenu. Ne rien ajouter d'autre avant que le critère de sortie soit atteint.

### 1.1 Hygiène du dépôt

- Déplacer `Tourd Argent Menu April 2025.pdf` dans `fixtures/`.
- `.gitignore` à la racine : ignorer `*.pdf`, `.DS_Store`.
- `fixtures/.gitignore` : `*.pdf`.
- `README.md` racine : 15 lignes max — but du repo, comment ajouter le marketplace, avertissement
  « contenu de démonstration ».

### 1.2 `.claude-plugin/marketplace.json` — contenu littéral

```json
{
  "name": "theodo-lab",
  "owner": {
    "name": "Théodore de Leusse",
    "url": "https://github.com/theodore2leusse"
  },
  "description": "Marketplace bac à sable pour prototyper des plugins Claude",
  "plugins": [
    {
      "name": "menu-digest",
      "source": "./plugins/menu-digest",
      "displayName": "Menu Digest",
      "description": "Résume la carte d'un restaurant fournie en PDF selon un format éditorial fixe en 5 sections",
      "version": "0.1.0",
      "category": "productivity",
      "keywords": ["menu", "restaurant", "pdf", "resume"],
      "author": { "name": "Théodore de Leusse" },
      "license": "MIT"
    }
  ]
}
```

> Le dépôt étant **public**, ne mettre **aucune adresse e-mail** dans `owner` ni dans `author`.
> Le champ `email` est optionnel.

### 1.3 `plugins/menu-digest/.claude-plugin/plugin.json` — contenu littéral

```json
{
  "name": "menu-digest",
  "displayName": "Menu Digest",
  "version": "0.1.0",
  "description": "Résume la carte d'un restaurant fournie en PDF selon un format éditorial fixe en 5 sections",
  "author": { "name": "Théodore de Leusse" },
  "repository": "https://github.com/theodore2leusse/plugin-test",
  "license": "MIT",
  "keywords": ["menu", "restaurant", "pdf", "resume"]
}
```

> Volontairement **aucun** champ `skills`, `agents`, `hooks` : les chemins par défaut sont corrects
> et les déclarer expose au piège du §3.4.

### 1.4 `skills/menu-summary/SKILL.md`

**Frontmatter — contenu littéral :**

```yaml
---
name: menu-summary
description: Résume la carte d'un restaurant en cinq sections imposées — présentation du restaurant, entrées, plats, desserts, puis conseils pour profiter du repas. À utiliser dès que l'utilisateur fournit un menu ou une carte de restaurant (PDF, photo, capture d'écran ou texte) et demande un résumé, une synthèse, une présentation ou une explication de ce menu.
---
```

**Spécification du corps** (l'agent rédige la prose, en respectant ceci à la lettre) :

- Cible : **moins de 150 lignes**. Ton directif, à l'impératif, adressé à Claude — pas de
  paraphrase du format en langage marketing.
- **Ne mentionner aucun outil d'extraction PDF.** Le contenu du menu est déjà lisible.
- Une section « Format de sortie » donnant les **cinq titres de section exacts**, dans l'ordre,
  en tant que titres markdown de niveau 2.
- Une section « Règles de fidélité » reprenant le §5 mot pour mot dans l'esprit.
- Une section « Cas limites » couvrant : catégorie absente du menu ; menu à formules/prix fixe qui
  ne se découpe pas en entrée-plat-dessert ; carte des vins et boissons (à exclure des sections
  2-4, mentionnables en section 5) ; plusieurs restaurants ou plusieurs services dans un même PDF ;
  passages illisibles ; menu multilingue.
- Une section « Longueur cible » : introduction 3-5 phrases ; sections 2-4 = une ligne par plat ;
  section 5 = 3 à 5 conseils.
- **Un exemple de sortie courte et complète** en fin de fichier (menu fictif de 6 plats), qui sert
  de gabarit de référence.

### 1.5 Validation et livraison

- [ ] `claude plugin validate .` depuis la racine → aucune erreur.
- [ ] Vérifier à la main que `plugins/menu-digest/skills/menu-summary/SKILL.md` existe bien à ce
      chemin exact (une faute de chemin ici ne produit **aucune erreur** : la skill est
      silencieusement introuvable).
- [ ] Test local en Claude Code : `/plugin marketplace add .` puis
      `/plugin install menu-digest@theodo-lab`, et vérifier que `menu-summary` apparaît.
- [ ] Commit initial, `git remote add origin <url SSH>`, `git push -u origin main`.

**STOP-HUMAIN — critère de sortie de la phase 1 :**

- [ ] Dans claude.ai : `Customize > Plugins > Add marketplace` avec
      `https://github.com/theodore2leusse/plugin-test` → le plugin `Menu Digest` apparaît, puis
      `Install`.
- [ ] En chat, `menu-summary` est visible dans la liste `/`.
- [ ] Déposer le PDF du Tour d'Argent avec la consigne « résume ce menu ». La réponse contient les
      **cinq sections dans l'ordre**.
- [ ] Tester aussi **sans** invocation explicite (juste le PDF + « résume ce menu ») pour évaluer
      le déclenchement automatique par la `description`. Si la skill ne se déclenche pas,
      **le correctif est la `description`, pas le corps du SKILL.md.**

⛔ **Ne pas démarrer la phase 2 avant que ces quatre cases soient cochées.**

---

## Phase 2 — Enrichissement (progressive disclosure + surfaces Cowork)

### 2.1 Deuxième skill : `menu-tasting-plan`

Rôle : proposer un accord en 3 services à partir de la carte, avec une fourchette de budget.

- **Frontmatter** : `name: menu-tasting-plan` ; `description` mentionnant explicitement
  « menu dégustation », « accord 3 services », « budget », et la condition de déclenchement
  (l'utilisateur a fourni une carte et demande une sélection ou une suggestion, pas un résumé).
  Bien la différencier de `menu-summary` pour éviter le déclenchement croisé.
- **`references/pairing-rules.md`** — savoir embarqué (niveau 3), 40 à 80 lignes : progression des
  saveurs, éviter la redondance d'ingrédient entre services, règles d'équilibre
  (léger → riche → sucré), adaptations végétariennes, principes d'accord simples.
  Le SKILL.md doit **référencer ce fichier par son chemin relatif** et indiquer de ne le lire que
  lorsqu'un accord est réellement demandé.
- **`scripts/price_range.py`** — calcul déterministe :
  - lit sur **stdin** un JSON `{"courses": [{"name": str, "price": number}, ...]}` ;
  - écrit sur stdout un résumé lisible : total, min, max, médiane, et budget par personne ;
  - **bibliothèque standard uniquement** (`json`, `sys`, `statistics`) — le sandbox n'autorise
    aucune installation de paquet ;
  - gère proprement l'absence de prix (message explicite, pas de trace d'exception) ;
  - le SKILL.md précise **comment l'appeler** et rappelle que le prix doit venir du menu, jamais
    d'une estimation.

### 2.2 Sub-agent : `agents/menu-critic.md`

- Frontmatter avec `name` et `description` ; description du type « relit un résumé de menu produit
  et signale tout écart au format en 5 sections ou toute mention de plat absent de la carte ».
- Corps : une checklist de contrôle qui reprend la grille du §7.
- ⚠️ **Cowork uniquement.** Vérifier le format de frontmatter attendu pour un agent avant
  d'écrire — c'est le point le moins bien documenté du plan.

### 2.3 Hook : `hooks/hooks.json` — contenu littéral

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'menu-digest actif — deposez un menu PDF pour obtenir un resume en 5 sections.'"
          }
        ]
      }
    ]
  }
}
```

> Volontairement trivial : le seul but est de **rendre observable** qu'un hook s'exécute.
> Grisé en chat, actif en Cowork. Si `SessionStart` n'est pas supporté en Cowork, le noter dans le
> §8 plutôt que d'empiler les tentatives.

### 2.4 Fixture synthétique

- `fixtures/synthetic-menu.md` : menu bidon **commité** (contenu original, aucun droit tiers),
  avec entrées / plats / desserts, des prix, et **un piège délibéré** — par exemple une catégorie
  absente ou une formule prix fixe — pour éprouver les règles de fidélité.
- Le PDF produit reste **gitignoré**. Génération sans installer quoi que ce soit :
  `cupsfilter fixtures/synthetic-menu.html > fixtures/synthetic-menu.pdf`
  (convertir d'abord le markdown en HTML minimal).

### 2.5 Livraison

- Bump `version` à `0.2.0` **dans les deux** fichiers (`marketplace.json` **et** `plugin.json` :
  une version épinglée ne déclenche une mise à jour chez l'utilisateur que si la chaîne change).
- `claude plugin validate .`, commit, push.

**STOP-HUMAIN — critère de sortie de la phase 2 :**

- [ ] Mise à jour du plugin visible côté claude.ai après le push.
- [ ] `menu-tasting-plan` se déclenche sur une demande d'accord, et **pas** `menu-summary`.
- [ ] En Cowork : la bannière du hook apparaît, et `menu-critic` est listé.
- [ ] Le script produit une fourchette de budget cohérente avec les prix réels du menu.

---

## Phase 3 — Capitalisation pour le client

- `plugins/menu-digest/README.md` : ce que fait le plugin, comment l'installer, comment le modifier.
- Ajouter à ce PLAN.md une section **« Transposition client »** consignant :
  - ce qui a marché du premier coup et ce qui a résisté ;
  - la formulation de `description` qui déclenche le plus fiablement ;
  - la procédure exacte côté admin client (repo **privé ou interne** + **Claude GitHub App** +
    mode de diffusion, cf. §3.8 et §9) — ce chemin diffère du nôtre, qui passe par un repo public
    en scope personnel ;
  - la liste des permissions à demander à l'admin du client **avant** le démarrage.

---

## 5. Règles de fidélité (à reprendre dans le SKILL.md)

**Sections 2, 3 et 4 — strictement fidèles :**
- Ne lister **que** des plats effectivement présents sur la carte.
- Reprendre les **noms de plats verbatim**, dans leur langue d'origine.
- Ne **jamais** inventer un prix, un ingrédient, une provenance ou une allergie.
- Si une catégorie est absente, l'écrire explicitement (« ce menu ne propose pas de desserts »)
  et **ne pas** combler le vide.
- Si un passage est illisible, le signaler plutôt que de deviner.

**Sections 1 et 5 — inférence autorisée mais balisée :**
- La culture générale (type de cuisine, région, tradition) est autorisée, mais chaque affirmation
  doit être **rattachable à un élément visible du menu**.
- Interdiction d'affirmer quoi que ce soit sur l'ambiance, le service, les prix pratiqués ou la
  réputation, sauf mention sur le menu.
- Les conseils de la section 5 doivent s'appuyer sur la composition réelle de la carte
  (redondances, plats à partager, ordre suggéré), pas sur des généralités interchangeables.

**Langue :** répondre dans la langue de la conversation ; conserver les noms de plats en langue
d'origine, avec au besoin une glose courte entre parenthèses.

---

## 6. Format de sortie imposé

```markdown
## Le restaurant
## Les entrées
## Les plats
## Les desserts
## Pour profiter au mieux du repas
```

Ordre non négociable, aucune section supplémentaire, aucune section omise (une catégorie vide est
signalée dans sa section, pas supprimée).

---

## 7. Grille de vérification manuelle

À dérouler après chaque test, PDF ouvert à côté. Environ 2 minutes.

| # | Contrôle | OK |
|---|---|---|
| 1 | Les 5 sections sont présentes, dans l'ordre, avec les titres exacts | |
| 2 | Chaque plat cité figure réellement sur le menu (échantillonner 5 plats) | |
| 3 | Aucun plat du menu manquant dans sa catégorie (échantillonner 3 plats) | |
| 4 | Les noms de plats sont verbatim, non traduits, non reformulés | |
| 5 | Aucun prix inventé ; les prix cités correspondent au menu | |
| 6 | Les catégories absentes sont signalées, pas comblées | |
| 7 | La section 1 n'affirme rien d'invérifiable sur le restaurant | |
| 8 | Les conseils de la section 5 sont spécifiques à cette carte, pas génériques | |
| 9 | La langue de réponse est celle de la conversation | |
| 10 | Les boissons et vins ne polluent pas les sections 2-4 | |

---

## 8. Incertitudes assumées

À lever par l'observation lors de l'exécution, sans y consacrer d'effort de recherche préalable :

1. Le **rôle custom** de l'utilisateur autorise-t-il l'ajout d'un marketplace ? → phase 0.
2. **Cowork** supporte-t-il l'événement `SessionStart` d'un hook de plugin ? → phase 2.
3. ~~Format exact du **frontmatter d'un sub-agent**~~ → **levé le 2026-08-19** pour Claude Code :
   `name` et `description` obligatoires, `model` / `color` / `tools` optionnels ; deux syntaxes de
   `tools` acceptées (`tools: Read, Grep` et `tools: ["Read", "Grep"]`) ; omettre `tools` = accès
   complet (`plugin-dev/agents/agent-creator.md:110`). Sur 34 agents du marketplace officiel, 22
   déclarent `tools` — mais **tous** avec des noms d'outils Claude Code, et « Cowork » n'apparaît
   que dans un seul fichier de tout ce marketplace. Décision prise en conséquence : `menu-critic`
   **ne déclare pas `tools`** et est **conçu sans besoin d'outil** (il travaille sur le résumé et la
   carte que l'appelant lui passe dans le prompt). Reste à observer en Cowork : l'inventaire réel
   d'outils offert à un sub-agent, pour pouvoir déclarer une liste juste côté client.
4. Comportement d'un PDF **image-only de 4 pages** en chat : qualité de l'OCR, coût en contexte.
5. **Fiabilité du déclenchement automatique** de la skill sur simple dépôt de PDF, sans `/`.
6. Le versioning : un push suffit-il à propager la mise à jour, ou faut-il réinstaller le plugin ?

---

## 9. Le client est sur Claude **Team**, pas Enterprise

Vérifié en documentation. **Aucun impact sur le plugin lui-même** : format, arborescence,
manifestes et skills sont identiques. L'écart porte uniquement sur la **gouvernance du
déploiement**.

**Disponible sur Team exactement comme sur Enterprise :**

- Gestion org-wide des plugins via `Organization settings > Plugins`, réservée aux rôles
  **Owner / Primary Owner** (la doc dit « Team **and** Enterprise »).
- Les deux voies de marketplace custom : **upload ZIP** (≤ 50 Mo, 100 plugins) **et sync GitHub**
  via la Claude GitHub App. Le sync n'est pas réservé à Enterprise.
- Les quatre modes de diffusion : *installed by default*, *available for install*, *not available*,
  *required*.
- Le provisioning de skills org-wide, et **Cowork**. Nuance favorable : les sessions cloud Cowork
  sont **activées par défaut** sur Team (désactivées par défaut sur Enterprise).

**Absent sur Team :**

| Fonction | Conséquence |
|---|---|
| **Accès par groupe** aux plugins (Enterprise only) | Un plugin est **tout-ou-rien pour l'org entière**. Pas de pilote sur un sous-ensemble d'utilisateurs. |
| **Rôles custom** | Aucune délégation fine : seul un Owner / Primary Owner peut gérer les plugins. |
| **Activation sélective de Cowork** | Tout-ou-rien également. |
| **Scanning de sécurité des skills et plugins** | Présenté comme une fonction Enterprise — à considérer comme absent. |

**Conséquences pour la mission :**

1. **Le pilote passe par le mode *available for install***, pas par les groupes : publication en
   opt-in, recrutement manuel des testeurs, puis bascule en *installed by default* après
   validation. C'est le seul substitut au rollout progressif.
2. **⚠️ Le repo du marketplace doit être privé ou interne** chez le client : le sync org **refuse
   un repo public**. Notre chemin d'apprentissage (repo public + scope personnel) diverge donc ici.
   À éprouver avant la livraison, pas le jour J.
3. **Pas de scanning automatique** → la revue de sécurité du plugin devra être manuelle et
   formalisée si l'équipe sécurité du client la demande.
4. Identifier **nommément l'Owner** du Claude Team du client dès le cadrage : sans lui, aucune
   installation org-wide n'est possible, et il n'existe aucun rôle intermédiaire à qui déléguer.

## 10. Anti-objectifs

- Aucune `command/` (non consommée en chat ni en Cowork).
- Aucun serveur MCP, aucun connecteur.
- Aucun code d'extraction PDF.
- Aucune dépendance à installer, ni dans le repo ni sur la machine.
- Aucun contenu tiers commité (les PDF restent gitignorés).
- Aucune adresse e-mail dans les fichiers du dépôt public.
