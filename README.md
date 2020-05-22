# tetris-opl
Tetris implementation in pygame, following some but definitely not all of Tetris guidelines.
Requires Python 3.x and pygame 1.9.3

# Patch Notes
Fixed:
- corrected code to initialize empty grid, put it in a function for easy resetting.

Added:
- Collision
- Locking
- Line clearing
- Scoring
- Levels (and increased drop speed with level). Formula used is from official Tetris, but we can use a less complex one if desired.
- Soft drop speed changes based on level
- Game Over
- Restart after game over with spacebar

To-Do:
- Create lock delay
- Use random bag shuffle instead of pure random choice
- Next block display
- Wall kicks for nicer rotation
