"""
GitHub Contribution Graph Art Generator
Krijon commits ne datat e duhura per te shkruar tekst ne contribution graph.
Ndryshoni TEXT = "..." per tekst tuaj.
"""

import subprocess
import os
from datetime import datetime, timedelta

# ─── KONFIGURIM ────────────────────────────────────────────
TEXT     = "HIRE ME"   # Teksti qe doni te shfaqet
COMMITS_PER_CELL = 5   # Sa commits per cdo "pixel" (me shume = me e gjelbër)
# ────────────────────────────────────────────────────────────

# Fonti pixel 5×N per çdo shkronje
FONT = {
    'A': [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
    'B': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,1,0]],
    'C': [[0,1,1],[1,0,0],[1,0,0],[1,0,0],[0,1,1]],
    'D': [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
    'E': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,1,1]],
    'F': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,0,0]],
    'G': [[0,1,1],[1,0,0],[1,0,1],[1,0,1],[0,1,1]],
    'H': [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
    'I': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
    'J': [[0,0,1],[0,0,1],[0,0,1],[1,0,1],[0,1,0]],
    'K': [[1,0,1],[1,1,0],[1,0,0],[1,1,0],[1,0,1]],
    'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
    'M': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
    'N': [[1,0,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1]],
    'O': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'P': [[1,1,0],[1,0,1],[1,1,0],[1,0,0],[1,0,0]],
    'Q': [[0,1,0],[1,0,1],[1,0,1],[1,1,1],[0,1,1]],
    'R': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
    'S': [[0,1,1],[1,0,0],[0,1,0],[0,0,1],[1,1,0]],
    'T': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    'U': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
    'V': [[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0]],
    'W': [[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1]],
    'X': [[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
    'Y': [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0]],
    'Z': [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],
    ' ': [[0],[0],[0],[0],[0]],
    '!': [[0,1],[0,1],[0,1],[0,0],[0,1]],
    '.': [[0],[0],[0],[0],[1]],
}


def text_to_grid(text: str) -> list[list[int]]:
    """Kthen tekstin ne nje grid 5-rresht."""
    grid = [[] for _ in range(5)]
    for idx, ch in enumerate(text.upper()):
        letter = FONT.get(ch, FONT[' '])
        for row in range(5):
            grid[row].extend(letter[row])
            # shto 1 kolonë hapësire midis shkronjave (jo pas të fundit)
            if idx < len(text) - 1:
                grid[row].append(0)
    return grid


def get_start_sunday(offset_weeks: int = 0) -> datetime:
    """Gjen të dielën e parë ~52 javë më parë + offset."""
    today = datetime.now()
    start = today - timedelta(weeks=52 - offset_weeks)
    while start.weekday() != 6:   # 6 = e diel (Sunday)
        start -= timedelta(days=1)
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def make_commits(date: datetime, n: int = COMMITS_PER_CELL):
    """Bën n commits bosh ne daten e dhënë."""
    date_str = date.strftime("%Y-%m-%dT12:00:00")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"]    = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    for i in range(n):
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", f"art {date_str} #{i}"],
            env=env,
            check=True,
            capture_output=True,
        )


def main():
    grid = text_to_grid(TEXT)
    total_cols  = len(grid[0])
    total_weeks = 52

    # Qendërzim horizontal
    offset = max(0, (total_weeks - total_cols) // 2)
    start_sunday = get_start_sunday(offset_weeks=offset)

    print(f"Teksti: '{TEXT}'")
    print(f"Gjerësia grid: {total_cols} kolona")
    print(f"Duke filluar nga java: {start_sunday.date()}")

    # Git config
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name",  "GitHub Action"],      check=True)

    commits_made = 0
    for col in range(total_cols):
        for row in range(5):           # rreshtat 0-4 = E hënë - E premte
            if grid[row][col] == 1:
                date = start_sunday + timedelta(weeks=col, days=row + 1)
                make_commits(date)
                commits_made += COMMITS_PER_CELL

    print(f"\n✅ Gati! {commits_made} commits u krijuan.")
    print("Bëj 'git push' ose lëre workflow-in ta bëjë automatikisht.")


if __name__ == "__main__":
    main()
