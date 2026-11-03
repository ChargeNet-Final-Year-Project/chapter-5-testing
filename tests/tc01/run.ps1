$ErrorActionPreference = 'Stop'
$root = (Resolve-Path "$PSScriptRoot/../..").Path
Set-Location "$root/.work/chargenet-backend"
Start-Transcript -Path "$PSScriptRoot/backend-regression.txt" -Force
try {
$env:GOCACHE = "$root/.cache/go-build"
$env:GOPATH = "$root/.cache/go"
$env:TEST_DATABASE_URL = 'postgres://chargenet:Chapter5LocalOnly@localhost:55432/chargenet_test?sslmode=disable'
go version
go test -v -count=1 -p 1 ./...
Write-Host "go test exit: $LASTEXITCODE"
go vet ./...
Write-Host "go vet exit: $LASTEXITCODE"
go build ./...
Write-Host "go build exit: $LASTEXITCODE"
} finally { Stop-Transcript }
