# Placeholder Reference

## Placeholder → Value (Project → Local)

When syncing templates to local environment, replace these:

| Placeholder | Detection Method | Fallback |
|-------------|-----------------|----------|
| `__NU_PATH__` | `(Get-Command nu.exe).Source`, then `~\AppData\Local\Programs\nu\bin\nu.exe`, then `${env:ProgramFiles}\nu\bin\nu.exe` | `'nu.exe'` (relies on PATH) |
| `__GIT_USR_BIN__` | Find `git.exe` via `Get-Command`, locate parent's `usr\bin`, then check `C:\Program Files\Git\usr\bin` | `C:\Program Files\Git\usr\bin` |
| `__USERNAME__` | `$env:USERNAME` | N/A (always available) |

## Value → Placeholder (Local → Project)

When syncing local environment to templates, detect and replace:

### `.wezterm.lua`

- `config.default_prog = { 'C:\\...\\nu.exe' }` → `config.default_prog = { '__NU_PATH__' }`
- If cross-platform block already exists (with `target_triple` check), keep it and only update `__NU_PATH__`
- If no cross-platform block, wrap in `if wezterm.target_triple == 'x86_64-pc-windows-msvc'` check
- The Shift+Enter keybinding (`SendString '\x1b[13;2u'`) should be preserved as-is

### `env.nu`

- `$env.YAZI_FILE_ONE = "C:\\...\\file.exe"` → `$env.YAZI_FILE_ONE = "__GIT_USR_BIN__\\file.exe"`
- `load-env { http_proxy: "http://127.0.0.1:XXXX", https_proxy: "http://127.0.0.1:XXXX" }` → comment out: `# load-env { http_proxy: "http://127.0.0.1:7890", https_proxy: "http://127.0.0.1:7890" }`
- Starship prompt config (lines 1-3) should be preserved as-is

### `settings.json`

- Extract only the `statusLine` field from local settings.json
- Replace username in the command path: `C:/Users/<USERNAME>/.claude/statusline.ps1` → `C:/Users/__USERNAME__/.claude/statusline.ps1`
- NEVER include `env`, `permissions`, or `model` fields — these contain user secrets

### Files with no placeholders (copy directly)

- `config.nu` — contains `alias cc = claude` and yazi wrapper. Copy as-is both directions.
- `starship.toml` — Pastel Powerline preset. Copy as-is both directions.
- `statusline.ps1` — Full script. Copy as-is both directions.

## Nu.exe Path — Double Backslash Rule

Nushell and Lua both treat `\` as escape character. When writing paths:
- **Lua** (`config.default_prog`): `C:\\Users\\...` (double backslash in Lua string literal)
- **Nushell** (`$env.YAZI_FILE_ONE`): `C:\\Program Files\\...` (double backslash in Nushell string)

The install script does this via `$path -replace '\\', '\\'`. Same approach in sync.
