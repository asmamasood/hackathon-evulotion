# Auth Agent Main Script
# Entry point for the authentication specialist agent

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("info", "skills", "init", "hash-password")]
    [string]$Command = "info",
    
    [Parameter(Mandatory=$false)]
    [string]$Password
)

# Import helper functions
$scriptPath = Join-Path $PSScriptRoot "scripts\auth-agent-functions.ps1"
if (Test-Path $scriptPath) {
    . $scriptPath
} else {
    Write-Error "Auth agent functions not found at $scriptPath"
    exit 1
}

# Initialize the auth agent
Initialize-AuthAgent

switch ($Command) {
    "info" {
        Show-AuthAgentInfo
        Get-AuthSkills
    }
    
    "skills" {
        Get-AuthSkills
    }
    
    "init" {
        Write-Host "Auth Agent already initialized." -ForegroundColor Green
    }
    
    "hash-password" {
        if (-not $Password) {
            Write-Host "Error: -Password parameter is required for hash-password command" -ForegroundColor Red
            Write-Host "Usage: .\auth-agent.ps1 -Command hash-password -Password 'your_password'" -ForegroundColor Yellow
            exit 1
        }
        
        Invoke-PasswordHashing -Password $Password
    }
}

Write-Host ""
Write-Host "Auth Agent ready for authentication tasks!" -ForegroundColor Green