# FastAPI Backend Agent Main Script
# Entry point for the FastAPI backend specialist agent

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("info", "skills", "init", "structure")]
    [string]$Command = "info"
)

# Import helper functions
$scriptPath = Join-Path $PSScriptRoot "scripts\backend-agent-functions.ps1"
if (Test-Path $scriptPath) {
    . $scriptPath
} else {
    Write-Error "Backend agent functions not found at $scriptPath"
    exit 1
}

# Initialize the backend agent
Initialize-BackendAgent

switch ($Command) {
    "info" {
        Show-BackendAgentInfo
        Get-BackendSkills
    }
    
    "skills" {
        Get-BackendSkills
    }
    
    "init" {
        Write-Host "Backend Agent already initialized." -ForegroundColor Green
    }
    
    "structure" {
        Show-FastAPIStructure
    }
}

Write-Host ""
Write-Host "FastAPI Backend Agent ready for backend development tasks!" -ForegroundColor Green