param([switch]$CheckOnly)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

function Info($m) { Write-Host $m }
function Fail($m) {
    Write-Host ""
    Write-Host "[ERROR] $m" -ForegroundColor Red
    Write-Host ""
    exit 1
}

Info "Project: $root"

# ---------- 1. Node / npm ----------
$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) {
    Fail "npm not found. Please install Node.js 18+ from https://nodejs.org/ and reopen this window."
}
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCmd) { Info ("Node:   " + (& node -v 2>$null)) }
Info ("npm:    " + (& npm -v 2>$null))

# ---------- 2. Locate a Python that can import flask ----------
$candidates = New-Object System.Collections.ArrayList
function AddCandidate($p) {
    if ($p -and (Test-Path $p) -and -not $candidates.Contains($p)) { [void]$candidates.Add($p) }
}

if ($env:PYTHON) { AddCandidate $env:PYTHON }
$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) { AddCandidate $py.Source }
Get-ChildItem "C:\Program Files\python*\python.exe" -ErrorAction SilentlyContinue | ForEach-Object { AddCandidate $_.FullName }
Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe" -ErrorAction SilentlyContinue | ForEach-Object { AddCandidate $_.FullName }
Get-ChildItem "$env:USERPROFILE\.workbuddy\binaries\python\versions\*\python.exe" -ErrorAction SilentlyContinue | ForEach-Object { AddCandidate $_.FullName }

$probe = "import importlib.metadata as m, sys; print(m.version('flask')); print(sys.version.split()[0])"
$pythonExe = $null
$flaskInfo = $null
foreach ($c in $candidates) {
    $out = & $c -c $probe 2>$null
    if ($LASTEXITCODE -eq 0 -and $out -and $out.Count -ge 2) {
        $pythonExe = $c
        $flaskInfo = "flask " + $out[0] + " / Python " + $out[1]
        break
    }
}

if (-not $pythonExe) {
    Write-Host ""
    Write-Host "Checked Python candidates:" -ForegroundColor Yellow
    foreach ($c in $candidates) { Write-Host ("  - " + $c) }
    Fail "No Python with Flask found. Install it with: pip install -r backend\requirements.txt"
}

Info ("Python: " + $pythonExe)
Info ("Env:    " + $flaskInfo)

# ---------- 3. Frontend build (only when dist is missing) ----------
$distIndex = Join-Path $root "frontend\dist\index.html"
if (Test-Path $distIndex) {
    Info "Frontend build: found (skip build)"
} else {
    Info "Frontend build: not found, building..."
    Push-Location (Join-Path $root "frontend")
    if (-not (Test-Path "node_modules")) {
        Info "Installing frontend dependencies..."
        & npm install
        if ($LASTEXITCODE -ne 0) { Pop-Location; Fail "npm install failed (exit $LASTEXITCODE)" }
    }
    & npm run build
    $buildCode = $LASTEXITCODE
    Pop-Location
    if ($buildCode -ne 0) { Fail "npm run build failed (exit $buildCode)" }
    Info "Frontend build: done"
}

if ($CheckOnly) {
    Info ""
    Info "Environment looks good."
    exit 0
}

# ---------- 4. Start Flask ----------
if (-not $env:PORT) { $env:PORT = "5000" }
Info ""
Info ("Starting server at http://127.0.0.1:" + $env:PORT)
Info "Press Ctrl+C to stop."
Info ""

Push-Location (Join-Path $root "backend")
& $pythonExe "app.py"
$runCode = $LASTEXITCODE
Pop-Location

if ($runCode -ne 0) { Fail "Server exited with code $runCode" }
exit 0
