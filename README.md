# ⚽ Football Database Management System

A comprehensive Python application for managing football competition data with intelligent team name matching, web scraping, Monte Carlo simulations, and interactive visualizations.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Status](https://img.shields.io/badge/status-active-success)]()

## 🌟 Key Features

### 🎯 **Intelligent Fuzzy Team Matching** ⭐ NEW!
- Type team names naturally with special characters
- Handles variations: "Bodo/Glimt" → finds "BodoGlimt"
- Case-insensitive matching
- Partial name matching
- Works in both calendar entry AND results entry
- **Perfect for teams with special characters in names!**

### 📊 Core Features
- **Complete Database Management**: Track teams, matches, and standings
- **Two-Step Workflow**: Enter fixtures first, then results separately
- **Automatic Standings Calculation**: Real-time UEFA-style rankings
- **Web Scraping**: Fetch teams and results automatically
- **Monte Carlo Simulations**: Predict tournament outcomes
- **Interactive GUI Dashboard**: Visual interface (optional)
- **JSON Storage**: Human-readable data persistence

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/football-database.git
cd football-database

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main_app.py
```

## 📖 Usage

### Starting the Application

```bash
python main_app.py
```

### Workflow

#### Step 1: Create or Load Database
```
1. Create new competition database
   OR
2. Load existing competition database
```

#### Step 2: Enter Match Calendar (Fixtures)
```
Choose: 2. Enter matchday calendar

💡 You can now type team names naturally:
- "Bodo/Glimt" → automatically finds "BodoGlimt" ✅
- "Man City" → finds "Manchester City" ✅
- "PSG" → finds "Paris Saint-Germain" ✅
- Or use team numbers (1-36)
```

#### Step 3: Enter Match Results
```
Choose: 3. Enter matchday results manually

The system shows your pre-entered fixtures.
Just enter the scores - team names are already set!

Even if fixtures have old team names (like "Bodo/Glimt"),
the fuzzy matcher automatically finds the correct team ("BodoGlimt")!
```

## 🎯 The Fuzzy Matching Feature

### The Problem It Solves

**Before:** 
```
Home team: Bodo/Glimt
❌ ERROR: Home team 'Bodo/Glimt' not found in database!
```

**After:** 
```
Home team: Bodo/Glimt
  → Matched: BodoGlimt ✅
Away team: Juventus
  → Matched: Juventus ✅
✓ Added: BodoGlimt vs Juventus
```

### How It Works

The fuzzy matcher:
1. **Normalizes input**: Removes special characters (/, -, .)
2. **Tries exact match**: Case-insensitive exact match
3. **Tries normalized match**: "Bodo/Glimt" matches "BodoGlimt"
4. **Tries partial match**: "Man City" matches "Manchester City"
5. **Shows what matched**: Confirms the team found

### Supported Variations

All these will correctly find "BodoGlimt":
- `Bodo/Glimt` ✅
- `bodoglimt` ✅
- `BODO GLIMT` ✅
- `Bodo` ✅
- `bodo glimt` ✅

## 📂 Project Structure

```
football-database/
│
├── main_app.py              # Main application entry point
├── football_db.py           # Core database with fuzzy matching
├── monte_carlo_sim.py       # Monte Carlo simulation module
├── web_scraper.py           # Web scraping functionality
├── gui_dashboard.py         # GUI interface (optional)
│
├── data/                    # Data storage
│   └── *.json              # Competition databases
│
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
│
└── docs/                   # Documentation
    ├── QUICKSTART.md       # Quick start guide
    ├── TUTORIAL.md         # Detailed tutorial
    └── API.md              # API documentation
```

## 🔧 Technical Details

### Fuzzy Matching Algorithm

```python
def find_team_fuzzy(self, search_name: str) -> Optional[str]:
    """
    Find team by name with fuzzy matching
    
    Args:
        search_name: Team name to search for (can include special chars)
    
    Returns:
        Actual team name from database, or None if not found
    """
    # 1. Normalize: Remove special chars, lowercase
    normalized_search = self.normalize_team_name(search_name)
    
    # 2. Try exact match (case-insensitive)
    for team_name in self.teams.keys():
        if team_name.lower() == search_name.lower():
            return team_name
    
    # 3. Try normalized match (Bodo/Glimt → BodoGlimt)
    for team_name in self.teams.keys():
        if self.normalize_team_name(team_name) == normalized_search:
            return team_name  # ← Key fix!
    
    # 4. Try partial matches...
```

### Where Fuzzy Matching Is Used

1. **Calendar Entry** (`enter_matchday_calendar`)
   - Home team input
   - Away team input

2. **Results Entry** (`enter_matchday_results`)
   - Team verification from stored matches
   - Statistics updates

This ensures that even if old matches were stored with "Bodo/Glimt", they'll still work when the team is now called "BodoGlimt"!

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| **Fuzzy Team Matching** | Intelligent name matching | ✅ Active |
| Database Management | CRUD operations for teams/matches | ✅ Active |
| Standings Calculation | Automatic UEFA-style ranking | ✅ Active |
| Two-Step Workflow | Calendar → Results | ✅ Active |
| Web Scraping | Auto-fetch teams/results | ✅ Active |
| Monte Carlo Simulation | Tournament predictions | ✅ Active |
| JSON Storage | Data persistence | ✅ Active |
| GUI Dashboard | Visual interface | ✅ Active |
| Export Standings | Export to text files | ✅ Active |

## 🎮 Example Usage

### Creating a New Competition

```python
from football_db import FootballDatabase

# Create database
db = FootballDatabase("Champions League 2024-25")

# Add teams
db.add_team("Real Madrid", "Spain")
db.add_team("BodoGlimt", "Norway")  # No slash for filesystem compatibility
db.add_team("Manchester City", "England")

# Create match (calendar entry)
db.create_match("BodoGlimt", "Manchester City", matchday=1)

# Later, enter results
# Even if you type "Bodo/Glimt", it will work!
```

### CLI Example

```bash
$ python main_app.py

FOOTBALL DATABASE MANAGEMENT SYSTEM
====================================

MAIN MENU
---------
1. Create new competition database
2. Load existing competition database
3. Quick start guide
4. Exit

Enter your choice: 2

Enter competition name: Champions League 2024-25

MAIN MENU
---------
1. View current standings
2. Enter matchday calendar      ← First, enter fixtures
3. Enter matchday results        ← Then, enter scores
4. View all matches
...

Enter your choice: 2

Enter matchday number: 5
How many matches in matchday 5? 1

Available teams:
1. Arsenal
2. Atalanta
...
11. BodoGlimt
...

Home team (name or number): Bodo/Glimt
  → Matched: BodoGlimt             ← Fuzzy matching works!
Away team (name or number): Juventus
  → Matched: Juventus
✓ Added: BodoGlimt vs Juventus

---

Enter your choice: 3

Enter matchday number: 5

=== Match 1/1 ===
BodoGlimt vs Juventus            ← Shows the match
BodoGlimt score: 2               ← Just enter scores
Juventus score: 3
✓ Result recorded: BodoGlimt 2-3 Juventus
```

## 🛠️ Configuration

### requirements.txt

```
requests>=2.27.0
beautifulsoup4>=4.10.0
matplotlib>=3.5.0        # For GUI (optional)
customtkinter>=5.0.0     # For GUI (optional)
```

### Python Version

- Minimum: Python 3.8
- Recommended: Python 3.11
- Tested on: Python 3.8, 3.9, 3.10, 3.11

## 🐛 Troubleshooting

### Common Issues

**Issue 1: Team name not found**
```
❌ ERROR: Home team 'Bodo/Glimt' not found in database!
```
**Solution**: This is now FIXED with fuzzy matching! Update to the latest version.

**Issue 2: Import errors**
```
ImportError: No module named 'web_scraper'
```
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

**Issue 3: GUI not launching**
```
ImportError: No module named 'customtkinter'
```
**Solution**: Install GUI dependencies:
```bash
pip install customtkinter matplotlib
```

## 🔄 Changelog

### Version 1.1.0 (2025-11-27) - Fuzzy Matching Update

**🎯 Major Feature:**
- ✨ Added intelligent fuzzy team name matching
- ✅ Handles special characters (/, -, etc.)
- ✅ Case-insensitive matching
- ✅ Partial name matching
- ✅ Works in calendar AND results entry

**🐛 Bug Fixes:**
- Fixed: "Bodo/Glimt not found" error
- Fixed: Team name mismatch between fixtures and database
- Fixed: Results entry failing with old fixture names

**📝 Improvements:**
- Better error messages
- User feedback when team is matched
- Fallback suggestions if no match found

### Version 1.0.0 (2025-11-15) - Initial Release

- Basic database management
- Web scraping
- Monte Carlo simulations
- GUI dashboard
- JSON storage

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/football-database.git
cd football-database

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 🙏 Acknowledgments

- UEFA for the Champions League format
- Python community for excellent libraries
- Contributors and testers
- Special thanks for the fuzzy matching feature suggestion!

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/football-database/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/football-database/discussions)
- **Email**: your.email@example.com

## 🗺️ Roadmap

- [ ] Add team aliases (PSG → Paris Saint-Germain)
- [ ] Levenshtein distance for typo correction
- [ ] Multi-language support
- [ ] Web interface
- [ ] REST API
- [ ] Mobile app
- [ ] Real-time data updates
- [ ] Advanced statistics

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by [Your Name]**

**Last Updated**: 2025-11-27  
**Version**: 1.1.0  
**Status**: Active Development 🚀
