# ⚡ Quick Start Guide

Get your Football Database up and running in 5 minutes!

## 🚀 Installation (2 minutes)

### Step 1: Clone or Download

```bash
# Option A: Clone from GitHub
git clone https://github.com/yourusername/football-database.git
cd football-database

# Option B: Download ZIP
# Extract and navigate to the folder
cd football-database
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! You're ready to go! ✅

---

## 🎮 First Run (3 minutes)

### Start the Application

```bash
python main_app.py
```

### Create Your First Competition

```
MAIN MENU
1. Create new competition database    ← Choose this
2. Load existing competition database
3. Quick start guide
4. Exit

Enter your choice: 1

Enter competition name: Champions League 2024-25

TEAM SETUP
1. Automatically fetch teams (Champions League only)
2. Enter teams manually                ← Choose this for now

Enter choice: 2
How many teams? 4

Team 1 name: Real Madrid
Team 1 country: Spain

Team 2 name: BodoGlimt
Team 2 country: Norway

Team 3 name: Manchester City
Team 3 country: England

Team 4 name: Juventus
Team 4 country: Italy
```

### Enter Match Calendar (Fixtures)

```
MAIN MENU
2. Enter matchday calendar            ← Choose this

Enter matchday number: 1
How many matches in matchday 1? 2

Available teams:
1. BodoGlimt
2. Juventus
3. Manchester City
4. Real Madrid

--- Match 1/2 ---
Home team (name or number): Bodo/Glimt    ← Type with slash!
  → Matched: BodoGlimt                     ← Fuzzy matching works!
Away team (name or number): Juventus
✓ Added: BodoGlimt vs Juventus

--- Match 2/2 ---
Home team (name or number): 3              ← Or use number
  Selected: Manchester City
Away team (name or number): Real Madrid
✓ Added: Manchester City vs Real Madrid
```

### Enter Match Results

```
MAIN MENU
3. Enter matchday results manually    ← Choose this

Enter matchday number: 1

=== Match 1/2 ===
BodoGlimt vs Juventus
BodoGlimt score: 2                    ← Just enter scores!
Juventus score: 3
✓ Result recorded: BodoGlimt 2-3 Juventus

=== Match 2/2 ===
Manchester City vs Real Madrid
Manchester City score: 1
Real Madrid score: 1
✓ Result recorded: Manchester City 1-1 Real Madrid
```

### View Standings

```
MAIN MENU
1. View current standings              ← Choose this

CHAMPIONS LEAGUE 2024-25 - STANDINGS
=====================================
Pos  Team                MP  W  D  L  GF  GA  GD   Pts
1    Juventus            1   1  0  0  3   2   +1   3
2    Real Madrid         1   0  1  0  1   1   0    1
3    Manchester City     1   0  1  0  1   1   0    1
4    BodoGlimt           1   0  0  1  2   3   -1   0
```

🎉 **Congratulations!** You've created your first football database!

---

## 🎯 Key Features You Just Used

✅ **Fuzzy Team Matching** - Typed "Bodo/Glimt" with slash, found "BodoGlimt"  
✅ **Two-Step Workflow** - Calendar first, then results  
✅ **Automatic Standings** - Calculated in real-time  
✅ **Number Selection** - Used team number (3) instead of name  

---

## 📚 What's Next?

### Learn More Features

```
MAIN MENU
4. View all matches          - See complete match list
5. Launch Visual Dashboard   - GUI interface (needs extra packages)
6. Fetch results from web    - Auto-scrape data
9. Run Monte Carlo simulation - Predict outcomes
11. Save database            - Persist your data
```

### Add More Matchdays

Repeat the process:
1. Enter matchday calendar (fixtures for matchday 2, 3, etc.)
2. Enter matchday results (scores)
3. View updated standings

### Save Your Work

```
MAIN MENU
11. Save database            ← IMPORTANT!

✓ Data saved to: champions_league_2024-25_data.json
```

### Load Next Time

```
MAIN MENU
2. Load existing competition database

Enter competition name: Champions League 2024-25
✓ Database loaded successfully!
```

---

## 💡 Pro Tips

### 1. Fuzzy Team Matching

All these work for "BodoGlimt":
- `Bodo/Glimt` ✅
- `bodoglimt` ✅
- `BODO GLIMT` ✅
- `Bodo` ✅
- Or just use number: `1` ✅

### 2. Quick Team Selection

Instead of typing full names, use numbers:
```
Home team: 1        ← Faster!
Away team: 2
```

### 3. Save Regularly

After entering results, always save:
```
MAIN MENU → 11. Save database
```

### 4. Show Available Teams

When entering calendar, the system shows all teams with numbers.

### 5. View Matches

Check what matches exist:
```
MAIN MENU → 4. View all matches
```

---

## 🐛 Common First-Time Issues

### Issue 1: "Module not found"

```bash
# Install dependencies
pip install -r requirements.txt
```

### Issue 2: "Team not found" error

**Old version:** Would fail  
**New version (v1.1.0):** Fuzzy matching handles it! ✅

If you still get errors, make sure you have v1.1.0:
```bash
# Check football_db.py has find_team_fuzzy() method
grep -n "find_team_fuzzy" football_db.py
```

### Issue 3: Can't load database

Make sure you're typing the exact competition name:
```
Created as: "Champions League 2024-25"
Load as: "Champions League 2024-25"  ← Must match exactly!
```

### Issue 4: GUI won't launch (Option 5)

```bash
# Install GUI dependencies
pip install matplotlib customtkinter
```

---

## 📖 Next Steps

### Read the Documentation

1. **[README.md](README.md)** - Complete feature overview
2. **[FUZZY_MATCHING.md](docs/FUZZY_MATCHING.md)** - How fuzzy matching works
3. **[CHANGELOG.md](CHANGELOG.md)** - What's new in v1.1.0

### Try Advanced Features

1. **Monte Carlo Simulation** (Option 9)
   - Predict tournament outcomes
   - Calculate qualification probabilities

2. **Web Scraping** (Option 6)
   - Auto-fetch match results
   - Requires internet connection

3. **GUI Dashboard** (Option 5)
   - Visual interface
   - Requires: `pip install matplotlib customtkinter`

---

## 🎯 Typical Workflow

```
Session 1: Setup
├── Create competition
├── Add teams
├── Enter matchday 1 calendar
└── Save

Session 2: First Results
├── Load competition
├── Enter matchday 1 results
├── View standings
└── Save

Session 3: Continue
├── Load competition
├── Enter matchday 2 calendar
├── Enter matchday 2 results
├── View updated standings
└── Save

... and so on for each matchday
```

---

## ⏱️ Time Investment

- **Setup:** 2 minutes
- **Learn basics:** 3 minutes
- **Enter 1 matchday:** 2-5 minutes
- **Total to get started:** ~10 minutes

---

## 🆘 Need Help?

- **Documentation:** Check [README.md](README.md)
- **Issues:** Open on [GitHub Issues](https://github.com/yourusername/football-database/issues)
- **Questions:** Ask in [Discussions](https://github.com/yourusername/football-database/discussions)

---

## ✅ Quick Reference

### Menu Options (Most Used)

| Option | Action | When to Use |
|--------|--------|-------------|
| 1 | View standings | After entering results |
| 2 | Enter calendar | Before each matchday |
| 3 | Enter results | After matches are played |
| 4 | View matches | To check fixture list |
| 11 | Save | After any changes |

### Keyboard Shortcuts

- **Ctrl+C** - Exit anytime
- Just enter **numbers** for quick team selection

---

**You're ready to go! Enjoy managing your football database!** ⚽🚀

**Time to master:** 5 minutes  
**Time to value:** Immediate ✅
