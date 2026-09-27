<#
.SYNOPSIS
    Automates syncing a local KiCad project to a GitHub repository.
#>

$RepoName = Read-Host "Enter your GitHub repository name (e.g., my-kicad-board)"
$GithubUser = Read-Host "Enter your GitHub username"
$CommitMsg = Read-Host "Enter commit message [default: Update KiCad project]"

if ([string]::IsNullOrWhiteSpace($CommitMsg)) {
    $CommitMsg = "Update KiCad project"
}

Write-Host "`n[1/5] Creating KiCad .gitignore file..." -ForegroundColor Cyan
$GitIgnoreContent = @'
# KiCad specific files
*.kicad_sch~
*.kicad_pcb~
*-bak
*.pro~
*_cache.lib
*-_cache.dcm
fp-lib-table.bak
sym-lib-table.bak

# OS and backup files
.DS_Store
Thumbs.db
*.bak
*.tmp
'@

Set-Content -Path ".gitignore" -Value $GitIgnoreContent

Write-Host "[2/5] Initializing local Git repository..." -ForegroundColor Cyan
if (!(Test-Path ".git")) {
    git init
} else {
    Write-Host "Git repository already initialized." -ForegroundColor Yellow
}

Write-Host "[3/5] Adding files and committing..." -ForegroundColor Cyan
git add .
git commit -m "$CommitMsg"

Write-Host "[4/5] Setting main branch..." -ForegroundColor Cyan
git branch -M main

$RemoteUrl = "https://github.com/$GithubUser/$RepoName.git"
Write-Host "[5/5] Connecting to GitHub ($RemoteUrl) and pushing..." -ForegroundColor Cyan

# Check if remote already exists, update if it does
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    git remote set-url origin $RemoteUrl
} else {
    git remote add origin $RemoteUrl
}

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuccessfully synced to GitHub!" -ForegroundColor Green
} else {
    Write-Host "`nPush failed. Make sure you created the empty repository on GitHub first!" -ForegroundColor Red
}