param(
  [string]$SkillRoot = $(if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' })
)
$ErrorActionPreference = 'Stop'
$source = (Resolve-Path (Join-Path $PSScriptRoot '.')).Path
$destination = Join-Path $SkillRoot 'project-manager-49'
New-Item -ItemType Directory -Force -Path $SkillRoot | Out-Null
if (Test-Path -LiteralPath $destination) {
  Write-Host "Updating existing Skill at $destination"
}
New-Item -ItemType Directory -Force -Path $destination | Out-Null
Copy-Item -Recurse -Force -Path (Join-Path $source '*') -Destination $destination
Write-Host "Installed project-manager-49 to $destination"
