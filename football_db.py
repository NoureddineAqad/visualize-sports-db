"""
Football Database Management System
Handles team fetching, match scheduling, results entry, and standings calculation
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup


class Team:
    """Represents a football team"""
    def __init__(self, name: str, country: str = ""):
        self.name = name
        self.country = country
        self.matches_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
    
    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against
    
    def update_stats(self, goals_for: int, goals_against: int):
        """Update team statistics after a match"""
        self.matches_played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        
        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
        elif goals_for == goals_against:
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1
    
    def reset_stats(self):
        """Reset all statistics"""
        self.matches_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'country': self.country,
            'matches_played': self.matches_played,
            'wins': self.wins,
            'draws': self.draws,
            'losses': self.losses,
            'goals_for': self.goals_for,
            'goals_against': self.goals_against,
            'points': self.points,
            'goal_difference': self.goal_difference
        }


class Match:
    """Represents a football match"""
    def __init__(self, home_team: str, away_team: str, matchday: int):
        self.home_team = home_team
        self.away_team = away_team
        self.matchday = matchday
        self.home_score: Optional[int] = None
        self.away_score: Optional[int] = None
        self.played = False
    
    def set_result(self, home_score: int, away_score: int):
        """Set the match result"""
        self.home_score = home_score
        self.away_score = away_score
        self.played = True
    
    def to_dict(self) -> dict:
        return {
            'home_team': self.home_team,
            'away_team': self.away_team,
            'matchday': self.matchday,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'played': self.played
        }


class FootballDatabase:
    """Main database class for managing football competition data"""
    
    def __init__(self, competition_name: str):
        self.competition_name = competition_name
        self.teams: Dict[str, Team] = {}
        self.matches: List[Match] = []
        self.current_matchday = 0
        self.data_file = f"{competition_name.lower().replace(' ', '_')}_data.json"
    
    def normalize_team_name(self, name: str) -> str:
        """
        Normalize team name for fuzzy matching
        Removes special characters and standardizes format
        """
        import re
        normalized = name.lower().strip()
        normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
        normalized = ' '.join(normalized.split())
        return normalized
    
    def find_team_fuzzy(self, search_name: str) -> Optional[str]:
        """
        Find team by name with fuzzy matching
        Handles variations like "Bodo/Glimt" vs "BodoGlimt"
        
        Returns the actual team name from database, or None if not found
        """
        normalized_search = self.normalize_team_name(search_name)
        
        # Try exact match first (case-insensitive)
        for team_name in self.teams.keys():
            if team_name.lower().strip() == search_name.lower().strip():
                return team_name
        
        # Try normalized match (this will match "Bodo/Glimt" to "BodoGlimt")
        for team_name in self.teams.keys():
            if self.normalize_team_name(team_name) == normalized_search:
                return team_name
        
        # Try partial match (search term in team name)
        for team_name in self.teams.keys():
            if normalized_search in self.normalize_team_name(team_name):
                return team_name
        
        # Try reverse partial match (team name in search term)
        for team_name in self.teams.keys():
            if self.normalize_team_name(team_name) in normalized_search:
                return team_name
        
        return None
    
    def fetch_champions_league_teams(self) -> List[Tuple[str, str]]:
        """
        Attempt to fetch Champions League teams from web sources
        Returns list of (team_name, country) tuples
        """
        print("Attempting to fetch Champions League teams...")
        teams = []
        
        try:
            # Try UEFA official website
            url = "https://www.uefa.com/uefachampionsleague/clubs/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to find team elements (structure may vary)
                # This is a placeholder - actual selectors depend on UEFA's current HTML structure
                team_elements = soup.find_all(['div', 'a'], class_=lambda x: x and 'team' in x.lower())
                
                for element in team_elements[:36]:  # Champions League typically has 36 teams
                    team_name = element.get_text(strip=True)
                    if team_name and len(team_name) > 2:
                        teams.append((team_name, ""))
                
                if teams:
                    print(f"Successfully fetched {len(teams)} teams from UEFA website")
                    return teams
        
        except Exception as e:
            print(f"Error fetching from UEFA website: {e}")
        
        # Fallback: return empty list if fetching fails
        print("Could not automatically fetch teams. Will use manual entry.")
        return teams
    
    def add_team(self, name: str, country: str = "") -> Team:
        """Add a team to the database"""
        team = Team(name, country)
        self.teams[name] = team
        return team
    
    def verify_and_edit_teams(self, fetched_teams: List[Tuple[str, str]]) -> List[Team]:
        """
        Display fetched teams and allow user to verify/edit them
        """
        print("\n" + "="*70)
        print(f"TEAM VERIFICATION FOR {self.competition_name}")
        print("="*70)
        
        if not fetched_teams:
            print("No teams were automatically fetched.")
            num_teams = int(input("How many teams are in this competition? "))
            fetched_teams = [("", "") for _ in range(num_teams)]
        
        teams_list = []
        
        for i, (name, country) in enumerate(fetched_teams, 1):
            print(f"\n--- Team {i} ---")
            if name:
                print(f"Fetched: {name} ({country if country else 'Country not found'})")
                correct = input("Is this correct? (y/n/edit): ").lower()
                
                if correct == 'y':
                    teams_list.append((name, country))
                elif correct == 'edit':
                    name = input("Enter team name: ").strip()
                    country = input("Enter country (optional): ").strip()
                    teams_list.append((name, country))
                else:
                    name = input("Enter correct team name: ").strip()
                    country = input("Enter country (optional): ").strip()
                    teams_list.append((name, country))
            else:
                name = input(f"Enter team {i} name: ").strip()
                country = input("Enter country (optional): ").strip()
                teams_list.append((name, country))
        
        # Add teams to database
        for name, country in teams_list:
            self.add_team(name, country)
        
        print(f"\n✓ {len(self.teams)} teams added to the database")
        return list(self.teams.values())
    
    def add_manual_teams(self, num_teams: int):
        """Manually add teams to the database"""
        print(f"\nEnter {num_teams} team names:")
        for i in range(num_teams):
            name = input(f"Team {i+1} name: ").strip()
            country = input(f"Team {i+1} country (optional): ").strip()
            self.add_team(name, country)
    
    def create_match(self, home_team: str, away_team: str, matchday: int) -> Match:
        """Create a new match"""
        if home_team not in self.teams or away_team not in self.teams:
            raise ValueError(f"Both teams must exist in the database")
        
        match = Match(home_team, away_team, matchday)
        self.matches.append(match)
        return match
    
    def enter_matchday_calendar(self, matchday: int):
        """Enter all matches for a specific matchday"""
        print(f"\n{'='*70}")
        print(f"ENTERING MATCHDAY {matchday} CALENDAR")
        print(f"{'='*70}")
        
        num_matches = int(input(f"How many matches in matchday {matchday}? "))
        
        print("\nAvailable teams:")
        team_list = sorted(self.teams.keys())
        for i, team_name in enumerate(team_list, 1):
            print(f"{i}. {team_name}")
        
        print("\n💡 TIP: You can enter team names exactly as shown above, or use the team number.")
        
        for i in range(num_matches):
            print(f"\n--- Match {i+1}/{num_matches} ---")
            
            while True:
                home_input = input("Home team (name or number): ").strip()
                
                # Check if input is a number
                if home_input.isdigit():
                    idx = int(home_input) - 1
                    if 0 <= idx < len(team_list):
                        home = team_list[idx]
                        print(f"  Selected: {home}")
                        break
                    else:
                        print(f"❌ Invalid number. Please enter 1-{len(team_list)}")
                        continue
                else:
                    # Try fuzzy matching first
                    matched_team = self.find_team_fuzzy(home_input)
                    if matched_team:
                        home = matched_team
                        if matched_team != home_input:
                            print(f"  → Matched: {home}")
                        break
                    
                    # If fuzzy match failed, show suggestions
                    similar = [t for t in self.teams.keys() if home_input.lower() in t.lower() or t.lower() in home_input.lower()]
                    if similar:
                        print(f"❌ Team '{home_input}' not found. Did you mean:")
                        for j, t in enumerate(similar, 1):
                            print(f"  {j}. {t}")
                        retry = input("Enter the number of the correct team, or 'r' to retry: ").strip()
                        if retry.isdigit():
                            idx = int(retry) - 1
                            if 0 <= idx < len(similar):
                                home = similar[idx]
                                print(f"  Selected: {home}")
                                break
                    else:
                        print(f"❌ Team '{home_input}' not found in database!")
                    print("Please try again.")
            
            while True:
                away_input = input("Away team (name or number): ").strip()
                
                # Check if input is a number
                if away_input.isdigit():
                    idx = int(away_input) - 1
                    if 0 <= idx < len(team_list):
                        away = team_list[idx]
                        print(f"  Selected: {away}")
                        if away == home:
                            print("❌ Away team cannot be the same as home team!")
                            continue
                        break
                    else:
                        print(f"❌ Invalid number. Please enter 1-{len(team_list)}")
                        continue
                else:
                    # Try fuzzy matching first
                    matched_team = self.find_team_fuzzy(away_input)
                    if matched_team:
                        away = matched_team
                        if matched_team != away_input:
                            print(f"  → Matched: {away}")
                        if away == home:
                            print("❌ Away team cannot be the same as home team!")
                            continue
                        break
                    
                    # If fuzzy match failed, show suggestions
                    similar = [t for t in self.teams.keys() if away_input.lower() in t.lower() or t.lower() in away_input.lower()]
                    if similar:
                        print(f"❌ Team '{away_input}' not found. Did you mean:")
                        for j, t in enumerate(similar, 1):
                            print(f"  {j}. {t}")
                        retry = input("Enter the number of the correct team, or 'r' to retry: ").strip()
                        if retry.isdigit():
                            idx = int(retry) - 1
                            if 0 <= idx < len(similar):
                                away = similar[idx]
                                print(f"  Selected: {away}")
                                if away == home:
                                    print("❌ Away team cannot be the same as home team!")
                                    continue
                                break
                    else:
                        print(f"❌ Team '{away_input}' not found in database!")
                    print("Please try again.")
            
            # Create the match
            try:
                self.create_match(home, away, matchday)
                print(f"✓ Added: {home} vs {away}")
            except ValueError as e:
                print(f"❌ Error: {e}")
                retry = input("Retry this match? (y/n): ")
                if retry.lower() == 'y':
                    i -= 1  # Retry this match
    
    def enter_matchday_results(self, matchday: int):
        """Enter results for all matches in a matchday"""
        print(f"\n{'='*70}")
        print(f"ENTERING MATCHDAY {matchday} RESULTS")
        print(f"{'='*70}")
        
        matchday_matches = [m for m in self.matches if m.matchday == matchday and not m.played]
        
        if not matchday_matches:
            print(f"No unplayed matches found for matchday {matchday}")
            print(f"\nDebug info:")
            print(f"  Total matches in database: {len(self.matches)}")
            print(f"  Matches for matchday {matchday}: {len([m for m in self.matches if m.matchday == matchday])}")
            already_played = [m for m in self.matches if m.matchday == matchday and m.played]
            if already_played:
                print(f"  Already played matches: {len(already_played)}")
            return
        
        print(f"Found {len(matchday_matches)} unplayed matches for matchday {matchday}\n")
        
        for i, match in enumerate(matchday_matches, 1):
            print(f"\n--- Match {i}/{len(matchday_matches)} ---")
            print(f"{match.home_team} vs {match.away_team}")
            
            while True:
                try:
                    home_score_input = input(f"{match.home_team} score: ").strip()
                    away_score_input = input(f"{match.away_team} score: ").strip()
                    
                    # Convert to integers
                    home_score = int(home_score_input)
                    away_score = int(away_score_input)
                    
                    if home_score < 0 or away_score < 0:
                        print("❌ Scores must be non-negative! Please try again.")
                        continue
                    
                    # Verify teams exist in database - use fuzzy matching!
                    actual_home_team = self.find_team_fuzzy(match.home_team)
                    if not actual_home_team:
                        print(f"❌ ERROR: Home team '{match.home_team}' not found in database!")
                        print(f"Available teams: {list(self.teams.keys())}")
                        break
                    
                    actual_away_team = self.find_team_fuzzy(match.away_team)
                    if not actual_away_team:
                        print(f"❌ ERROR: Away team '{match.away_team}' not found in database!")
                        print(f"Available teams: {list(self.teams.keys())}")
                        break
                    
                    # Set result
                    match.set_result(home_score, away_score)
                    
                    # Update team statistics using the actual team names from database
                    self.teams[actual_home_team].update_stats(home_score, away_score)
                    self.teams[actual_away_team].update_stats(away_score, home_score)
                    
                    print(f"✓ Result recorded: {match.home_team} {home_score}-{away_score} {match.away_team}")
                    break
                
                except ValueError as e:
                    print(f"❌ Please enter valid integer scores! (Error: {e})")
                except KeyError as e:
                    print(f"❌ ERROR: Team not found in database: {e}")
                    print(f"Available teams: {list(self.teams.keys())}")
                    break
                except Exception as e:
                    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
                    print("Skipping this match. Please report this issue.")
                    break
        
        self.current_matchday = max(self.current_matchday, matchday)
        print(f"\n✓ All results for matchday {matchday} have been entered")
    
    def get_standings(self) -> List[Team]:
        """Get current standings sorted by points, goal difference, and goals scored"""
        return sorted(
            self.teams.values(),
            key=lambda t: (t.points, t.goal_difference, t.goals_for),
            reverse=True
        )
    
    def display_standings(self):
        """Display the current standings table"""
        standings = self.get_standings()
        
        print(f"\n{'='*90}")
        print(f"{self.competition_name.upper()} - STANDINGS (After Matchday {self.current_matchday})")
        print(f"{'='*90}")
        print(f"{'Pos':<4} {'Team':<30} {'MP':<4} {'W':<4} {'D':<4} {'L':<4} {'GF':<4} {'GA':<4} {'GD':<5} {'Pts':<4}")
        print("-" * 90)
        
        for i, team in enumerate(standings, 1):
            print(f"{i:<4} {team.name:<30} {team.matches_played:<4} {team.wins:<4} "
                  f"{team.draws:<4} {team.losses:<4} {team.goals_for:<4} {team.goals_against:<4} "
                  f"{team.goal_difference:+5} {team.points:<4}")
        
        print("="*90)
    
    def save_to_file(self):
        """Save database to JSON file"""
        data = {
            'competition_name': self.competition_name,
            'current_matchday': self.current_matchday,
            'teams': {name: team.to_dict() for name, team in self.teams.items()},
            'matches': [match.to_dict() for match in self.matches]
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Database saved to {self.data_file}")
    
    def load_from_file(self):
        """Load database from JSON file"""
        if not os.path.exists(self.data_file):
            print(f"No saved data found for {self.competition_name}")
            return False
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.competition_name = data['competition_name']
        self.current_matchday = data['current_matchday']
        
        # Load teams
        for name, team_data in data['teams'].items():
            team = Team(team_data['name'], team_data['country'])
            team.matches_played = team_data['matches_played']
            team.wins = team_data['wins']
            team.draws = team_data['draws']
            team.losses = team_data['losses']
            team.goals_for = team_data['goals_for']
            team.goals_against = team_data['goals_against']
            team.points = team_data['points']
            self.teams[name] = team
        
        # Load matches
        for match_data in data['matches']:
            match = Match(match_data['home_team'], match_data['away_team'], match_data['matchday'])
            if match_data['played']:
                match.set_result(match_data['home_score'], match_data['away_score'])
            self.matches.append(match)
        
        print(f"✓ Database loaded from {self.data_file}")
        return True


def main_menu():
    """Display and handle main menu"""
    print("\n" + "="*70)
    print("FOOTBALL DATABASE MANAGEMENT SYSTEM")
    print("="*70)
    print("1. Create new competition database")
    print("2. Load existing competition database")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    return choice


def competition_menu(db: FootballDatabase):
    """Display and handle competition-specific menu"""
    while True:
        print("\n" + "="*70)
        print(f"{db.competition_name.upper()} - MENU")
        print("="*70)
        print("1. View current standings")
        print("2. Enter matchday calendar")
        print("3. Enter matchday results")
        print("4. View all matches")
        print("5. Save database")
        print("6. Export standings to file")
        print("7. Return to main menu")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            db.display_standings()
        
        elif choice == '2':
            matchday = int(input("Enter matchday number: "))
            db.enter_matchday_calendar(matchday)
        
        elif choice == '3':
            matchday = int(input("Enter matchday number: "))
            db.enter_matchday_results(matchday)
            db.display_standings()
        
        elif choice == '4':
            print("\n" + "="*70)
            print("ALL MATCHES")
            print("="*70)
            for match in sorted(db.matches, key=lambda m: (m.matchday, m.home_team)):
                if match.played:
                    print(f"MD{match.matchday}: {match.home_team} {match.home_score}-{match.away_score} {match.away_team}")
                else:
                    print(f"MD{match.matchday}: {match.home_team} vs {match.away_team} (Not played)")
        
        elif choice == '5':
            db.save_to_file()
        
        elif choice == '6':
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
        
        elif choice == '7':
            save = input("Save before exiting? (y/n): ")
            if save.lower() == 'y':
                db.save_to_file()
            break
        
        else:
            print("Invalid choice!")


def main():
    """Main application entry point"""
    print("Welcome to the Football Database Management System!")
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            comp_name = input("\nEnter competition name (e.g., 'Champions League 2024-25'): ").strip()
            db = FootballDatabase(comp_name)
            
            # Ask about automatic team fetching
            if 'champions league' in comp_name.lower():
                fetch = input("\nAttempt to automatically fetch team names? (y/n): ").lower()
                if fetch == 'y':
                    fetched_teams = db.fetch_champions_league_teams()
                    db.verify_and_edit_teams(fetched_teams)
                else:
                    num_teams = int(input("How many teams? "))
                    db.add_manual_teams(num_teams)
            else:
                num_teams = int(input("How many teams? "))
                db.add_manual_teams(num_teams)
            
            competition_menu(db)
        
        elif choice == '2':
            comp_name = input("\nEnter competition name to load: ").strip()
            db = FootballDatabase(comp_name)
            if db.load_from_file():
                competition_menu(db)
        
        elif choice == '3':
            print("\nThank you for using the Football Database Management System!")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
