# Menu Digest

Plugin de démonstration. Il résume la carte d'un restaurant fournie en PDF, en photo ou en
texte, et propose un accord en trois services. Son contenu métier est volontairement anecdotique :
sa valeur est de servir d'**ossature réutilisable** pour un vrai plugin d'organisation.

## Ce qu'il contient

| Composant | Chemin | Surfaces | Rôle |
|---|---|---|---|
| Skill `menu-summary` | `skills/menu-summary/SKILL.md` | chat + Cowork | Résume une carte selon un format imposé en 5 sections |
| Skill `menu-tasting-plan` | `skills/menu-tasting-plan/SKILL.md` | chat + Cowork | Compose un accord en 3 services avec fourchette de budget |
| Sub-agent `menu-critic` | `agents/menu-critic.md` | **Cowork uniquement** | Relit un résumé produit et signale les écarts au format |

`menu-tasting-plan` illustre la **divulgation progressive** sur trois niveaux : son frontmatter
(~210 tokens, toujours chargé), son corps (~1,3k au déclenchement), puis
`references/pairing-rules.md` et `scripts/price_range.py`, lus ou exécutés seulement en cas de
besoin réel. Le code d'un script n'entre jamais en contexte : seule sa sortie compte.

## Installation

**claude.ai** — `Customize > Plugins > Add marketplace`, coller
`https://github.com/theodore2leusse/plugin-test`, puis installer `Menu Digest`.

**Claude Code** — `/plugin marketplace add theodore2leusse/plugin-test` puis
`/plugin install menu-digest@theodo-lab`.

⚠️ **Une installation est épinglée à la version du moment.** Un `git push` ne propage rien. Pour
récupérer une mise à jour : rafraîchir le marketplace, mettre à jour le plugin, **puis redémarrer**.
En CLI : `claude plugin marketplace update theodo-lab` puis
`claude plugin update menu-digest@theodo-lab`. Le suffixe `@theodo-lab` est **obligatoire**, sans
lui la commande répond « Plugin not found » alors que le plugin est bien installé.

## Utilisation

- Déposer un menu et demander « résume ce menu » → `menu-summary`.
- Déposer un menu et demander « fais-moi un accord entrée-plat-dessert » → `menu-tasting-plan`.
- En Cowork, après un résumé : « fais relire ce résumé par menu-critic, en lui passant le résumé
  et la carte » → `menu-critic`.

## Comment le modifier

### Le déclenchement se joue sur la `description`, pas sur le corps

Si une skill ne se déclenche pas, **le correctif est la `description`**. Ce qui marche, mesuré :
dire ce que fait la skill **et** quand l'utiliser, énumérer les modalités d'entrée (PDF, photo,
capture, texte) et les synonymes de la demande, puis — c'est le point décisif quand deux skills se
ressemblent — ajouter une **clause d'exclusion nommant la skill voisine**. Celle de
`menu-tasting-plan` renvoie explicitement à `menu-summary`, et aucun déclenchement croisé n'a été
observé.

### Pièges qui coûtent du temps

- **Jamais de `: ` dans une valeur de frontmatter.** Un deux-points suivi d'un espace dans un
  scalaire YAML non quoté invalide tout le frontmatter, et la skill devient introuvable **en
  silence**. Ni `claude plugin validate` ni `claude plugin details` ne le signalent.
- **Bumper la version dans les *deux* manifestes**, `.claude-plugin/marketplace.json` **et**
  `plugins/menu-digest/.claude-plugin/plugin.json`. Une version inchangée ne déclenche aucune
  mise à jour côté utilisateur.
- **Ne pas déclarer les champs `skills`, `agents`, `hooks`** dans `plugin.json` : les chemins par
  défaut suffisent, et ces champs **remplacent** le défaut au lieu de s'y ajouter.
- **Un chemin de fichier erroné ne produit aucune erreur** : la skill est simplement absente.
  Vérifier `skills/<nom>/SKILL.md` à la main.
- **`claude plugin details` affiche l'inventaire de la source, pas de la version installée.** Il
  peut annoncer le bon contenu pendant que l'installation en sert un plus ancien.

### Appeler un script depuis une skill

`${CLAUDE_PLUGIN_ROOT}` **n'est pas défini** dans le shell d'une skill sur chat et Cowork : cette
variable relève de la mécanique des *commands*. Un chemin relatif ne marche pas non plus, le
répertoire courant n'étant pas celui de la skill. La forme retenue, en une seule commande :

```bash
SCRIPT="${CLAUDE_PLUGIN_ROOT:-}/skills/menu-tasting-plan/scripts/price_range.py"
[ -f "$SCRIPT" ] || SCRIPT=$(find "$HOME" /sessions -path '*/skills/menu-tasting-plan/scripts/price_range.py' 2>/dev/null | head -1)
echo '{"courses":[...]}' | python3 "$SCRIPT"
```

Un script doit se limiter à la **bibliothèque standard** : aucune installation de paquet n'est
possible dans le sandbox.

### Restreindre les droits d'un sub-agent

Le champ `tools` du frontmatter est le **seul** moyen de restreindre. Une interdiction écrite dans
le corps de l'agent reste une consigne, pas une contrainte : un sub-agent reçoit `Write` et `Edit`
par défaut. Attention aux noms — sur Cowork, `Read`, `Write`, `Edit`, `Glob`, `Grep` existent, mais
**`Bash` n'existe pas** : c'est `mcp__workspace__bash`. Recopier le patron répandu
`tools: Read, Glob, Grep, Bash` n'accorderait donc pas l'accès au shell, et sans erreur visible.

## Limites connues

- Aucune extraction PDF : le plugin repose entièrement sur la lecture native des documents.
- `menu-critic` est invisible en chat, les sub-agents étant réservés à Cowork.
- Le plugin n'embarque aucune `command` : cette mécanique n'est pas consommée en chat ni en Cowork.
- Reste à vérifier qu'une liste `tools` déclarée est réellement **honorée** sur Cowork, et non
  simplement acceptée.
