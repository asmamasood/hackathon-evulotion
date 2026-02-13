# Frontend Agent Helper Functions
# This script provides helper functions for frontend-related tasks

function Initialize-FrontendAgent {
    <#
    .SYNOPSIS
        Initializes the frontend agent environment
    .DESCRIPTION
        Sets up the environment for Next.js frontend tasks
    #>
    Write-Host "Initializing Frontend Agent..." -ForegroundColor Green

    # Check if required directories exist
    $frontendDir = Join-Path $PSScriptRoot ".."
    $skillsDir = Join-Path $frontendDir "skills"

    if (-not (Test-Path $frontendDir)) {
        Write-Host "Frontend directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $frontendDir -Force
    }

    if (-not (Test-Path $skillsDir)) {
        Write-Host "Frontend skills directory not found. Creating..." -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $skillsDir -Force
    }

    Write-Host "Frontend Agent initialized successfully!" -ForegroundColor Green
}

function Get-FrontendSkills {
    <#
    .SYNOPSIS
        Lists all available frontend skills
    .DESCRIPTION
        Retrieves and displays all available frontend skills
    #>
    $skillsDir = Join-Path $PSScriptRoot "..\skills"
    $skillFiles = Get-ChildItem -Path $skillsDir -Filter "*.md" -Name

    Write-Host "Available Frontend Skills:" -ForegroundColor Cyan
    foreach ($skill in $skillFiles) {
        $skillName = $skill -replace '.md', ''
        Write-Host "  - $skillName" -ForegroundColor White
    }
}

function Show-NextJSStructure {
    <#
    .SYNOPSIS
        Shows recommended Next.js project structure
    .DESCRIPTION
        Displays the recommended structure for a Next.js project with App Router
    #>
    Write-Host ""
    Write-Host "Recommended Next.js App Router Project Structure:" -ForegroundColor Cyan
    
    $structure = @"
    my-app/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx
    │   ├── globals.css
    │   ├── loading.tsx
    │   ├── error.tsx
    │   ├── not-found.tsx
    │   ├── api/
    │   │   └── route.ts
    │   ├── dashboard/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx
    │   │   └── [userId]/
    │   │       └── page.tsx
    │   └── blog/
    │       ├── page.tsx
    │       └── [slug]/
    │           └── page.tsx
    ├── components/
    │   ├── ui/
    │   │   ├── button.tsx
    │   │   └── card.tsx
    │   └── navigation/
    │       └── navbar.tsx
    ├── lib/
    │   └── utils.ts
    ├── public/
    │   ├── favicon.ico
    │   └── vercel.svg
    ├── styles/
    │   └── globals.css
    ├── types/
    │   └── index.ts
    ├── next.config.js
    ├── tsconfig.json
    └── package.json


"@

    Write-Host $structure -ForegroundColor White
}

function Show-FrontendAgentInfo {
    <#
    .SYNOPSIS
        Displays information about the Frontend Agent
    .DESCRIPTION
        Shows details about the Frontend Agent's purpose and capabilities
    #>
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host "     Frontend Agent - Responsive UI with Next.js App Router" -ForegroundColor Blue
    Write-Host "===========================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Focus: Building responsive, scalable, and well-structured frontend applications using Next.js App Router" -ForegroundColor White
    Write-Host ""
    Write-Host "Capabilities:" -ForegroundColor Cyan
    Write-Host "  - Next.js App Router implementation" -ForegroundColor White
    Write-Host "  - Responsive UI design" -ForegroundColor White
    Write-Host "  - Data schema design for frontend-backend integration" -ForegroundColor White
    Write-Host "  - Component architecture and modular design" -ForegroundColor White
    Write-Host "  - Performance optimization" -ForegroundColor White
    Write-Host ""
    Write-Host "Best Practices:" -ForegroundColor Cyan
    Write-Host "  - Follow Next.js conventions" -ForegroundColor White
    Write-Host "  - Responsive design principles" -ForegroundColor White
    Write-Host "  - Accessibility compliance" -ForegroundColor White
    Write-Host ""
}

# Note: Export-ModuleMember can only be used in .psm1 files, not regular .ps1 files
# The functions are available when the script is dot-sourced