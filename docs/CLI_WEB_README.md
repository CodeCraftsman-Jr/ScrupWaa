# Universal Mobile Phone Scraper - CLI & Web Interface

A comprehensive mobile phone search system with both command-line and web interfaces for searching across GSMArena, 91mobiles, and Kimovil.

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

## 📱 Interfaces Available

### 1. Command Line Interface (CLI)

**Run the CLI:**
```bash
# Using Python directly
python cli.py "Samsung Galaxy S24"

# Using batch file (Windows)
scraper_cli.bat "Samsung Galaxy S24"
```

**CLI Features:**
- ✅ Interactive mode for easy searching
- ✅ Basic and detailed search modes
- ✅ Multi-site search (GSMArena, 91mobiles, Kimovil)
- ✅ JSON export functionality
- ✅ Phone comparison mode
- ✅ Customizable result limits

**CLI Examples:**
```bash
# Basic search
python cli.py "iPhone 15"

# Detailed search with specific sites
python cli.py "OnePlus" --detailed --sites gsmarena 91mobiles --max-results 10

# Compare phones
python cli.py "Samsung" --compare

# Export to JSON
python cli.py "Google Pixel" --output json

# Interactive mode
python cli.py
```

### 2. Web Interface

**Run the Web App:**
```bash
# Using Python directly
python web_app.py

# Using batch file (Windows)
scraper_web.bat
```

**Web Features:**
- 🌐 Modern responsive web interface
- 🔍 Real-time search with progress indicators
- 📊 Basic and detailed search modes
- 🖼️ Image galleries for phones
- 📋 Expandable specifications
- 💾 JSON export functionality
- 📱 Mobile-friendly design

**Access the Web Interface:**
- Open your browser and go to: `http://localhost:5000`
- Search for phones using the web form
- Export results as JSON files

## 📋 CLI Usage Guide

### Command Syntax
```bash
python cli.py [OPTIONS] QUERY
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--detailed` | `-d` | Get detailed specifications, offers, and images | Basic search |
| `--sites` | `-s` | Specify sites: gsmarena, 91mobiles, kimovil | All sites |
| `--max-results` | `-m` | Maximum results per site | 5 |
| `--output` | `-o` | Output format: console, json, both | console |
| `--output-file` | `-f` | Custom output file path | Auto-generated |
| `--compare` | `-c` | Compare phones side by side | Disabled |
| `--verbose` | `-v` | Verbose output | Disabled |
| `--list-sites` | | List available search sites | |

### Examples

#### Basic Search
```bash
python cli.py "Samsung Galaxy S24"
# Output: Basic phone list with names, prices, ratings
```

#### Detailed Search
```bash
python cli.py "iPhone 15 Pro" --detailed
# Output: Complete specifications, images, offers, seller info
```

#### Multi-Site Search
```bash
python cli.py "OnePlus 11" --sites gsmarena 91mobiles
# Search only GSMArena and 91mobiles
```

#### Limited Results
```bash
python cli.py "Xiaomi" --max-results 3
# Get only 3 results per site
```

#### Export to JSON
```bash
python cli.py "Google Pixel" --detailed --output json
# Save detailed results to JSON file in data/ folder
```

#### Phone Comparison
```bash
python cli.py "Samsung S24" --compare
# Side-by-side comparison of specifications
```

#### Interactive Mode
```bash
python cli.py
# Enter interactive mode for guided search
```

## 🌐 Web Interface Guide

### Starting the Web App
```bash
python web_app.py
```
Then open: `http://localhost:5000`

### Web Interface Features

#### Search Form
- **Query**: Enter phone name or model
- **Search Mode**:
  - Basic: Names, prices, ratings
  - Detailed: Full specs, images, offers
- **Max Results**: Results per site (3-15)
- **Sites**: Check/uncheck sites to search

#### Results Display
- **Basic Mode**: Card layout with key info
- **Detailed Mode**: Full specifications with accordion
- **Images**: Click to view full-size images
- **Export**: Download results as JSON

### Web Interface Screenshots
- Modern Bootstrap UI
- Responsive design (works on mobile)
- Real-time progress indicators
- Expandable specification categories

## 📁 Project Structure

```
universal-scraper/
├── cli.py                 # Command Line Interface
├── web_app.py            # Flask Web Application
├── scraper_cli.bat       # Windows CLI launcher
├── scraper_web.bat       # Windows web app launcher
├── templates/            # HTML templates (auto-created)
│   └── index.html
├── static/               # CSS/JS assets (auto-created)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── universal_search.py   # Core search functionality
├── format_results.py     # Result formatting
├── models/               # Data models
├── scrapers/             # Site-specific scrapers
├── utils/                # Utility functions
└── data/                 # Search results storage
```

## 🔧 Configuration

### Requirements
```
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
fake-useragent==1.4.0
cloudscraper
curl_cffi
undetected-chromedriver
flask==2.3.3
```

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI
python cli.py "Samsung"

# Run Web App
python web_app.py
```

## 📊 Output Formats

### CLI Basic Output
```
🔸 GSM ARENA:
  1. Samsung Galaxy S24 Ultra
     Price: $1,199
     Rating: 9.0/10

  2. Samsung Galaxy S24+
     Price: $999
     Rating: 8.8/10
```

### CLI Detailed Output
```
📋 DETAILED RESULTS (5 phones):

🔸 GSM ARENA:
Samsung Galaxy S24 Ultra
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Price: $1,199 | Rating: 9.0/10 | In Stock: Yes

📱 DISPLAY:
  Type: Dynamic AMOLED 2X
  Size: 6.8 inches
  Resolution: 3120 x 1440

⚡ PLATFORM:
  OS: Android 14
  Chipset: Snapdragon 8 Gen 3
  CPU: Octa-core
```

### Web Interface Output
- Interactive cards with expandable specs
- Image galleries
- Offer listings
- Seller information
- JSON export capability

## 🚀 Advanced Usage

### Batch Processing
```bash
# Search multiple phones
for phone in "iPhone 15" "Samsung S24" "OnePlus 11"; do
    python cli.py "$phone" --detailed --output json
done
```

### API Integration
```python
from universal_search import UniversalSearch
from format_results import format_detailed_results

searcher = UniversalSearch()
results = searcher.search_all("Samsung S24", max_results_per_site=5)
detailed = format_detailed_results(results)
```

### Custom Output Processing
```python
import json
from cli import search_phones

# Get results programmatically
results = search_phones("iPhone", ['gsmarena'], 5, detailed=True)

# Process and save
with open('custom_output.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## 🐛 Troubleshooting

### Common Issues

**CLI Import Errors:**
```bash
# Make sure you're in the project directory
cd /path/to/universal-scraper

# Install requirements
pip install -r requirements.txt
```

**Web App Won't Start:**
```bash
# Check if port 5000 is available
netstat -an | find "5000"

# Kill process using port 5000
# Then restart web app
```

**No Search Results:**
- Check internet connection
- Try different search terms
- Some sites may have anti-bot protection

**Permission Errors:**
```bash
# On Windows, run as administrator or use different directory
# On Linux/Mac, check file permissions
```

## 📈 Performance Tips

- **Use specific search terms**: "Samsung Galaxy S24" instead of "Samsung"
- **Limit results**: Use `--max-results 3` for faster searches
- **Select specific sites**: Don't search all sites if you only need one
- **Use basic mode**: For quick searches without full details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both CLI and web interfaces
5. Submit a pull request

## 📄 License

This project is open source. See LICENSE file for details.

## 🆘 Support

- **Issues**: Create GitHub issues for bugs
- **Features**: Request new features via issues
- **Documentation**: Check this README and inline help (`python cli.py --help`)

---

**Happy Scraping!** 📱✨