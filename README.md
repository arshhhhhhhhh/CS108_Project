# Mini Game Hub

A final project for the CS108 course (Spr 2026)

>A secure, multi-user game hub that integrates Bash scripting for authentication and Python (Pygame) for gameplay.
>Two authenticated players select a game from a menu, play via a graphical interface, and have their results recorded on a persistent leaderboard.

## Usage

The project Mini Game Hub is run using the `main.sh` file as follows:

```bash
bash main.sh
```

This will prompt for usernames and passwords of two players for authentication. After authentication, `main.sh` will call `game.py` as:
```bash
python3 game.py <username1> <username2>
```

game.py receives the two authenticated usernames and manages the full Python-side flow: the game menu, gameplay, post-game recording, and analytics.

## Features

Follwing features have been implemented:

**main.sh**
- User authentication system with login and registration via a Bash shell interface
- Password hashing using [SHA-256](https://www.simplilearn.com/tutorials/cyber-security-tutorial/sha-256-algorithm) for secure credential storage
- Player credentials stored and validated against a TSV-based user database
- Duplicate login prevention ensuring both players must use distinct usernames
- Automatic prompt to register when an unrecognized username is entered
- Input validation rejecting empty usernames or passwords

**game.py**
- Multi-game platform supporting Tic-Tac-Toe, Othello, and Connect 4 from a unified main menu
- Two-player local multiplayer with named player profiles
- Turn-switching feature allowing players to swap sides from the main menu
- Object-oriented architecture with a shared base `Game` class extended by each game
- Pygame-powered graphical interface running at 60 FPS with custom background and image assets
- Custom font rendering for player names and piece counts in the game UI
- Graceful exit handling at any point during gameplay or navigation


**tictactoe.py / connect4.py / othello.py**
- **Connect 4 & Tic-Tac-Toe**: Win detection across all four directions — horizontal, vertical, and both diagonals — using efficient sliding window computation over NumPy arrays
- **Othello**: Win detection based on piece count comparison, with support for early termination when no valid moves remain for either player
- Draw detection when the board is completely filled or no valid move left
- Real-time hover preview showing where a piece will be placed before committing a move
- Visual win indicators highlighting the winning line on the board
- Live piece counters displayed on-screen for both players throughout the game
- In-game reset functionality to restart a match without returning to the main menu
- Game history logging to a CSV file with player names, result, date, and game type