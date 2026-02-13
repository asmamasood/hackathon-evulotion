# Database Agent Helper Functions
# This script provides helper functions for database-related tasks

function Initialize-DatabaseAgent {
    <#
    .SYNOPSIS
        Initializes the database agent environment
    .DESCRIPTION
        Sets up the environment for Neon PostgreSQL tasks
    #>
    Write-Host "Initializing Database Agent..." -ForegroundColor Green
    
    # Check if required directories exist
    $databaseDir = Join-Path $PSScriptRoot ".."
    $skillsDir = Join-Path $databaseDir "skills"
    
    if (-not (Test-Path $databaseDir)) {
        Write-Host "Database directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $databaseDir -Force
    }
    
    if (-not (Test-Path $skillsDir)) {
        Write-Host "Database skills directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $skillsDir -Force
    }
    
    Write-Host "Database Agent initialized successfully!" -ForegroundColor Green
}

function Get-DatabaseSkills {
    <#
    .SYNOPSIS
        Lists all available database skills
    .DESCRIPTION
        Retrieves and displays all available database skills
    #>
    $skillsDir = Join-Path $PSScriptRoot "..\skills"
    $skillFiles = Get-ChildItem -Path $skillsDir -Filter "*.md" -Name
    
    Write-Host "Available Database Skills:" -ForegroundColor Cyan
    foreach ($skill in $skillFiles) {
        $skillName = $skill -replace '.md', ''
        Write-Host "  - $skillName" -ForegroundColor White
    }
}

function Show-NeonPostgreSQLStructure {
    <#
    .SYNOPSIS
        Shows recommended Neon PostgreSQL project structure
    .DESCRIPTION
        Displays the recommended structure for Neon PostgreSQL database management
    #>
    $structure = @"
Recommended Neon PostgreSQL Project Structure:
.
├── migrations/
│   ├── 001_initial_schema.sql
│   ├── 002_add_user_preferences.sql
│   └── 003_create_indexes.sql
├── schemas/
│   ├── users.sql
│   ├── todos.sql
│   └── categories.sql
├── queries/
│   ├── user_queries.sql
│   ├── todo_queries.sql
│   └── reports.sql
├── scripts/
│   ├── seed_data.sql
│   └── backup.sql
├── config/
│   └── database.yml
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
└── docs/
    └── schema_documentation.md

Neon-Specific Configuration:
- Branch management for development/staging/production
- Connection pooling settings
- Serverless compute configuration
- Analytics and monitoring setup

"@
    Write-Host $structure -ForegroundColor White
}

function Show-DatabaseAgentInfo {
    <#
    .SYNOPSIS
        Displays information about the Database Agent
    .DESCRIPTION
        Shows details about the Database Agent's purpose and capabilities
    #>
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host "     Database Agent - Neon Serverless PostgreSQL Management" -ForegroundColor Blue
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Focus: Database management and optimization for Neon Serverless PostgreSQL" -ForegroundColor White
    Write-Host ""
    Write-Host "Capabilities:" -ForegroundColor Cyan
    Write-Host "  - Schema design for scalability and maintainability" -ForegroundColor White
    Write-Host "  - Safe and effective migration management" -ForegroundColor White
    Write-Host "  - Query optimization and indexing" -ForegroundColor White
    Write-Host "  - Neon Serverless PostgreSQL integration" -ForegroundColor White
    Write-Host "  - Performance tuning and monitoring" -ForegroundColor White
    Write-Host ""
    Write-Host "Best Practices:" -ForegroundColor Cyan
    Write-Host "  - Follow PostgreSQL conventions" -ForegroundColor White
    Write-Host "  - Neon Serverless optimization" -ForegroundColor White
    Write-Host "  - Data integrity and security" -ForegroundColor White
    Write-Host ""
}

# Note: Export-ModuleMember can only be used in .psm1 files, not regular .ps1 files
# The functions are available when the script is dot-sourced