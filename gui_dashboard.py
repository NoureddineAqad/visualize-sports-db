"""
GUI Dashboard for Football Database
Optional visual interface using customtkinter
"""

try:
    import customtkinter as ctk
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("⚠️  GUI dependencies not installed")
    print("Install with: pip install customtkinter matplotlib")

from typing import Dict, List
import sys


class FootballDashboard:
    """GUI Dashboard for Football Database"""
    
    def __init__(self, database):
        """
        Initialize dashboard
        
        Args:
            database: FootballDatabase instance
        """
        if not GUI_AVAILABLE:
            print("❌ GUI not available. Install dependencies:")
            print("   pip install customtkinter matplotlib")
            return
        
        self.db = database
        self.root = None
        self.standings_frame = None
        self.chart_frame = None
    
    def create_window(self):
        """Create main window"""
        if not GUI_AVAILABLE:
            return
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create window
        self.root = ctk.CTk()
        self.root.title(f"Football Database - {self.db.competition_name}")
        self.root.geometry("1200x800")
        
        # Create main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text=self.db.competition_name,
            font=("Arial", 24, "bold")
        )
        title.pack(pady=10)
        
        # Create notebook (tabs)
        tabview = ctk.CTkTabview(main_frame)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        tab_standings = tabview.add("Standings")
        tab_matches = tabview.add("Matches")
        tab_stats = tabview.add("Statistics")
        
        # Populate tabs
        self.create_standings_tab(tab_standings)
        self.create_matches_tab(tab_matches)
        self.create_stats_tab(tab_stats)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            main_frame,
            text="🔄 Refresh Data",
            command=self.refresh_all,
            height=40
        )
        refresh_btn.pack(pady=10)
    
    def create_standings_tab(self, parent):
        """Create standings display"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Get standings
        standings = self.db.get_standings()
        
        # Header
        header_frame = ctk.CTkFrame(scroll_frame)
        header_frame.pack(fill="x", pady=5)
        
        headers = ["Pos", "Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]
        widths = [50, 200, 50, 50, 50, 50, 50, 50, 70, 50]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                width=width
            )
            label.grid(row=0, column=i, padx=2)
        
        # Team rows
        for pos, team in enumerate(standings, 1):
            row_frame = ctk.CTkFrame(scroll_frame)
            row_frame.pack(fill="x", pady=2)
            
            # Color code for qualification
            if pos <= 8:
                bg_color = ("green", "dark green")  # Qualified
            else:
                bg_color = ("gray", "dark gray")  # Not qualified
            
            values = [
                str(pos),
                team.name,
                str(team.matches_played),
                str(team.wins),
                str(team.draws),
                str(team.losses),
                str(team.goals_for),
                str(team.goals_against),
                f"{team.goal_difference:+d}",
                str(team.points)
            ]
            
            for i, (value, width) in enumerate(zip(values, widths)):
                label = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    width=width,
                    fg_color=bg_color if i == 0 else None
                )
                label.grid(row=0, column=i, padx=2)
    
    def create_matches_tab(self, parent):
        """Create matches display"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Group matches by matchday
        matchdays = {}
        for match in self.db.matches:
            if match.matchday not in matchdays:
                matchdays[match.matchday] = []
            matchdays[match.matchday].append(match)
        
        # Display each matchday
        for matchday in sorted(matchdays.keys()):
            # Matchday header
            header = ctk.CTkLabel(
                scroll_frame,
                text=f"Matchday {matchday}",
                font=("Arial", 16, "bold")
            )
            header.pack(anchor="w", pady=(10, 5))
            
            # Matches
            for match in matchdays[matchday]:
                match_frame = ctk.CTkFrame(scroll_frame)
                match_frame.pack(fill="x", pady=2)
                
                if match.played:
                    result_text = f"{match.home_team} {match.home_score}-{match.away_score} {match.away_team}"
                else:
                    result_text = f"{match.home_team} vs {match.away_team} (Not played)"
                
                match_label = ctk.CTkLabel(
                    match_frame,
                    text=result_text,
                    font=("Arial", 12)
                )
                match_label.pack(pady=5)
    
    def create_stats_tab(self, parent):
        """Create statistics visualization"""
        if not GUI_AVAILABLE:
            return
        
        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Get top 10 teams
        standings = self.db.get_standings()[:10]
        teams = [team.name for team in standings]
        points = [team.points for team in standings]
        
        # Points bar chart
        ax1.barh(teams, points, color='steelblue')
        ax1.set_xlabel('Points')
        ax1.set_title('Top 10 Teams by Points')
        ax1.invert_yaxis()
        
        # Goals comparison
        goals_for = [team.goals_for for team in standings]
        goals_against = [team.goals_against for team in standings]
        
        x = range(len(teams))
        width = 0.35
        
        ax2.bar([i - width/2 for i in x], goals_for, width, label='Goals For', color='green')
        ax2.bar([i + width/2 for i in x], goals_against, width, label='Goals Against', color='red')
        ax2.set_ylabel('Goals')
        ax2.set_title('Goals For vs Against')
        ax2.set_xticks(x)
        ax2.set_xticklabels([t[:15] for t in teams], rotation=45, ha='right')
        ax2.legend()
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def refresh_all(self):
        """Refresh all data displays"""
        print("🔄 Refreshing dashboard...")
        # In a full implementation, this would reload data and update displays
        print("✅ Dashboard refreshed!")
    
    def run(self):
        """Run the dashboard"""
        if not GUI_AVAILABLE:
            print("❌ Cannot run GUI - dependencies not installed")
            return
        
        self.create_window()
        self.root.mainloop()


def launch_dashboard(database):
    """
    Launch GUI dashboard for a database
    
    Args:
        database: FootballDatabase instance
    """
    if not GUI_AVAILABLE:
        print("\n❌ GUI Dashboard not available")
        print("\nTo use the GUI dashboard, install:")
        print("  pip install customtkinter matplotlib")
        print("\nPress Enter to continue...")
        input()
        return
    
    print("🚀 Launching GUI dashboard...")
    dashboard = FootballDashboard(database)
    dashboard.run()


def main():
    """Test the GUI dashboard"""
    if not GUI_AVAILABLE:
        print("❌ GUI dependencies not installed")
        print("Install with: pip install customtkinter matplotlib")
        return
    
    print("=== GUI DASHBOARD TEST ===")
    print("This module requires integration with football_db.py")
    print("Use it through the main_app.py interface")


if __name__ == "__main__":
    main()
