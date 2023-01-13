package Game;

import Pieces.*;

public class ChessBoard {

    private final Square[][] board;
    private boolean whiteTurn = true;

    //Creates a board digitally to represent and sets each piece up
    public ChessBoard() {
        board = new Square[8][8];
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                board[i][j] = new Square();
            }
        }
        board[0][0].setPiece(new Rook(0, 0, false));
        board[0][1].setPiece(new Knight(0, 1, false));
        board[0][2].setPiece(new Bishop(0, 2, false));
        board[0][3].setPiece(new Queen(0, 3, false));
        board[0][4].setPiece(new King(0, 4, false));
        board[0][5].setPiece(new Bishop(0, 5, false));
        board[0][6].setPiece(new Knight(0, 6, false));
        board[0][7].setPiece(new Rook(0, 7, false));
        for (int i = 0; i < 8; i++) {
            board[1][i].setPiece(new Pawn(1, i, false));
        }
        board[7][0].setPiece(new Rook(7, 0, true));
        board[7][1].setPiece(new Knight(7, 1, true));
        board[7][2].setPiece(new Bishop(7, 2, true));
        board[7][3].setPiece(new Queen(7, 3, true));
        board[7][4].setPiece(new King(7, 4, true));
        board[7][5].setPiece(new Bishop(7, 5, true));
        board[7][6].setPiece(new Knight(7, 6, true));
        board[7][7].setPiece(new Rook(7, 7, true));
        for (int i = 0; i < 8; i++) {
            board[6][i].setPiece(new Pawn(6, i, true));
        }
    }
    public void changeTurn(){
        whiteTurn = !whiteTurn;
    }
    public boolean getWhiteTurn(){
        return whiteTurn;
    }
    //Accessors
    public Square getSquare(int x, int y) {
        return board[x][y];
    }

    public Piece<?> getPiece(int x, int y) {
        return board[x][y].getPiece();
    }
    /**
     * Puts a piece onto a new square
     *
     * @param x X coordinate on the board of the piece about to move
     * @param y Y coordinate on the board of the piece about to move
     * @param x1 X coordinate on the board of where the piece is moving to
     * @param y1 Y coordinate on the board of where the king is moving to
     */
    public void setPiece(int x, int y, int x1, int y1) {
        board[x1][y1].setPiece(board[x][y].getPiece());
        board[x][y].removePiece();
        board[x1][y1].getPiece().setMoved();
    }

    /**
     * Puts a piece onto a new square without any consideration of if there is already a piece there
     *
     * @param x X coordinate on the board where the piece is going
     * @param y Y coordinate on the board where the piece is going
     * @param p Parametrized piece that will go on this square
     *
     * @return Returns whether there is check coming from a direction or not
     */
    public void setPiece(int x, int y, Piece<?> p) {
        board[x][y].setPiece(null);
        board[x][y].setPiece(p);
    }

    /**
     * Checks whether a move is valid
     *
     * @param x X coordinate on the board of the piece about to move
     * @param y Y coordinate on the board of the piece about to move
     * @param x1 X coordinate on the board of where the piece is moving to
     * @param y1 Y coordinate on the board of where the king is moving to
     *
     * @return Whether the move attempted is valid or not
     */
    public boolean checkMove(int x, int y, int x1, int y1) {
        if (x == 10 || x1 == 10) {
            return false;
        }
        return board[x][y].getPiece().checkMove(x, y, x1, y1, this);
    }

    /**
     * Creates a deep copy of the existing chess board
     * @param b ChessBoard representation
     * @return New Chessboard
     */
    public ChessBoard boardCopy(ChessBoard b) {
        ChessBoard c = new ChessBoard();
        for (int r = 0; r < 8; r++) {
            for (int cc = 0; cc < 8; cc++) {
                c.getSquare(r, cc).removePiece();
                if (b.getPiece(r, cc) != null) {
                    c.getSquare(r, cc).setPiece(b.getPiece(r, cc));
                }
            }
        }
        return c;
    }

    /**
     * Checks whether a side is in check or not
     *
     * @param x X coordinate on the board of the piece about to move
     * @param y Y coordinate on the board of the piece about to move
     * @param x1 X coordinate on the board of where the piece is moving to
     * @param y1 Y coordinate on the board of where the king is moving to
     * @param b ChessBoard representation
     *
     * @return Whether a side is in check or not
     */
    public boolean checkInCheck(int x, int y, int x1, int y1, ChessBoard b) {
        int kX = 0;
        int kY = 0;
        ChessBoard c = boardCopy(b);
        c.setPiece(x, y, x1, y1);
        if(x == 10 || y == 10 || x1 == 10 || y1 == 10){
            return true;
        }
        boolean white = c.getPiece(x1, y1).getIsWhite();
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (c.getPiece(i, j) != null && c.getPiece(i, j).getIsWhite() == white && c.getPiece(i, j).toString().equals("King")) {
                    kX = i;
                    kY = j;
                }
            }
        }
        int xInc = c.getPiece(kX, kY).getIsWhite() ? -1 : 1;
        if (checkOnBoard(kX + xInc, kY + 1) && c.getPiece(kX + xInc, kY + 1) != null && c.getPiece(kX + xInc, kY + 1).toString().equals("Pawn") && c.getPiece(kX + xInc, kY + 1).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
            return true;
        } else if (checkOnBoard(kX + xInc, kY - 1) && c.getPiece(kX + xInc, kY - 1) != null && c.getPiece(kX + xInc, kY - 1).toString().equals("Pawn") && c.getPiece(kX + xInc, kY - 1).getIsWhite()!= c.getPiece(kX, kY).getIsWhite()) {
            return true;
        }
        return rowColumnCheck(kX,kY,c) || checkKnights(kX, kY, c) || diagonalCheck(kX, kY, c) || kingCheck(kX, kY, c);
    }
    /**
     * Helper function for finding if side is in check from a 90 degree angle
     *
     * @param kX X coordinate on the board of the king
     * @param kY Y coordinate on the board of the king
     * @param c ChessBoard representation
     *
     * @return Returns whether there is check coming from a direction or not
     */
    public boolean rowColumnCheck(int kX,int kY, ChessBoard c){
        return rowColumnHelper(kX,kY,1,0,c) || rowColumnHelper(kX,kY,0,1,c) || rowColumnHelper(kX,kY,-1,0,c) || rowColumnHelper(kX,kY,0,-1,c);
    }
    /**
     * Returns if there is a piece delivering check from a horizontal/vertical direction
     *
     * @param kX X coordinate on the board of the king
     * @param kY Y coordinate on the board of the king
     * @param xInc x direction that we are checking
     * @param yInc y direction that we are checking
     * @param c ChessBoard representation
     *
     * @return Whether check is coming from a direction or not
     */
    public boolean rowColumnHelper(int kX,int kY, int xInc, int yInc, ChessBoard c){
        for (int i = 1; i < 8; i++) {
            if (checkOnBoard(kX+xInc*i, kY+yInc*i) && c.getPiece(kX+xInc*i, kY+yInc*i) != null && c.getPiece(kX+xInc*i, kY+yInc*i).getIsWhite() == c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if(checkOnBoard(kX+xInc*i, kY+yInc*i)&& c.getPiece(kX+xInc*i, kY+yInc*i) != null && c.getPiece(kX+xInc*i, kY+yInc*i).getIsWhite() != c.getPiece(kX, kY).getIsWhite()){
                return c.getPiece(kX+xInc*i, kY+yInc*i).toString().equals("Rook") || c.getPiece(kX+xInc*i, kY+yInc*i).toString().equals("Queen");
            }
        }
        return false;
    }
    /**
     * Helper function for finding if side is in check from a diagonal angle
     *
     * @param kX X coordinate on the board of the king
     * @param kY Y coordinate on the board of the king
     * @param c ChessBoard representation
     *
     * @return Returns whether there is check coming from a direction or not
     */
    public boolean diagonalCheck(int kX,int kY, ChessBoard c){
        return diagonalHelp(kX, kY,1,1,c) || diagonalHelp(kX, kY,-1,1,c) ||diagonalHelp(kX, kY,-1,-1,c) ||diagonalHelp(kX, kY,1,-1,c) ;
    }
    /**
     * Returns if there is a piece delivering check from a diagonal direction
     *
     * @param kX X coordinate on the board of the king
     * @param kY Y coordinate on the board of the king
     * @param xInc x direction that we are checking
     * @param yInc y direction that we are checking
     * @param c ChessBoard representation
     *
     * @return Whether check is coming from a direction or not
     */
    private boolean diagonalHelp(int kX,int kY, int xInc, int yInc, ChessBoard c){
        for (int i = 1; i < 8; i++) {
            if (!checkOnBoard(kX + xInc*i, kY + yInc*i)) {
                return false;
            }
            if (c.getPiece(kX + xInc*i, kY + yInc*i) != null) {
                return c.getPiece(kX + xInc*i, kY + yInc*i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX + xInc*i, kY + yInc*i).toString().equals("Bishop") || c.getPiece(kX + xInc*i, kY + yInc*i).toString().equals("Queen"));
            }
        }
        return false;
    }
    /**
     * Checks whether the king is in check or not
     *
     * @param kX X coordinate on the board of the king
     * @param kY Y coordinate on the board of the king
     * @param c ChessBoard representation
     *
     * @return Whether the king is in check
     */
    public boolean kingCheck(int kX,int kY, ChessBoard c){
        for(int i = -1; i < 2; i++){
            for(int j = -1; j < 2; j++){
                if((i != j || i != 0) && checkOnBoard(kX+i,kY+j) && c.getPiece(kX+i,kY+j) != null && c.getPiece(kX+i,kY+j).toString().equals("King"))
                    return true;
            }
        }
        return false;
    }
    /**
     * Checks if we are at the end of a game
     *
     * @param whitesTurn is it white to move?
     *
     * @return Whether we are at the end of the game yet
     */
    public boolean checkGameEnd(boolean whitesTurn) {
        int kX = 0, kY = 0;
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (board[i][j].getPiece() != null && board[i][j].getPiece().getIsWhite() == whitesTurn && board[i][j].getPiece().toString().equals("King")) {
                    kX = i;
                    kY = j;
                }
            }
        }
        //Would need to check that king can't move, no pieces can block and attacking piece cant be taken
        return false;
    }
    /**
     * Checks that the spot you are checking for is on the board
     *
     * @param x X coordinate on the board
     * @param y Y coordinate on the board
     *
     * @return Whether the square is on the board or not
     */
    public boolean checkOnBoard(int x, int y) {
        return x >= 0 && x < 8 && y >= 0 && y < 8;
    }
    /**
     * Checks that the spot the knight is moving to is valid
     *
     * @param x X coordinate on the board of knight
     * @param y Y coordinate on the board of knight
     * @param c Represntation of our chess board
     *
     * @return Whether the knight can be moved to that spot
     */
    public boolean checkKnights(int x, int y, ChessBoard c) {
        int[][] squares = {{2,1},{2,-1},{-2,-1},{-2,1},{-1,2},{-1,-2},{1,2},{1,-2}};
        for(int i = 0; i < 8; i++){
            if(checkOnBoard(x + squares[i][0], y + squares[i][1]) && c.getPiece(x + squares[i][0], y + squares[i][1]) != null && c.getPiece(x, y).getIsWhite() != c.getPiece(x + squares[i][0], y + squares[i][1]).getIsWhite() && c.getPiece(x + squares[i][0], y + squares[i][1]).toString().equals("Knight")){
                return true;
            }
        }
        return false;
    }

}
