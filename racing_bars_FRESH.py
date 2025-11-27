"""
Racing bars animation module for Champions League standings visualization.
Works with GUI dashboard - accepts pre-processed snapshot data.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
import numpy as np
from pathlib import Path
from PIL import Image

def load_team_logo(team_name, logo_dir='logos'):
    """
    Load team logo from logos directory.
    
    Args:
        team_name: Name of the team
        logo_dir: Directory containing logo files
    
    Returns:
        numpy array of logo image or None if not found
    """
    logo_path = Path(logo_dir)
    if not logo_path.exists():
        return None
    
    # Try different variations of the team name
    for name in [team_name, team_name.replace(' ', '_'), team_name.lower(), team_name.lower().replace(' ', '_')]:
        for ext in ['.png', '.svg', '.jpg', '.jpeg']:
            logo_file = logo_path / f"{name}{ext}"
            if logo_file.exists():
                try:
                    if ext in ['.png', '.jpg', '.jpeg']:
                        img = Image.open(logo_file)
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        return np.array(img)
                except Exception as e:
                    print(f"   ⚠️  Error loading {logo_file}: {e}")
                    pass
    return None

# Rank-based colors for qualification zones
RANK_COLORS = {
    'qualified': '#2ecc71',      # Green - Top 8 (Direct qualification)
    'playoff': '#f39c12',        # Orange - 9-24 (Playoff)
    'eliminated': '#e74c3c'      # Red - 25-36 (Eliminated)
}

# Official team colors
TEAM_COLORS = {
    'Liverpool': '#C8102E', 'Manchester City': '#6CABDD', 'Arsenal': '#EF0107',
    'Aston Villa': '#95BFE5', 'Real Madrid': '#FEBE10', 'Barcelona': '#A50044',
    'Atletico Madrid': '#CB3524', 'Girona': '#CC0000', 'Bayern Munich': '#DC052D',
    'Bayer Leverkusen': '#E32221', 'Borussia Dortmund': '#FDE100', 'RB Leipzig': '#DD0741',
    'VfB Stuttgart': '#E32219', 'Inter Milan': '#0068A8', 'AC Milan': '#FB090B',
    'Juventus': '#000000', 'Atalanta': '#1B5297', 'Bologna': '#001E8C',
    'PSG': '#004170', 'Paris Saint-Germain': '#004170', 'Monaco': '#E1000F',
    'Lille': '#D91A21', 'Brest': '#E2001A', 'Benfica': '#FF0000', 'Porto': '#003D7B',
    'Sporting CP': '#00683C', 'PSV Eindhoven': '#FF0000', 'Feyenoord': '#E30613',
    'Celtic': '#00A650', 'Club Brugge': '#0053A0', 'Shakhtar Donetsk': '#FF6600',
    'Dinamo Zagreb': '#005BAC', 'Red Star Belgrade': '#E4032E', 'Young Boys': '#FFED00',
    'Salzburg': '#C40C29', 'Sparta Prague': '#9C2A3C', 'Slovan Bratislava': '#0066CC',
    'Sturm Graz': '#000000',
}

# Team initials
TEAM_INITIALS = {
    'Liverpool': 'LIV', 'Manchester City': 'MCI', 'Arsenal': 'ARS', 'Aston Villa': 'AVL',
    'Real Madrid': 'RMA', 'Barcelona': 'BAR', 'Atletico Madrid': 'ATM', 'Girona': 'GIR',
    'Bayern Munich': 'BAY', 'Bayer Leverkusen': 'LEV', 'Borussia Dortmund': 'BVB',
    'RB Leipzig': 'RBL', 'VfB Stuttgart': 'STU', 'Inter Milan': 'INT', 'AC Milan': 'MIL',
    'Juventus': 'JUV', 'Atalanta': 'ATA', 'Bologna': 'BOL', 'PSG': 'PSG',
    'Paris Saint-Germain': 'PSG', 'Monaco': 'MON', 'Lille': 'LIL', 'Brest': 'BRE',
    'Benfica': 'BEN', 'Porto': 'POR', 'Sporting CP': 'SCP', 'PSV Eindhoven': 'PSV',
    'Feyenoord': 'FEY', 'Celtic': 'CEL', 'Club Brugge': 'BRU', 'Shakhtar Donetsk': 'SHA',
    'Dinamo Zagreb': 'DZG', 'Red Star Belgrade': 'RSB', 'Young Boys': 'YBB',
    'Salzburg': 'SAL', 'Sparta Prague': 'SPA', 'Slovan Bratislava': 'SLO', 'Sturm Graz': 'STG',
}

class RacingBars:
    """Creates animated racing bar charts for Champions League standings."""
    
    def __init__(self, snapshots, fps=20, duration_per_round=5.0, repeat=False, max_teams=None):
        """
        Initialize animator with snapshot data from GUI.
        
        Args:
            snapshots: List of snapshot dicts with format:
                       [{'round': X, 'standings': [{'name': ..., 'points': ..., 'gd': ...}, ...]}, ...]
            fps: Frames per second
            duration_per_round: Duration in seconds for each round
            repeat: Whether to loop the animation (default: False - stops after last round)
            max_teams: Maximum number of teams to display (None = all teams, 8/16/24 = top N)
        """
        self.snapshots = snapshots
        self.fps = fps
        self.duration_per_round = duration_per_round
        self.frames_per_round = int(fps * duration_per_round)
        self.repeat = repeat
        self.max_teams = max_teams
        
        # Figure and axes will be set by GUI
        self.fig = None
        self.ax = None
        
        # Load team logos
        self.logos = {}
        print("\n🖼️  Loading team logos...")
        if snapshots and len(snapshots) > 0:
            for team in snapshots[0]['standings']:
                name = team['name']
                logo = load_team_logo(name)
                self.logos[name] = logo
                if logo is not None:
                    print(f"   ✅ {name}")
        
        logos_count = sum(1 for l in self.logos.values() if l is not None)
        total_teams = len(self.logos)
        print(f"   📊 Loaded {logos_count}/{total_teams} logos")
        
        print(f"\n📊 RacingBars initialized: {len(snapshots)} snapshots, {self.frames_per_round} frames/round")
    
    def interpolate(self, snap1, snap2, progress):
        """
        Interpolate between two snapshots.
        - Positions: smooth interpolation for visual movement
        - Points/GD: NO interpolation - show actual values only
        
        Args:
            snap1: First snapshot
            snap2: Second snapshot  
            progress: 0.0 to 1.0
        """
        standings1 = {t['name']: (i, t) for i, t in enumerate(snap1['standings'])}
        standings2 = {t['name']: (i, t) for i, t in enumerate(snap2['standings'])}
        
        # Use snap2 data (the new state) - no fake intermediate values
        result = []
        for name in standings2.keys():
            if name in standings1:
                pos1, _ = standings1[name]
                pos2, data2 = standings2[name]
                
                result.append({
                    'name': name,
                    'position': pos1 + (pos2 - pos1) * progress,  # Smooth position movement
                    'points': data2.get('points', 0),              # Always show NEW points
                    'gd': data2.get('gd', 0)                       # Always show NEW gd
                })
        
        return sorted(result, key=lambda x: x['position'])
    
    def draw_frame(self, frame_num):
        """
        Draw a single frame - called by GUI's FuncAnimation.
        
        Args:
            frame_num: Frame number to draw
        """
        if self.ax is None:
            print("⚠️  Axes not set!")
            return
        
        self.ax.clear()
        self.ax.set_xlim(0, 180)  # Wide X axis
        self.ax.set_ylim(0, 120)  # TALLER Y axis for more spacing (was 100)
        self.ax.set_aspect('auto')  # Allow stretching to fill figure
        self.ax.axis('off')
        
        # Determine which snapshot and progress
        snap_idx = min(frame_num // self.frames_per_round, len(self.snapshots) - 1)
        frame_in_snap = frame_num % self.frames_per_round
        progress = frame_in_snap / self.frames_per_round
        
        # Get standings
        if snap_idx < len(self.snapshots) - 1:
            standings = self.interpolate(self.snapshots[snap_idx], self.snapshots[snap_idx + 1], progress)
            # Show the NEW round number (snap_idx + 1) since we're showing new data
            current_round = self.snapshots[snap_idx + 1]['round']
        else:
            standings = [{'name': t['name'], 'position': i, 
                         'points': t.get('points', 0), 'gd': t.get('gd', 0)}
                        for i, t in enumerate(self.snapshots[-1]['standings'])]
            current_round = self.snapshots[-1]['round']
        
        # Filter to show only top N teams if max_teams is set
        if self.max_teams is not None:
            standings = standings[:self.max_teams]
        
        # Title - adjusted for taller Y axis (120 instead of 100)
        title_text = f'AFTER ROUND {current_round}'
        if self.max_teams is not None:
            title_text += f' (Top {self.max_teams})'
        self.ax.text(5, 115, title_text,
                    fontsize=18, fontweight='bold', color='white', va='top')
        self.ax.text(5, 110, 'Champions League 2025-26',
                    fontsize=11, style='italic', color='#888888', va='top')
        
        # Layout - MORE VERTICAL SPACE (Y is now 0-120)
        num_teams = len(standings)
        top_y, bottom_y = 105, 5  # More usable vertical space
        row_height = (top_y - bottom_y) / num_teams
        max_points = max(s['points'] for s in standings) if standings else 1
        
        # WIDE LAYOUT: logos (x=15), bars (x=28-155), stats (x=162)
        logo_x = 15
        bar_start_x = 28
        bar_max_width = 127  # From x=28 to x=155
        stats_x = 162
        
        # Draw teams
        for team in standings:
            pos = team['position']
            y_center = top_y - (pos + 0.5) * row_height
            name = team['name']
            points = team['points']
            gd = team.get('gd', 0)
            
            # Color by rank
            rank = int(pos) + 1
            if rank <= 8:
                color = RANK_COLORS['qualified']
            elif rank <= 24:
                color = RANK_COLORS['playoff']
            else:
                color = RANK_COLORS['eliminated']
            
            # MAXIMUM logo size - 0.9 of row height, max 3.0
            radius = min(0.9 * row_height, 3.0)
            logo = self.logos.get(name)
            
            if logo is not None:
                # Display team logo at logo_x position
                try:
                    extent = [logo_x - radius, logo_x + radius,
                             y_center - radius, y_center + radius]
                    self.ax.imshow(logo, extent=extent, aspect='equal', zorder=10)
                except:
                    # Fallback to circle if logo display fails
                    circle = Circle((logo_x, y_center), radius, facecolor=color,
                                  edgecolor='white', linewidth=1.5, alpha=0.8)
                    self.ax.add_patch(circle)
                    initials = TEAM_INITIALS.get(name, name[:3].upper())
                    self.ax.text(logo_x, y_center, initials, fontsize=16, fontweight='bold',
                                color='white', ha='center', va='center')
            else:
                # Circle with initials if no logo - larger text
                circle = Circle((logo_x, y_center), radius, facecolor=color,
                              edgecolor='white', linewidth=1.5, alpha=0.8)
                self.ax.add_patch(circle)
                initials = TEAM_INITIALS.get(name, name[:3].upper())
                self.ax.text(logo_x, y_center, initials, fontsize=16, fontweight='bold',
                            color='white', ha='center', va='center')
            
            # THIN LINE - using full width available
            bar_width = (points / max_points) * bar_max_width if max_points > 0 else 0
            bar_height_val = row_height * 0.15
            
            rect = Rectangle((bar_start_x, y_center - bar_height_val/2), bar_width, bar_height_val,
                           facecolor=color, edgecolor='white', linewidth=1, alpha=0.9)
            self.ax.add_patch(rect)
        
        # FIXED POSITION STATS - only for positions 1, 8, and 24
        # Calculate fixed y positions for these ranks
        rank_positions = {}
        for team in standings:
            rank = int(team['position']) + 1
            if rank in [1, 8, 24]:
                rank_positions[rank] = team
        
        # Position 1 (top of direct qualification)
        if 1 in rank_positions:
            y_pos_1 = top_y - (0.5) * row_height
            team_1 = rank_positions[1]
            self.ax.text(stats_x, y_pos_1, f"{int(team_1['points'])} pts",
                        fontsize=11, fontweight='bold', color='#2ecc71',
                        va='center', ha='left', bbox=dict(boxstyle='round,pad=0.4', 
                        facecolor='black', edgecolor='#2ecc71', linewidth=2))
        
        # Position 8 (last direct qualification spot)
        if 8 in rank_positions:
            y_pos_8 = top_y - (7.5) * row_height
            team_8 = rank_positions[8]
            self.ax.text(stats_x, y_pos_8, f"{int(team_8['points'])} pts",
                        fontsize=11, fontweight='bold', color='#2ecc71',
                        va='center', ha='left', bbox=dict(boxstyle='round,pad=0.4',
                        facecolor='black', edgecolor='#2ecc71', linewidth=2))
        
        # Position 24 (last playoff spot)
        if 24 in rank_positions:
            y_pos_24 = top_y - (23.5) * row_height
            team_24 = rank_positions[24]
            self.ax.text(stats_x, y_pos_24, f"{int(team_24['points'])} pts",
                        fontsize=11, fontweight='bold', color='#f39c12',
                        va='center', ha='left', bbox=dict(boxstyle='round,pad=0.4',
                        facecolor='black', edgecolor='#f39c12', linewidth=2))
        
        # Force redraw
        if self.fig:
            try:
                self.fig.canvas.draw_idle()
                self.fig.canvas.flush_events()
            except:
                pass