# Auth Agent Helper Functions
# This script provides helper functions for authentication-related tasks

function Initialize-AuthAgent {
    <#
    .SYNOPSIS
        Initializes the auth agent environment
    .DESCRIPTION
        Sets up the environment for authentication-related tasks
    #>
    Write-Host "Initializing Auth Agent..." -ForegroundColor Green

    # Check if required directories exist
    $authDir = Join-Path $PSScriptRoot ".."
    $skillsDir = Join-Path $authDir "skills"

    if (-not (Test-Path $authDir)) {
        Write-Host "Auth directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $authDir -Force
    }

    if (-not (Test-Path $skillsDir)) {
        Write-Host "Auth skills directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $skillsDir -Force
    }

    Write-Host "Auth Agent initialized successfully!" -ForegroundColor Green
}

function Get-AuthSkills {
    <#
    .SYNOPSIS
        Lists all available auth skills
    .DESCRIPTION
        Retrieves and displays all available authentication skills
    #>
    $skillsDir = Join-Path $PSScriptRoot "..\skills"
    $skillFiles = Get-ChildItem -Path $skillsDir -Filter "*.md" -Name

    Write-Host "Available Auth Skills:" -ForegroundColor Cyan
    foreach ($skill in $skillFiles) {
        $skillName = $skill -replace '.md', ''
        Write-Host "  - $skillName" -ForegroundColor White
    }
}

function Invoke-PasswordHashing {
    <#
    .SYNOPSIS
        Demonstrates password hashing functionality
    .DESCRIPTION
        Shows how to properly hash passwords using secure methods
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Password
    )

    Write-Host "Hashing password securely..." -ForegroundColor Yellow
    # In a real implementation, this would use bcrypt or argon2
    # For demonstration purposes, we'll show the concept
    Write-Host "Password hashing would use bcrypt/argon2 with proper salting" -ForegroundColor Green
    Write-Host "Input: $($Password.Length) characters" -ForegroundColor Gray
}

function Show-AuthAgentInfo {
    <#
    .SYNOPSIS
        Displays information about the Auth Agent
    .DESCRIPTION
        Shows details about the Auth Agent's purpose and capabilities
    #>
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host "     Auth Agent - Secure Authentication Specialist" -ForegroundColor Blue
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Focus: Secure user authentication and authorization" -ForegroundColor White
    Write-Host ""
    Write-Host "Capabilities:" -ForegroundColor Cyan
    Write-Host "  - Secure signup/signin flows" -ForegroundColor White
    Write-Host "  - Password hashing and verification" -ForegroundColor White
    Write-Host "  - JWT token management" -ForegroundColor White
    Write-Host "  - Session management" -ForegroundColor White
    Write-Host "  - OAuth integration" -ForegroundColor White
    Write-Host "  - Role-based access control" -ForegroundColor White
    Write-Host ""
    Write-Host "Security Standards:" -ForegroundColor Cyan
    Write-Host "  - OWASP Top 10 compliance" -ForegroundColor White
    Write-Host "  - Industry best practices" -ForegroundColor White
    Write-Host "  - Production-ready security" -ForegroundColor White
    Write-Host ""
}

# Note: Export-ModuleMember can only be used in .psm1 files, not regular .ps1 files
# The functions are available when the script is dot-sourced