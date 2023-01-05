# Chess with AI

## Java

#### Contents

- Chess GUI with Java Swing components
- Chess Game with individual classes

#### File System

- Game Folder
  - ChessFrame - Manages GUI of chess board
  - ChessGame - Manages the state of the chess game
  - Square - Represents one square on a chess board, used in both ChessFrame and ChessGame
- Pieces Folder
- Pawn, Knight, Bishop, Rook, Queen, King - Represent one instance of each piece, used in ChessGame and ChessFrame

## Python

#### Contents

- Chess Game in Python
- AI uses the minmax algorithm to find the best moves
  - Alpha-Beta pruning is implemented to avoid traversing uncessecary paths
- AI that provides a move given a depth using original Chess Game
- AI that uses python-chess library for testing

#### File System

- ChessAI - AI that uses functions built from ChessGame
- AI - AI using python-chess library
- ChessPieces - Functions that maintain game state in chess game
- ChessGame - Main handler for maintaining the chess game, works with ChessPieces functions

#### Required libraries

- python-chess
- numpy
