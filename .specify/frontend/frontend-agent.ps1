# Frontend Agent Main Script
# Entry point for the Next.js frontend specialist agent

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("info", "skills", "init", "structure")]
    [string]$Command = "info"
)

# Import helper functions
$scriptPath = Join-Path $PSScriptRoot "scripts\frontend-agent-functions.ps1"
if (Test-Path $scriptPath) {
    . $scriptPath
} else {
    Write-Error "Frontend agent functions not found at $scriptPath"
    exit 1
}

# Initialize the frontend agent
Initialize-FrontendAgent

switch ($Command) {
    "info" {
        Show-FrontendAgentInfo
        Get-FrontendSkills
    }
    
    "skills" {
        Get-FrontendSkills
    }
    
    "init" {
        Write-Host "Frontend Agent already initialized." -ForegroundColor Green
    }
    
    "structure" {
        Show-NextJSStructure
    }
}

Write-Host ""
Write-Host "Frontend Agent ready for frontend development tasks!" -ForegroundColor Green