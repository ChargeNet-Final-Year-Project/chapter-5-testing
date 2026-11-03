$ErrorActionPreference = 'Stop'
$root = (Resolve-Path "$PSScriptRoot/../..").Path
Set-Location "$root/.work/chargenet-portal"
Start-Transcript -Path "$PSScriptRoot/portal-build.txt" -Force
try {
npm.cmd ci --cache "$root/.cache/npm"
Write-Host "dependencies exit: $LASTEXITCODE"
npm.cmd run typecheck
Write-Host "typecheck exit: $LASTEXITCODE"
npm.cmd run build
Write-Host "build exit: $LASTEXITCODE"
} finally { Stop-Transcript }
