# Builds the release zip into dist\PaleSpectrumAccess.zip.
# Usage (from the repo root):
#   powershell -ExecutionPolicy Bypass -File scripts\package-release.ps1
# The zip mirrors the game folder: prism.dll and prism_licenses go next to
# "Pale Spectrum.exe", and the .rpy files go into the game subfolder.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$files = @(
    "game\zz_ps_a11y_core.rpy",
    "game\zz_ps_a11y_screens.rpy",
    "game\zz_ps_a11y_descriptions.rpy",
    "prism.dll",
    "prism_licenses",
    "README.md",
    "CHANGELOG.md"
)

$dist = Join-Path $root "dist"
New-Item -ItemType Directory -Path $dist -Force | Out-Null
$zip = Join-Path $dist "PaleSpectrumAccess.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }

# Write entries with forward slashes (Windows PowerShell's ZipFile writes backslashes).
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [System.IO.Compression.ZipFile]::Open($zip, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($entry in $files) {
        $source = Join-Path $root $entry
        if (-not (Test-Path $source)) { throw "Missing release file: $source" }
        $items = if ((Get-Item $source).PSIsContainer) { Get-ChildItem $source -Recurse -File } else { @(Get-Item $source) }
        foreach ($item in $items) {
            $name = $item.FullName.Substring($root.Length + 1).Replace([char]92, [char]47)
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $item.FullName, $name) | Out-Null
        }
    }
} finally {
    $archive.Dispose()
}
Write-Host "Built: $zip"
