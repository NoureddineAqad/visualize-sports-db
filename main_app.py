"""
Integrated Football Database System
Main application combining all modules: database management, web scraping, and simulations
"""

import sys
import os

# Add current directory to path to ensure imports work
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from football_db import FootballDatabase, main_menu as db_main_menu
except ImportError as e:
    print(f"Error importing football_db: {e}")
    print(f"Make sure football_db.py is in the same directory as this script.")
    print(f"Current directory: {os.getcwd()}")
    sys.exit(1)

try:
    from monte_carlo_sim import simulation_menu
except ImportError as e:
    print(f"Error importing monte_carlo_sim: {e}")
    print(f"Make sure monte_carlo_sim.py is in the same directory as this script.")
    print(f"Current directory: {os.getcwd()}")
    sys.exit(1)

try:
    from web_scraper import scraper_menu
except ImportError as e:
    print(f"Error importing web_scraper: {e}")
    print(f"Make sure web_scraper.py is in the same directory as this script.")
    print(f"Current directory: {os.getcwd()}")
    sys.exit(1)


def find_json_files():
    """Find all JSON files in current directory that could be competition databases"""
    import glob
    json_files = glob.glob('*.json')
    # Filter for likely competition files (containing common keywords)
    competition_files = []
    for f in json_files:
        lower = f.lower()
        if any(keyword in lower for keyword in ['league', 'cup', 'champions', 'tournament', 'competition']):
            competition_files.append(f)
    return competition_files if competition_files else json_files


def save_last_competition(comp_name):
    """Save the last opened competition name"""
    try:
        with open('.last_competition', 'w', encoding='utf-8') as f:
            f.write(comp_name)
    except:
        pass


def load_last_competition():
    """Load the last opened competition name"""
    try:
        with open('.last_competition', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return None


def enhanced_competition_menu(db: FootballDatabase):
    """Enhanced menu with all features including scraping and simulations"""
    while True:
        print("\n" + "="*70)
        print(f"{db.competition_name.upper()} - MAIN MENU")
        print("="*70)
        print("\n📊 DATABASE MANAGEMENT")
        print("1. View current standings")
        print("2. Enter matchday calendar")
        print("3. Enter matchday results manually")
        print("4. View all matches")
        print("5. 🎨 Launch Visual Dashboard (GUI)")
        print("\n🌐 WEB SCRAPING")
        print("6. Fetch results from web (with verification)")
        print("7. Fetch team names from web")
        print("8. Extract data from Wikipedia (teams, calendar, results)")
        print("\n🎲 SIMULATIONS & PREDICTIONS")
        print("9. Run Monte Carlo simulation")
        print("10. View simulation results")
        print("\n💾 DATA MANAGEMENT")
        print("11. Save database")
        print("12. Export standings to file")
        print("13. Return to main menu")
        
        choice = input("\nEnter your choice (1-13): ").strip()
        
        if choice == '1':
            db.display_standings()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            matchday = int(input("Enter matchday number: "))
            db.enter_matchday_calendar(matchday)
        
        elif choice == '3':
            try:
                matchday_input = input("Enter matchday number: ").strip()
                if not matchday_input:
                    print("❌ Matchday number cannot be empty!")
                    continue
                matchday = int(matchday_input)
                if matchday < 1:
                    print("❌ Matchday must be a positive number!")
                    continue
                db.enter_matchday_results(matchday)
                db.display_standings()
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Please enter a valid matchday number!")
            except Exception as e:
                print(f"❌ Error entering results: {type(e).__name__}: {e}")
                print("Please try again or check your data.")
        
        elif choice == '4':
            print("\n" + "="*70)
            print("ALL MATCHES")
            print("="*70)
            
            # Group by matchday
            from collections import defaultdict
            matches_by_md = defaultdict(list)
            for match in db.matches:
                matches_by_md[match.matchday].append(match)
            
            if not matches_by_md:
                print("\nNo matches in database yet.")
            else:
                for matchday in sorted(matches_by_md.keys()):
                    print(f"\n--- MATCHDAY {matchday} ---")
                    for match in matches_by_md[matchday]:
                        if match.played:
                            print(f"  {match.home_team} {match.home_score}-{match.away_score} {match.away_team} ✓")
                        else:
                            print(f"  {match.home_team} vs {match.away_team}")
            
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            # Launch GUI Dashboard
            try:
                from gui_dashboard import launch_dashboard
                print("\n🎨 Launching Visual Dashboard...")
                print("A new window will open with interactive visualizations")
                print("Close the dashboard window to return here.\n")
                launch_dashboard(db)
            except ImportError as e:
                print(f"\n❌ Could not load GUI module: {e}")
                print("Make sure CustomTkinter and Matplotlib are installed:")
                print("   pip install customtkinter matplotlib")
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"\n❌ Error launching dashboard: {e}")
                import traceback
                traceback.print_exc()
                input("\nPress Enter to continue...")
        
        elif choice == '6':
            scraper_menu(db)
            db.display_standings()
            input("\nPress Enter to continue...")
        
        elif choice == '7':
            print("\nFetching team names...")
            fetched_teams = db.fetch_champions_league_teams()
            if fetched_teams:
                print(f"\nFound {len(fetched_teams)} teams:")
                for name, country in fetched_teams:
                    print(f"  - {name} ({country})")
                
                add = input("\nAdd these teams to database? (y/n): ").lower()
                if add == 'y':
                    db.verify_and_edit_teams(fetched_teams)
            else:
                print("No teams found via web scraping")
        
        elif choice == '8':
            from wikipedia_scraper import wikipedia_scraper_menu
            wikipedia_scraper_menu(db)
        
        elif choice == '9':
            simulation_menu(db)
        
        elif choice == '10':
            # Quick simulation results view
            print("\nThis will run a quick simulation to show probabilities.")
            run = input("Continue? (y/n): ").lower()
            if run == 'y':
                from monte_carlo_sim import MonteCarloSimulator
                sim = MonteCarloSimulator(db, n_simulations=5000)
                sim.run_simulations()
                sim.display_qualification_probabilities()
        
        elif choice == '11':
            db.save_to_file()
        
        elif choice == '12':
            filename = f"{db.competition_name.lower().replace(' ', '_')}_standings.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                standings = db.get_standings()
                f.write(f"{db.competition_name.upper()} - STANDINGS (After Matchday {db.current_matchday})\n")
                f.write("="*90 + "\n")
                f.write(f"{'Pos':<4} {'Team':<30} {'MP':<4} {'W':<4} {'D':<4} {'L':<4} {'GF':<4} {'GA':<4} {'GD':<5} {'Pts':<4}\n")
                f.write("-" * 90 + "\n")
                for i, team in enumerate(standings, 1):
                    f.write(f"{i:<4} {team.name:<30} {team.matches_played:<4} {team.wins:<4} "
                           f"{team.draws:<4} {team.losses:<4} {team.goals_for:<4} {team.goals_against:<4} "
                           f"{team.goal_difference:+5} {team.points:<4}\n")
            print(f"✓ Standings exported to {filename}")
        
        elif choice == '13':
            save = input("Save before exiting? (y/n): ")
            if save.lower() == 'y':
                db.save_to_file()
            break
        
        else:
            print("Invalid choice!")


def main():
    """Main application entry point"""
    print("="*70)
    print("FOOTBALL DATABASE MANAGEMENT SYSTEM")
    print("Complete solution with Web Scraping & Monte Carlo Simulations")
    print("="*70)
    
    while True:
        print("\n" + "="*70)
        print("MAIN MENU")
        print("="*70)
        print("1. Create new competition database")
        print("2. Load existing competition database")
        print("3. Quick start guide")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            comp_name = input("\nEnter competition name (e.g., 'Champions League 2024-25'): ").strip()
            db = FootballDatabase(comp_name)
            
            print("\n" + "="*70)
            print("TEAM SETUP")
            print("="*70)
            print("1. Automatically fetch teams (Champions League only)")
            print("2. Enter teams manually")
            
            setup_choice = input("\nEnter choice (1-2): ").strip()
            
            if setup_choice == '1' and 'champions league' in comp_name.lower():
                fetched_teams = db.fetch_champions_league_teams()
                db.verify_and_edit_teams(fetched_teams)
            else:
                num_teams = int(input("How many teams? "))
                db.add_manual_teams(num_teams)
            
            save_last_competition(comp_name)
            enhanced_competition_menu(db)
        
        elif choice == '2':
            # Check for last opened competition
            last_comp = load_last_competition()
            
            # Find available JSON files
            json_files = find_json_files()
            
            print("\n" + "="*70)
            print("LOAD COMPETITION DATABASE")
            print("="*70)
            
            # Show last opened if available
            if last_comp:
                print(f"\n💡 Last opened: {last_comp}")
                load_last = input("Press Enter to load it, or type a different name: ").strip()
                if not load_last:  # User pressed Enter
                    comp_name = last_comp
                else:
                    comp_name = load_last
            else:
                # Show available JSON files
                if json_files:
                    print("\n📁 Found these database files:")
                    for i, f in enumerate(json_files, 1):
                        print(f"  {i}. {f}")
                    print(f"  {len(json_files) + 1}. Enter custom name")
                    
                    choice_input = input(f"\nSelect file (1-{len(json_files) + 1}): ").strip()
                    
                    if choice_input.isdigit():
                        choice_num = int(choice_input)
                        if 1 <= choice_num <= len(json_files):
                            # Extract competition name from filename
                            selected_file = json_files[choice_num - 1]
                            # Remove .json extension, then remove _data suffix, then convert underscores to spaces
                            comp_name = selected_file.replace('.json', '')
                            if comp_name.endswith('_data'):
                                comp_name = comp_name[:-5]  # Remove _data
                            comp_name = comp_name.replace('_', ' ')
                        else:
                            comp_name = input("\nEnter competition name: ").strip()
                    else:
                        comp_name = choice_input if choice_input else input("\nEnter competition name: ").strip()
                else:
                    comp_name = input("\nEnter competition name to load: ").strip()
            
            db = FootballDatabase(comp_name)
            if db.load_from_file():
                save_last_competition(comp_name)
                enhanced_competition_menu(db)
            else:
                print("Failed to load database. Please check the competition name.")
        
        elif choice == '3':
            display_quick_start_guide()
        
        elif choice == '4':
            print("\n" + "="*70)
            print("Thank you for using the Football Database Management System!")
            print("="*70)
            break
        
        else:
            print("Invalid choice!")


def display_quick_start_guide():
    """Display a quick start guide for new users"""
    guide = """
    
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                       QUICK START GUIDE                              ║
    ╚══════════════════════════════════════════════════════════════════════╝
    
    STEP 1: CREATE DATABASE
    ─────────────────────────
    • Choose "Create new competition database"
    • Enter competition name (e.g., "Champions League 2024-25")
    • For Champions League, try automatic team fetching
    • For other competitions, enter teams manually
    
    STEP 2: ENTER MATCH CALENDAR
    ─────────────────────────────
    • Select "Enter matchday calendar"
    • Enter matchday number (1, 2, 3, etc.)
    • Input all matches for that matchday
    • Repeat for each matchday
    
    STEP 3: ENTER RESULTS
    ──────────────────────
    Option A - Manual Entry:
      • Select "Enter matchday results manually"
      • Enter scores for each match
    
    Option B - Web Scraping (Experimental):
      • Select "Fetch results from web"
      • System will attempt to find results automatically
      • Verify and correct any incorrect data
    
    STEP 4: VIEW STANDINGS
    ───────────────────────
    • After entering results, view updated standings
    • Standings are calculated automatically
    
    STEP 5: RUN SIMULATIONS (Optional)
    ───────────────────────────────────
    • Select "Run Monte Carlo simulation"
    • Choose number of simulations (10,000 recommended)
    • Select which matchdays to simulate
    • View qualification probabilities
    
    FEATURES:
    ─────────
    ✓ Automatic web scraping for teams and results
    ✓ User verification for all scraped data
    ✓ Monte Carlo simulations for predictions
    ✓ Qualification probability calculations
    ✓ Export standings and simulation results
    ✓ Save/load database between sessions
    
    TIPS:
    ─────
    • Always save your database after making changes
    • Web scraping works best for Champions League
    • For accurate simulations, enter at least 3-4 matchdays
    • Simulations become more accurate as more matches are played
    
    Press Enter to continue...
    """
    
    print(guide)
    input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting application...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)
