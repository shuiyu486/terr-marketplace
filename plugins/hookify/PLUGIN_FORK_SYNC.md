# Hookify fork sync ledger

## Upstream

- Repository: https://github.com/anthropics/claude-plugins-official
- Upstream path: `plugins/hookify`
- Local fork path: `plugins/hookify`

## Local fork intent

This fork keeps the official Hookify plugin behavior while preserving Windows compatibility fixes for UTF-8 hook input/output and rule-file loading.

## Preserve local changes

Keep these local differences when syncing from upstream:

- `.claude-plugin/plugin.json`
  - Keep `version` managed by `terr-marketplace`.
  - Keep `author.name` as `terrapin`.
  - Keep the description note about the Windows encoding fixes.
- `core/config_loader.py`
  - Keep explicit `encoding='utf-8'` when reading `.claude/hookify.*.local.md` rule files.
- `hooks/pretooluse.py`
- `hooks/posttooluse.py`
- `hooks/stop.py`
- `hooks/userpromptsubmit.py`
  - Keep stdin/stdout UTF-8 reconfiguration.
  - Keep raw stdin reading with `json.loads`.
  - Keep JSON parse debug dump handling for malformed hook input.

## Follow upstream

Use upstream as the source of truth for files and behavior not listed above. In particular:

- `hooks/hooks.json` should follow upstream command quoting.
- Documentation, commands, examples, agents, matchers, and utils should follow upstream unless a future local change is intentionally recorded here.

## Sync workflow

1. Compare upstream `plugins/hookify` against this local plugin directory.
2. Apply upstream changes except where they conflict with the preserved local changes above.
3. If a new local customization is added, record it in this ledger in the same change.
4. Validate from the marketplace root with `claude plugin validate .`.
