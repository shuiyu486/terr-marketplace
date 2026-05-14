# Paths Reference

## Local Environment Paths (Windows)

| Config | Absolute Path |
|--------|--------------|
| WezTerm | `$env:USERPROFILE\.wezterm.lua` |
| Nushell config | `$env:APPDATA\nushell\config.nu` (i.e., `~\AppData\Roaming\nushell\config.nu`) |
| Nushell env | `$env:APPDATA\nushell\env.nu` |
| Starship | `$env:USERPROFILE\.config\starship.toml` |
| Claude statusline | `$env:USERPROFILE\.claude\statusline.ps1` |
| Claude settings | `$env:USERPROFILE\.claude\settings.json` |

## ccNovaTerm Project Template Paths

All under `<repo-root>/config/`:

| Template | File |
|----------|------|
| WezTerm | `config/.wezterm.lua` |
| Nushell config | `config/config.nu` |
| Nushell env | `config/env.nu` |
| Starship | `config/starship.toml` |
| Claude statusline | `config/statusline.ps1` |
| Claude settings | `config/settings.json` |

## Finding ccNovaTerm Repo Root

Check these locations in order:
1. Current working directory (if it contains `config/.wezterm.lua`)
2. `$env:USERPROFILE\ccNovaTerm\`
3. Ask user to provide the path

## Backup Directory

`$env:USERPROFILE\ccNovaTerm-backup\<yyyyMMdd_HHmmss>\`

## Cache Directory (statusline runtime)

`$env:TEMP\ccNovaTerm-statusline-cache\ses-{PID}.txt`
