# Appwrite CLI Fix for Windows
# Add this to your PowerShell profile to fix the appwrite command

# Remove the broken alias if it exists
Remove-Item Alias:appwrite -ErrorAction SilentlyContinue

# Create function to call appwrite CLI correctly
function appwrite {
    $appwritePath = "C:\Users\$env:USERNAME\AppData\Roaming\npm\node_modules\appwrite-cli\index.js"
    
    if (Test-Path $appwritePath) {
        node $appwritePath $args
    } else {
        Write-Host "Error: Appwrite CLI not found at $appwritePath" -ForegroundColor Red
        Write-Host "Please reinstall: npm install -g appwrite-cli" -ForegroundColor Yellow
    }
}

Write-Host "Appwrite CLI fix loaded!" -ForegroundColor Green
Write-Host "You can now use 'appwrite' commands normally" -ForegroundColor Cyan
