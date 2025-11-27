"""
Monte Carlo Simulation Module for Football Database
Simulates tournament outcomes and calculates probabilities
"""

import random
from typing import Dict, List, Tuple
from collections import defaultdict
import copy


class MonteCarloSimulator:
    """Monte Carlo simulator for football tournaments"""
    
    def __init__(self, teams: Dict, matches: List):
        """
        Initialize simulator with current tournament state
        
        Args:
            teams: Dictionary of Team objects
            matches: List of Match objects
        """
        self.teams = teams
        self.matches = matches
        self.simulation_results = defaultdict(lambda: defaultdict(int))
    
    def simulate_match(self, home_team: str, away_team: str) -> Tuple[int, int]:
        """
        Simulate a single match between two teams
        
        Args:
            home_team: Home team name
            away_team: Away team name
        
        Returns:
            Tuple of (home_score, away_score)
        """
        # Get team strengths (based on current points)
        home_strength = self.teams[home_team].points + 10  # Home advantage
        away_strength = self.teams[away_team].points
        
        # Calculate expected goals based on strength
        home_expected = max(0.5, home_strength / 10)
        away_expected = max(0.5, away_strength / 10)
        
        # Simulate goals using Poisson-like distribution (simplified)
        home_score = max(0, int(random.gauss(home_expected, 1.5)))
        away_score = max(0, int(random.gauss(away_expected, 1.5)))
        
        return home_score, away_score
    
    def simulate_remaining_matches(self, teams_copy: Dict, matches_copy: List) -> Dict:
        """
        Simulate all remaining matches
        
        Args:
            teams_copy: Copy of teams dictionary
            matches_copy: Copy of matches list
        
        Returns:
            Updated teams dictionary after simulation
        """
        for match in matches_copy:
            if not match.played:
                # Simulate the match
                home_score, away_score = self.simulate_match(match.home_team, match.away_team)
                
                # Update match
                match.set_result(home_score, away_score)
                
                # Update team stats
                teams_copy[match.home_team].update_stats(home_score, away_score)
                teams_copy[match.away_team].update_stats(away_score, home_score)
        
        return teams_copy
    
    def run_single_simulation(self) -> Dict[str, int]:
        """
        Run a single complete simulation
        
        Returns:
            Dictionary mapping team names to final points
        """
        # Create deep copies
        teams_copy = {}
        for name, team in self.teams.items():
            teams_copy[name] = copy.deepcopy(team)
        
        matches_copy = [copy.deepcopy(match) for match in self.matches]
        
        # Simulate remaining matches
        teams_copy = self.simulate_remaining_matches(teams_copy, matches_copy)
        
        # Return final points
        return {name: team.points for name, team in teams_copy.items()}
    
    def run_simulations(self, n_simulations: int = 10000) -> Dict:
        """
        Run multiple simulations
        
        Args:
            n_simulations: Number of simulations to run
        
        Returns:
            Dictionary with simulation results and statistics
        """
        print(f"🎲 Running {n_simulations:,} Monte Carlo simulations...")
        
        # Track results
        final_positions = defaultdict(lambda: defaultdict(int))
        points_distribution = defaultdict(list)
        qualification_count = defaultdict(int)
        
        # Run simulations
        for i in range(n_simulations):
            if (i + 1) % 1000 == 0:
                print(f"  Progress: {i+1:,}/{n_simulations:,} ({100*(i+1)/n_simulations:.1f}%)")
            
            # Run single simulation
            final_points = self.run_single_simulation()
            
            # Sort teams by points
            sorted_teams = sorted(final_points.items(), key=lambda x: x[1], reverse=True)
            
            # Record final positions
            for position, (team_name, points) in enumerate(sorted_teams, 1):
                final_positions[team_name][position] += 1
                points_distribution[team_name].append(points)
                
                # Top 8 qualify (Champions League format)
                if position <= 8:
                    qualification_count[team_name] += 1
        
        print("✅ Simulations complete!\n")
        
        # Calculate statistics
        results = {
            'final_positions': dict(final_positions),
            'qualification_probability': {
                team: count / n_simulations * 100 
                for team, count in qualification_count.items()
            },
            'average_points': {
                team: sum(points) / len(points)
                for team, points in points_distribution.items()
            },
            'points_range': {
                team: (min(points), max(points))
                for team, points in points_distribution.items()
            },
            'n_simulations': n_simulations
        }
        
        return results
    
    def print_results(self, results: Dict):
        """
        Print simulation results in a formatted way
        
        Args:
            results: Results dictionary from run_simulations()
        """
        print("=" * 80)
        print(f"MONTE CARLO SIMULATION RESULTS ({results['n_simulations']:,} simulations)")
        print("=" * 80)
        
        # Sort teams by qualification probability
        sorted_teams = sorted(
            results['qualification_probability'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        print(f"\n{'Team':<30} {'Qual%':<8} {'Avg Pts':<10} {'Points Range'}")
        print("-" * 80)
        
        for team_name, qual_prob in sorted_teams:
            avg_points = results['average_points'][team_name]
            points_range = results['points_range'][team_name]
            
            print(f"{team_name:<30} {qual_prob:>6.1f}% {avg_points:>8.1f} "
                  f"{points_range[0]:>5d} - {points_range[1]:<5d}")
        
        print("\n" + "=" * 80)
        print("Top 8 teams qualify for knockout stage")
        print("=" * 80)
        
        # Show position probability for top teams
        print("\nPOSITION PROBABILITY (Top 5 Teams):\n")
        top_teams = sorted_teams[:5]
        
        print(f"{'Team':<25}", end="")
        for pos in range(1, 9):
            print(f" {pos:>6s}", end="")
        print()
        print("-" * 80)
        
        for team_name, _ in top_teams:
            print(f"{team_name:<25}", end="")
            pos_probs = results['final_positions'][team_name]
            total_sims = results['n_simulations']
            
            for pos in range(1, 9):
                prob = pos_probs.get(pos, 0) / total_sims * 100
                print(f" {prob:>5.1f}%", end="")
            print()
    
    def print_qualification_summary(self, results: Dict):
        """
        Print a summary of qualification probabilities
        
        Args:
            results: Results dictionary from run_simulations()
        """
        print("\n" + "=" * 60)
        print("QUALIFICATION PROBABILITY TIERS")
        print("=" * 60)
        
        qual_probs = results['qualification_probability']
        
        # Group by probability ranges
        certain = []      # > 95%
        very_likely = []  # 75-95%
        likely = []       # 50-75%
        possible = []     # 25-50%
        unlikely = []     # 5-25%
        very_unlikely = [] # < 5%
        
        for team, prob in qual_probs.items():
            if prob > 95:
                certain.append((team, prob))
            elif prob > 75:
                very_likely.append((team, prob))
            elif prob > 50:
                likely.append((team, prob))
            elif prob > 25:
                possible.append((team, prob))
            elif prob > 5:
                unlikely.append((team, prob))
            else:
                very_unlikely.append((team, prob))
        
        # Print each tier
        tiers = [
            ("🟢 CERTAIN (>95%)", certain),
            ("🔵 VERY LIKELY (75-95%)", very_likely),
            ("🟡 LIKELY (50-75%)", likely),
            ("🟠 POSSIBLE (25-50%)", possible),
            ("🔴 UNLIKELY (5-25%)", unlikely),
            ("⚫ VERY UNLIKELY (<5%)", very_unlikely)
        ]
        
        for tier_name, teams in tiers:
            if teams:
                print(f"\n{tier_name}")
                for team, prob in sorted(teams, key=lambda x: x[1], reverse=True):
                    print(f"  {team:<30} {prob:>6.1f}%")


def main():
    """Test the Monte Carlo simulator"""
    print("=== MONTE CARLO SIMULATOR TEST ===\n")
    print("This is a test module. Use it integrated with football_db.py")
    print("for actual simulations.\n")


if __name__ == "__main__":
    main()
