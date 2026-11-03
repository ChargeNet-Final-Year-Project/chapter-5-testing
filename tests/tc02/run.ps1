$ErrorActionPreference = 'Stop'
$root = (Resolve-Path "$PSScriptRoot/../..").Path
Set-Location "$root/.work/chargenet-mobile"
Start-Transcript -Path "$PSScriptRoot/mobile-regression.txt" -Force
try {
$flutter = 'C:/Users/ongji/flutter/bin/flutter.bat'
& $flutter --version
& $flutter pub get --enforce-lockfile
Write-Host "dependencies exit: $LASTEXITCODE"
& $flutter analyze
Write-Host "analysis exit: $LASTEXITCODE"
& $flutter test --concurrency=1 --reporter expanded
Write-Host "tests exit: $LASTEXITCODE"
& $flutter build apk --debug --dart-define=API_BASE_URL=http://10.0.2.2:18080
Write-Host "APK build exit: $LASTEXITCODE"
} finally { Stop-Transcript }
