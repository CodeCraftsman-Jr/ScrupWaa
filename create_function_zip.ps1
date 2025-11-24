# Create Appwrite Function Deployment Package
# Run this script to create function.zip for uploading to Appwrite

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Appwrite Function ZIP Creator" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "function_main.py")) {
    Write-Host "ERROR: function_main.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the ScrupWaa project root directory." -ForegroundColor Yellow
    exit 1
}

# Define files and folders to include
$items = @(
    "function_main.py",
    "universal_search.py",
    "format_results.py",
    "config.py",
    "requirements.txt",
    "models",
    "scrapers",
    "utils"
)

Write-Host "Checking files..." -ForegroundColor Yellow

# Verify all items exist
$missing = @()
foreach ($item in $items) {
    if (-not (Test-Path $item)) {
        $missing += $item
        Write-Host "  X Missing: $item" -ForegroundColor Red
    } else {
        Write-Host "  OK Found: $item" -ForegroundColor Green
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROR: Missing required files!" -ForegroundColor Red
    Write-Host "Please ensure all files are present before creating ZIP." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Creating function.zip..." -ForegroundColor Yellow

# Remove old ZIP if exists
if (Test-Path "function.zip") {
    Remove-Item "function.zip" -Force
    Write-Host "  Removed old function.zip" -ForegroundColor Gray
}

# Create ZIP file
try {
    Compress-Archive -Path $items -DestinationPath "function.zip" -CompressionLevel Optimal -Force
    Write-Host "  ZIP created successfully!" -ForegroundColor Green
} catch {
    Write-Host "  Error creating ZIP: $_" -ForegroundColor Red
    exit 1
}

# Get ZIP file info
$zipInfo = Get-Item "function.zip"
$sizeKB = [math]::Round($zipInfo.Length / 1KB, 2)
$sizeMB = [math]::Round($zipInfo.Length / 1MB, 2)

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "ZIP Package Ready!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "File: function.zip" -ForegroundColor White
Write-Host "Size: $sizeKB KB ($sizeMB MB)" -ForegroundColor White
Write-Host "Location: $($zipInfo.FullName)" -ForegroundColor White
Write-Host ""

# Verify ZIP contents
Write-Host "Verifying ZIP contents..." -ForegroundColor Yellow
$tempDir = "temp_verify_zip"

try {
    # Extract to temporary directory
    Expand-Archive -Path "function.zip" -DestinationPath $tempDir -Force
    
    # List contents
    Write-Host ""
    Write-Host "ZIP Contents:" -ForegroundColor Cyan
    Get-ChildItem $tempDir -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($tempDir.Length + 1)
        if ($_.PSIsContainer) {
            Write-Host "  [DIR]  $relativePath/" -ForegroundColor Blue
        } else {
            $fileSize = [math]::Round($_.Length / 1KB, 1)
            Write-Host "  [FILE] $relativePath ($fileSize KB)" -ForegroundColor Gray
        }
    }
    
    # Cleanup
    Remove-Item $tempDir -Recurse -Force
    
} catch {
    Write-Host "Warning: Could not verify ZIP contents" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://cloud.appwrite.io/console" -ForegroundColor White
Write-Host "2. Navigate to: Functions -> Create Function" -ForegroundColor White
Write-Host "3. Upload: function.zip" -ForegroundColor White
Write-Host "4. Set Runtime: Python 3.11" -ForegroundColor White
Write-Host "5. Set Entrypoint: function_main.py" -ForegroundColor White
Write-Host "6. Set Commands: pip install -r requirements.txt" -ForegroundColor White
Write-Host "7. Set Timeout: 300 seconds" -ForegroundColor White
Write-Host "8. Deploy and wait 3-5 minutes" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see: DEPLOY_VIA_CONSOLE.md" -ForegroundColor Cyan
Write-Host ""
