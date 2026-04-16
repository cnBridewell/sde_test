$ErrorActionPreference = "Stop"

# This script runs Spark + Delta locally in Docker so host Java is not required.
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$packRoot = (Resolve-Path (Join-Path $scriptDir "..\.." )).Path
$dockerDir = Join-Path $packRoot "docker"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker was not found. Install Docker Desktop and rerun this script."
}

Push-Location $dockerDir
try {
    Write-Host "[1/3] Building Docker image with PySpark + Delta dependencies"
    & docker compose build spark-local
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Initial build failed; retrying with BuildKit disabled for compatibility..."
        $env:DOCKER_BUILDKIT = "0"
        & docker compose build spark-local
        if ($LASTEXITCODE -ne 0) {
            throw "Docker image build failed. Ensure Docker Desktop is running and retry."
        }
    }

    Write-Host "[2/3] Running Delta smoke test in container"
    & docker compose run --rm spark-local python starter/databricks/local_delta_smoke_test.py
    if ($LASTEXITCODE -ne 0) {
        throw "Delta smoke test failed in Docker runtime."
    }

    Write-Host "[3/3] Docker Spark runtime is ready"
    Write-Host "Run your pipeline in the same container context with:"
    Write-Host "  docker compose run --rm spark-local python <your_pipeline_entrypoint.py>"
}
finally {
    Pop-Location
}
