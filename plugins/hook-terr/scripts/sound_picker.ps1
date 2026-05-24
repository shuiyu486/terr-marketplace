$sounds = @(
    @{ Id = 1; Alias = 'tada'; Path = 'C:\Windows\Media\tada.wav'; Description = 'recommended default' },
    @{ Id = 2; Alias = 'notify'; Path = 'C:\Windows\Media\notify.wav'; Description = 'short classic notification' },
    @{ Id = 3; Alias = 'windows-notify'; Path = 'C:\Windows\Media\Windows Notify System Generic.wav'; Description = 'Windows notification style' },
    @{ Id = 4; Alias = 'windows-ding'; Path = 'C:\Windows\Media\Windows Ding.wav'; Description = 'short ding' },
    @{ Id = 5; Alias = 'chimes'; Path = 'C:\Windows\Media\chimes.wav'; Description = 'classic chimes' },
    @{ Id = 6; Alias = 'ding'; Path = 'C:\Windows\Media\ding.wav'; Description = 'classic ding' },
    @{ Id = 7; Alias = 'chord'; Path = 'C:\Windows\Media\chord.wav'; Description = 'classic chord' },
    @{ Id = 8; Alias = 'windows-balloon'; Path = 'C:\Windows\Media\Windows Balloon.wav'; Description = 'Windows balloon' },
    @{ Id = 9; Alias = 'windows-default'; Path = 'C:\Windows\Media\Windows Default.wav'; Description = 'Windows default' },
    @{ Id = 10; Alias = 'windows-exclamation'; Path = 'C:\Windows\Media\Windows Exclamation.wav'; Description = 'Windows exclamation' },
    @{ Id = 11; Alias = 'windows-foreground'; Path = 'C:\Windows\Media\Windows Foreground.wav'; Description = 'Windows foreground' },
    @{ Id = 12; Alias = 'windows-message-nudge'; Path = 'C:\Windows\Media\Windows Message Nudge.wav'; Description = 'Windows message nudge' },
    @{ Id = 13; Alias = 'alarm01'; Path = 'C:\Windows\Media\Alarm01.wav'; Description = 'alarm 01' },
    @{ Id = 14; Alias = 'alarm02'; Path = 'C:\Windows\Media\Alarm02.wav'; Description = 'alarm 02' },
    @{ Id = 15; Alias = 'ring01'; Path = 'C:\Windows\Media\Ring01.wav'; Description = 'ring 01' },
    @{ Id = 16; Alias = 'windows-error'; Path = 'C:\Windows\Media\Windows Error.wav'; Description = 'Windows error' }
)

function Show-Sounds {
    Write-Host ''
    Write-Host 'hook-terr sound picker'
    Write-Host 'Enter an id or alias to preview. Enter s <id|alias> to select. Enter q to quit.'
    Write-Host ''
    foreach ($sound in $sounds) {
        $status = if (Test-Path -LiteralPath $sound.Path) { 'ok' } else { 'missing' }
        Write-Host ("{0,2}. {1,-22} [{2}] {3}" -f $sound.Id, $sound.Alias, $status, $sound.Path)
    }
    Write-Host ''
}

function Find-Sound([string] $Value) {
    $normalized = $Value.Trim().ToLowerInvariant()
    foreach ($sound in $sounds) {
        if ([string]$sound.Id -eq $normalized -or $sound.Alias.ToLowerInvariant() -eq $normalized) {
            return $sound
        }
    }
    return $null
}

function Play-Sound($Sound) {
    if (-not (Test-Path -LiteralPath $Sound.Path)) {
        Write-Host "Missing wav file: $($Sound.Path)"
        return
    }
    $player = New-Object System.Media.SoundPlayer $Sound.Path
    $player.Load()
    $player.PlaySync()
}

Show-Sounds
while ($true) {
    $inputValue = Read-Host 'preview id/alias, select with s id/alias, or q'
    if (-not $inputValue) { continue }
    $trimmed = $inputValue.Trim()
    if ($trimmed.ToLowerInvariant() -eq 'q') { exit 0 }

    if ($trimmed -match '^s\s+(.+)$') {
        $selected = Find-Sound $Matches[1]
        if ($null -eq $selected) {
            Write-Host "Unknown sound: $($Matches[1])"
            continue
        }
        if (-not (Test-Path -LiteralPath $selected.Path)) {
            Write-Host "Cannot select missing wav file: $($selected.Path)"
            continue
        }
        Write-Host ''
        Write-Host 'Selected sound:'
        Write-Host "  id: $($selected.Id)"
        Write-Host "  alias: $($selected.Alias)"
        Write-Host "  wavPath: $($selected.Path)"
        exit 0
    }

    $sound = Find-Sound $trimmed
    if ($null -eq $sound) {
        Write-Host "Unknown sound: $trimmed"
        continue
    }
    Play-Sound $sound
}
