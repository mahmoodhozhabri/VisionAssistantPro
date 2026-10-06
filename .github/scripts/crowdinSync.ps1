#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

# Git configuration for automated commits
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

$rawAddonId = $env:ADDON_ID
if ([string]::IsNullOrWhiteSpace($rawAddonId)) {
    Write-Error "Failed to get addon ID."
    exit 1
}
$addonId = $rawAddonId.Trim()

# --- STEP 1: PREPARATION AND SOURCE UPDATE ---

$xliffFile = "./$addonId.xliff"
$mdFile = "./readme.md"

if (Test-Path $mdFile) {
    if (Test-Path $xliffFile) {
        $tempXliff = [System.IO.Path]::GetTempFileName()
        try {
            Copy-Item "$addonId.xliff" $tempXliff -Force
            Write-Host "DEBUG: Updating XLIFF source based on readme.md..."
            ./l10nUtil.exe md2xliff $mdFile $xliffFile -o $tempXliff
        }
        finally {
            if (Test-Path $tempXliff) {
                Remove-Item $tempXliff -Force
            }
        }
    }
    else {
        Write-Host "DEBUG: XLIFF template not found. Creating new one from readme.md..."
        ./l10nUtil.exe md2xliff $mdFile $xliffFile
    }
}

# Update POT file (addon interface)
uv run scons pot
$potFile = "$addonId.pot"

# --- STEP 2: UPLOAD SOURCES TO CROWDIN ---

if (Test-Path $potFile) {
    Write-Host "DEBUG: Uploading updated POT source to Crowdin..."
    ./l10nUtil.exe uploadSourceFile "$potFile" -c $env:L10N_UTIL_CONFIG
}

if (Test-Path $mdFile) {
    Write-Host "DEBUG: Uploading updated Markdown source to Crowdin..."
    ./l10nUtil.exe uploadSourceFile "$mdFile" -c $env:L10N_UTIL_CONFIG
}

# --- STEP 3: EXPORT AND PROCESS TRANSLATIONS ---

Write-Host "DEBUG: Exporting translations from Crowdin..."
./l10nUtil.exe exportTranslations -o _addonL10n -c $env:L10N_UTIL_CONFIG

# Ensure base directories exist
New-Item -ItemType Directory -Force -Path addon/locale | Out-Null
New-Item -ItemType Directory -Force -Path addon/doc | Out-Null

# Load language mappings for Crowdin API calls
$languageMappings = Get-Content -Raw ".github/scripts/languageMappings.json" | ConvertFrom-Json

$exportSubdir = "_addonL10n/$addonId"
$baseExportDir = if (Test-Path $exportSubdir) { $exportSubdir } else { "_addonL10n" }

foreach ($dir in Get-ChildItem -Path $baseExportDir -Directory) {

    $crowdinCode = $dir.Name

    if ($crowdinCode -eq "en") {
        continue
    }

    # Reverse mapping: Find repo code from Crowdin code
    $repoLang = $null
    foreach ($prop in $languageMappings.PSObject.Properties) {
        if ($prop.Value -eq $crowdinCode) {
            $repoLang = $prop.Name
            break
        }
    }
    if (-not $repoLang) {
        $repoLang = $crowdinCode.Replace('-', '_')
    }

    $crowdinLang = $crowdinCode

    Write-Host "--- Processing Language: $repoLang (Crowdin: $crowdinLang) ---" -ForegroundColor Cyan

    # Paths

    $remoteMd = Join-Path $dir.FullName "readme.md"

    $remoteXliff = Join-Path $dir.FullName "$addonId.xliff"
    if (-not (Test-Path $remoteXliff)) {
        $candidateXliff = Get-ChildItem -Path $dir.FullName -Filter "*.xliff" | Select-Object -First 1
        if ($candidateXliff) { $remoteXliff = $candidateXliff.FullName }
    }

    $remotePo = Join-Path $dir.FullName "$addonId.po"
    if (-not (Test-Path $remotePo)) {
        $candidatePo = Get-ChildItem -Path $dir.FullName -Filter "*.po" | Select-Object -First 1
        if ($candidatePo) { $remotePo = $candidatePo.FullName }
    }

    $localMdDir = "addon/doc/$repoLang"
    $localMd = "$localMdDir/readme.md"

    $localPoPath = "addon/locale/$repoLang/LC_MESSAGES/nvda.po"

    # --- 3.1 PO FILE PROCESSING ---
    $poImported = $false
    $scorePo = 0.0
    $threshold = $env:MIN_PERCENTAGE_TRANSLATED

    if (Test-Path $remotePo) {

        Write-Host "DEBUG: Evaluating Remote PO score..."

        $res = uv run python .github/scripts/checkTranslation.py "$addonId.po" $crowdinLang

        $match = $res | Select-String "poScore="
        if ($match) {
            $scorePo = [double]($match.ToString().Split("=")[1])
        }

        Write-Host "DEBUG: PO Score -> $scorePo"

        if ($scorePo -ge $threshold) {

            Write-Host "SUCCESS: Remote PO is above threshold. Importing to $localPoPath"

            New-Item -ItemType Directory -Force -Path (Split-Path $localPoPath) | Out-Null

            Copy-Item $remotePo $localPoPath -Force

            $localMoPath = [System.IO.Path]::ChangeExtension($localPoPath, ".mo")
            try {
                msgfmt -o $localMoPath $localPoPath
            }
            catch {
                Write-Host "WARNING: Failed to compile MO file for $repoLang"
            }

            $poImported = $true
        }
        else {

            Write-Host "WARNING: Remote PO score is below threshold ($threshold)."
        }
    }

    if (-not $poImported -and (Test-Path $localPoPath)) {

        Write-Host "ACTION: Uploading local legacy PO to Crowdin ($crowdinLang) as fallback."

        ./l10nUtil.exe uploadTranslationFile $crowdinLang "$addonId.po" $localPoPath -c $env:L10N_UTIL_CONFIG
    }

    # --- 3.2 DOCUMENTATION PROCESSING (MARKDOWN & XLIFF FALLBACK) ---

    $threshold = $env:MIN_PERCENTAGE_TRANSLATED
    $docImported = $false

    if (Test-Path $remoteMd) {
        Write-Host "DEBUG: Evaluating Remote Markdown score..."

        $res = uv run python .github/scripts/checkTranslation.py "readme.md" $crowdinLang

        $scoreMd = 0.0
        $match = $res | Select-String "mdScore="
        if ($match) {
            $scoreMd = [double]($match.ToString().Split("=")[1])
        }

        Write-Host "DEBUG: Markdown Score -> $scoreMd"

        if ($scoreMd -ge $threshold) {
            if (!(Test-Path $localMdDir)) {
                New-Item -ItemType Directory -Force -Path $localMdDir | Out-Null
            }

            Write-Host "SUCCESS: Importing documentation from Markdown ($repoLang)..."
            Copy-Item $remoteMd $localMd -Force
            $docImported = $true
        }
        else {
            Write-Host "WARNING: Remote Markdown score is below threshold ($threshold)."
        }
    }
    elseif (Test-Path $remoteXliff) {
        Write-Host "DEBUG: Evaluating Remote XLIFF score..."

        $res = uv run python .github/scripts/checkTranslation.py "$addonId.xliff" $crowdinLang

        $scoreXliff = 0.0
        $match = $res | Select-String "xliffScore="
        if ($match) {
            $scoreXliff = [double]($match.ToString().Split("=")[1])
        }

        Write-Host "DEBUG: XLIFF Score -> $scoreXliff"

        if ($scoreXliff -ge $threshold) {
            if (!(Test-Path $localMdDir)) {
                New-Item -ItemType Directory -Force -Path $localMdDir | Out-Null
            }

            Write-Host "SUCCESS: Importing documentation from XLIFF ($repoLang)..."
            ./l10nUtil.exe xliff2md $remoteXliff $localMd
            $docImported = $true
        }
        else {
            Write-Host "WARNING: Remote XLIFF score is below threshold ($threshold)."
        }
    }
    else {
        Write-Host "DEBUG: No remote Markdown or XLIFF file found for this language."
    }
}

# --- STEP 4: COMMIT UPDATED TRANSLATIONS ---

git add addon/locale addon/doc

git diff --staged --quiet

if ($LASTEXITCODE -ne 0) {

    git commit -m "Update translations for $addonId from Crowdin (Automatic Sync)"

    Write-Host "SUCCESS: Translations committed."
}
else {

    Write-Host "DEBUG: No changes in translations to commit."
}

# Push all generated commits after successful Crowdin synchronization

$pushOutput = git push 2>&1

$repository = $env:GITHUB_REPOSITORY

Write-Host $pushOutput

if ($LASTEXITCODE -ne 0) {

    Write-Host "ERROR: Failed to push commits to $repository."
}
elseif ($pushOutput -match "Everything up-to-date") {

    Write-Host "INFO: No new commits needed to be pushed."
}
else {

    Write-Host "SUCCESS: New commits successfully pushed to $repository."
}
