# Module 00: Environment & Tooling Verification Script (PowerShell)
# Run this script to verify your development toolchain.

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       PYTHON MASTERY: TOOLCHAIN VERIFICATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

function Check-Tool {
    param (
        [string]$ToolName,
        [string]$Command,
        [string]$InstallTip
    )

    Write-Host -NoNewline "[Checking] $ToolName ... "
    try {
        $output = Invoke-Expression $Command 2>$null
        if ($LASTEXITCODE -eq 0 -or $output) {
            Write-Host "INSTALLED" -ForegroundColor Green
            Write-Host "           $($output.Split([Environment]::NewLine)[0])" -ForegroundColor DarkGray
            return $true
        } else {
            Write-Host "NOT FOUND" -ForegroundColor Yellow
            Write-Host "           Tip: $InstallTip" -ForegroundColor DarkYellow
            return $false
        }
    } catch {
        Write-Host "NOT FOUND" -ForegroundColor Yellow
        Write-Host "           Tip: $InstallTip" -ForegroundColor DarkYellow
        return $false
    }
}

$pyCheck = Check-Tool -ToolName "Python" -Command "python --version" -InstallTip "Download from https://python.org or install via uv."
$gitCheck = Check-Tool -ToolName "Git" -Command "git --version" -InstallTip "Download from https://git-scm.com."
$uvCheck = Check-Tool -ToolName "uv (Fast Package Manager)" -Command "uv --version" -InstallTip "Install via: powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`""
$ruffCheck = Check-Tool -ToolName "Ruff (Linter & Formatter)" -Command "ruff --version" -InstallTip "Install via: uv tool install ruff (or pip install ruff)"

Write-Host "`n------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "Running Python Diagnostics Script..." -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Cyan

if ($pyCheck) {
    python "01_environment_diagnostics.py"
} else {
    Write-Host "Skipping diagnostics because Python was not found in PATH." -ForegroundColor Red
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Verification Finished!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
