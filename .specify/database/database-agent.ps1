# Database Agent Main Script
# Entry point for the Neon PostgreSQL specialist agent

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("info", "skills", "init", "structure")]
    [string]$Command = "info"
)

# Import helper functions
$scriptPath = Join-Path $PSScriptRoot "scripts\database-agent-functions.ps1"
if (Test-Path $scriptPath) {
    . $scriptPath
} else {
    Write-Error "Database agent functions not found at $scriptPath"
    exit 1
}

# Initialize the database agent
Initialize-DatabaseAgent

switch ($Command) {
    "info" {
        Show-DatabaseAgentInfo
        Get-DatabaseSkills
    }
    
    "skills" {
        Get-DatabaseSkills
    }
    
    "init" {
        Write-Host "Database Agent already initialized." -ForegroundColor Green
    }
    
    "structure" {
        Show-NeonPostgreSQLStructure
    }
}

Write-Host ""
Write-Host "Database Agent ready for database management tasks!" -ForegroundColor Green