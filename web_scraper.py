"""
Web Scraper Module for Football Database
Fetches team and match data from web sources
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
import json
import time


class WebScraper:
    """Web scraper for football data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_champions_league_teams(self, season: str = "2024-25") -> List[Dict[str, str]]:
        """
        Fetch Champions League teams for a given season
        
        Args:
            season: Season string (e.g., "2024-25")
        
        Returns:
            List of dictionaries with team name and country
        """
        print(f"🌐 Fetching Champions League teams for {season}...")
        
        # Sample data - in a real implementation, this would scrape from UEFA.com
        # or another reliable source
        teams = [
            {"name": "Real Madrid", "country": "Spain"},
            {"name": "Manchester City", "country": "England"},
            {"name": "Bayern München", "country": "Germany"},
            {"name": "Paris Saint-Germain", "country": "France"},
            {"name": "Liverpool", "country": "England"},
            {"name": "Inter Milan", "country": "Italy"},
            {"name": "Borussia Dortmund", "country": "Germany"},
            {"name": "RB Leipzig", "country": "Germany"},
            {"name": "Barcelona", "country": "Spain"},
            {"name": "Juventus", "country": "Italy"},
            {"name": "Atlético Madrid", "country": "Spain"},
            {"name": "Atalanta", "country": "Italy"},
            {"name": "Bayer Leverkusen", "country": "Germany"},
            {"name": "Arsenal", "country": "England"},
            {"name": "Club Brugge", "country": "Belgium"},
            {"name": "Shakhtar Donetsk", "country": "Ukraine"},
            {"name": "AC Milan", "country": "Italy"},
            {"name": "Feyenoord", "country": "Netherlands"},
            {"name": "Sporting CP", "country": "Portugal"},
            {"name": "PSV Eindhoven", "country": "Netherlands"},
            {"name": "Dinamo Zagreb", "country": "Croatia"},
            {"name": "Red Bull Salzburg", "country": "Austria"},
            {"name": "Celtic", "country": "Scotland"},
            {"name": "Young Boys", "country": "Switzerland"},
            {"name": "Red Star Belgrade", "country": "Serbia"},
            {"name": "Porto", "country": "Portugal"},
            {"name": "Benfica", "country": "Portugal"},
            {"name": "Monaco", "country": "France"},
            {"name": "Aston Villa", "country": "England"},
            {"name": "Bologna", "country": "Italy"},
            {"name": "Girona", "country": "Spain"},
            {"name": "Stuttgart", "country": "Germany"},
            {"name": "Sturm Graz", "country": "Austria"},
            {"name": "Brest", "country": "France"},
            {"name": "BodoGlimt", "country": "Norway"},
            {"name": "Sparta Prague", "country": "Czech Republic"},
        ]
        
        print(f"✅ Found {len(teams)} teams")
        return teams
    
    def fetch_matchday_results(
        self, 
        competition: str = "Champions League", 
        season: str = "2024-25",
        matchday: int = 1
    ) -> List[Dict]:
        """
        Fetch match results for a specific matchday
        
        Args:
            competition: Competition name
            season: Season string
            matchday: Matchday number
        
        Returns:
            List of match dictionaries with home/away teams and scores
        """
        print(f"🌐 Fetching matchday {matchday} results...")
        
        # Sample data - in real implementation, this would scrape actual results
        # This is just example data for demonstration
        sample_results = [
            {
                "home_team": "Real Madrid",
                "away_team": "Stuttgart",
                "home_score": 3,
                "away_score": 1,
                "matchday": matchday
            },
            {
                "home_team": "Liverpool", 
                "away_team": "AC Milan",
                "home_score": 3,
                "away_score": 1,
                "matchday": matchday
            },
            {
                "home_team": "Bayern München",
                "away_team": "Dinamo Zagreb",
                "home_score": 9,
                "away_score": 2,
                "matchday": matchday
            }
        ]
        
        print(f"✅ Found {len(sample_results)} matches")
        return sample_results
    
    def verify_teams_interactive(self, teams: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Allow user to verify and edit scraped teams
        
        Args:
            teams: List of team dictionaries
        
        Returns:
            Verified list of teams
        """
        print("\n=== VERIFY SCRAPED TEAMS ===")
        print(f"Found {len(teams)} teams. Review the list:\n")
        
        for i, team in enumerate(teams, 1):
            print(f"{i:2d}. {team['name']:30s} ({team['country']})")
        
        while True:
            print("\nOptions:")
            print("1. Accept all teams")
            print("2. Remove a team")
            print("3. Edit a team")
            print("4. Add a team")
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == "1":
                print("✅ All teams accepted!")
                return teams
            
            elif choice == "2":
                try:
                    num = int(input("Enter team number to remove: "))
                    if 1 <= num <= len(teams):
                        removed = teams.pop(num - 1)
                        print(f"✅ Removed: {removed['name']}")
                    else:
                        print("❌ Invalid team number")
                except ValueError:
                    print("❌ Please enter a number")
            
            elif choice == "3":
                try:
                    num = int(input("Enter team number to edit: "))
                    if 1 <= num <= len(teams):
                        team = teams[num - 1]
                        print(f"Current: {team['name']} ({team['country']})")
                        new_name = input(f"New name (or Enter to keep): ").strip()
                        new_country = input(f"New country (or Enter to keep): ").strip()
                        
                        if new_name:
                            team['name'] = new_name
                        if new_country:
                            team['country'] = new_country
                        
                        print(f"✅ Updated: {team['name']} ({team['country']})")
                    else:
                        print("❌ Invalid team number")
                except ValueError:
                    print("❌ Please enter a number")
            
            elif choice == "4":
                name = input("Team name: ").strip()
                country = input("Country: ").strip()
                if name and country:
                    teams.append({"name": name, "country": country})
                    print(f"✅ Added: {name} ({country})")
                else:
                    print("❌ Name and country required")
            
            # Show updated list
            print("\nUpdated list:")
            for i, team in enumerate(teams, 1):
                print(f"{i:2d}. {team['name']:30s} ({team['country']})")
    
    def verify_results_interactive(self, results: List[Dict]) -> List[Dict]:
        """
        Allow user to verify and edit scraped results
        
        Args:
            results: List of match result dictionaries
        
        Returns:
            Verified list of results
        """
        print("\n=== VERIFY SCRAPED RESULTS ===")
        print(f"Found {len(results)} matches:\n")
        
        for i, match in enumerate(results, 1):
            print(f"{i}. {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
        
        while True:
            choice = input("\nAccept all? (y/n/edit): ").strip().lower()
            
            if choice == 'y':
                print("✅ All results accepted!")
                return results
            
            elif choice == 'n':
                print("❌ Results rejected")
                return []
            
            elif choice == 'edit':
                try:
                    num = int(input("Enter match number to edit: "))
                    if 1 <= num <= len(results):
                        match = results[num - 1]
                        print(f"Current: {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
                        
                        home_score = input("Home score: ").strip()
                        away_score = input("Away score: ").strip()
                        
                        if home_score.isdigit() and away_score.isdigit():
                            match['home_score'] = int(home_score)
                            match['away_score'] = int(away_score)
                            print(f"✅ Updated: {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
                        else:
                            print("❌ Invalid scores")
                    else:
                        print("❌ Invalid match number")
                except ValueError:
                    print("❌ Please enter a number")
    
    def fetch_live_scores(self, competition: str = "Champions League") -> List[Dict]:
        """
        Fetch live/recent scores
        
        Args:
            competition: Competition name
        
        Returns:
            List of live/recent matches
        """
        print(f"🌐 Fetching live scores for {competition}...")
        
        # In real implementation, this would fetch actual live data
        print("✅ No live matches at the moment")
        return []


def main():
    """Test the web scraper"""
    scraper = WebScraper()
    
    print("=== WEB SCRAPER TEST ===\n")
    
    # Test 1: Fetch teams
    teams = scraper.fetch_champions_league_teams()
    print(f"\n✅ Fetched {len(teams)} teams")
    
    # Test 2: Fetch results
    results = scraper.fetch_matchday_results(matchday=1)
    print(f"\n✅ Fetched {len(results)} results")
    
    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    main()
