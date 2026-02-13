# FastAPI Backend Agent Helper Functions
# This script provides helper functions for backend-related tasks

function Initialize-BackendAgent {
    <#
    .SYNOPSIS
        Initializes the backend agent environment
    .DESCRIPTION
        Sets up the environment for FastAPI backend tasks
    #>
    Write-Host "Initializing FastAPI Backend Agent..." -ForegroundColor Green
    
    # Check if required directories exist
    $backendDir = Join-Path $PSScriptRoot ".."
    $skillsDir = Join-Path $backendDir "skills"
    
    if (-not (Test-Path $backendDir)) {
        Write-Host "Backend directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $backendDir -Force
    }
    
    if (-not (Test-Path $skillsDir)) {
        Write-Host "Backend skills directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $skillsDir -Force
    }
    
    Write-Host "FastAPI Backend Agent initialized successfully!" -ForegroundColor Green
}

function Get-BackendSkills {
    <#
    .SYNOPSIS
        Lists all available backend skills
    .DESCRIPTION
        Retrieves and displays all available backend skills
    #>
    $skillsDir = Join-Path $PSScriptRoot "..\skills"
    $skillFiles = Get-ChildItem -Path $skillsDir -Filter "*.md" -Name
    
    Write-Host "Available Backend Skills:" -ForegroundColor Cyan
    foreach ($skill in $skillFiles) {
        $skillName = $skill -replace '.md', ''
        Write-Host "  - $skillName" -ForegroundColor White
    }
}

function Show-FastAPIStructure {
    <#
    .SYNOPSIS
        Shows recommended FastAPI project structure
    .DESCRIPTION
        Displays the recommended structure for a FastAPI project
    #>
    Write-Host ""
    Write-Host "Recommended FastAPI Project Structure:" -ForegroundColor Cyan
    $structure = @"
    project/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py          # Application entry point
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── v1/
    │   │       ├── __init__.py
    │   │       └── endpoints/
    │   │           ├── __init__.py
    │   │           ├── users.py
    │   │           └── auth.py
    │   ├── models/          # Pydantic models
    │   │   ├── __init__.py
    │   │   └── user.py
    │   ├── schemas/         # Database models
    │   │   ├── __init__.py
    │   │   └── user.py
    │   ├── database/
    │   │   ├── __init__.py
    │   │   └── session.py
    │   └── core/
    │       ├── __init__.py
    │       ├── config.py
    │       └── security.py
    ├── tests/
    ├── requirements.txt
    └── alembic/
"@
    Write-Host $structure -ForegroundColor White
}

function Show-BackendAgentInfo {
    <#
    .SYNOPSIS
        Displays information about the Backend Agent
    .DESCRIPTION
        Shows details about the Backend Agent's purpose and capabilities
    #>
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host "     FastAPI Backend Agent" -ForegroundColor Blue
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Focus: FastAPI backend development, request/response handling, authentication integration, database interaction" -ForegroundColor White
    Write-Host ""
    Write-Host "Capabilities:" -ForegroundColor Cyan
    Write-Host "  - FastAPI routing and request/response validation" -ForegroundColor White
    Write-Host "  - Authentication integration (JWT, OAuth)" -ForegroundColor White
    Write-Host "  - Database integration (SQLAlchemy, async operations)" -ForegroundColor White
    Write-Host "  - Error handling and dependency management" -ForegroundColor White
    Write-Host "  - API optimization and performance tuning" -ForegroundColor White
    Write-Host ""
    Write-Host "Best Practices:" -ForegroundColor Cyan
    Write-Host "  - Follow FastAPI conventions" -ForegroundColor White
    Write-Host "  - Security-first approach" -ForegroundColor White
    Write-Host "  - Production-ready solutions" -ForegroundColor White
    Write-Host ""
}

# Note: Export-ModuleMember can only be used in .psm1 files, not regular .ps1 files
# The functions are available when the script is dot-sourced