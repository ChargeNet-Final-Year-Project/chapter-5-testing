$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$env:GOCACHE = "$root/.cache/go-build"
$env:GOPATH = "$root/.cache/go"
$env:DATABASE_URL = 'postgres://chargenet:Chapter5LocalOnly@localhost:55432/chargenet_evidence_test?sslmode=disable'
$env:JWT_SECRET = 'chapter-five-disposable-local-secret'
$env:GATEWAY = 'ocpi'
$env:PORT = '18080'
$env:PUBLIC_BASE_URL = 'http://localhost:18080'
$env:PORTAL_ORIGIN = 'http://localhost:15173'
$env:SIM_TIME_SCALE = '10'
$env:PLATFORM_FEE_PCT = '5'
$env:MIN_START_BALANCE = '10'
$env:FX_RATE_SOURCE = ''
$env:VITE_API_BASE_URL = 'http://localhost:18080'
New-Item -ItemType Directory "$root/.runtime" -Force | Out-Null
Set-Location "$root/.work/chargenet-backend"
go build -o "$root/.runtime/server.exe" ./cmd/server
if ($LASTEXITCODE -ne 0) { throw 'Backend build failed' }
$backend = Start-Process -FilePath "$root/.runtime/server.exe" -WorkingDirectory "$root/.work/chargenet-backend" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/.runtime/backend.stdout.txt" -RedirectStandardError "$root/.runtime/backend.stderr.txt"
$portal = Start-Process -FilePath (Get-Command node).Source -ArgumentList 'node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','15173','--strictPort' -WorkingDirectory "$root/.work/chargenet-portal" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/.runtime/portal.stdout.txt" -RedirectStandardError "$root/.runtime/portal.stderr.txt"
Write-Host "Backend PID $($backend.Id); portal PID $($portal.Id)"
Write-Host 'Stop these two processes when finished. PostgreSQL container: chargenet-ch5-new-postgres.'
