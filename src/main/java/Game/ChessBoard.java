package Game;

import Pieces.*;

public class ChessBoard {

    private final Square[][] board;
    private final String b = "Black";
    private final String w = "White";

    //Creates a board digitally to reprsent and sets each piece up
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
    //Accessors
    public Square getSquare(int x, int y) {
        return board[x][y];
    }

    public Piece<?> getPiece(int x, int y) {
        return board[x][y].getPiece();
    }
    //Two methods to set pieces
    //Used coordinates to move
    public void setPiece(int x, int y, int x1, int y1) {
        board[x1][y1].setPiece(board[x][y].getPiece());
        board[x][y].removePiece();
    }

    //Just sets specific piece down on specific spot
    public void setPiece(int x, int y, Piece p) {
        board[x][y].setPiece(null);
        board[x][y].setPiece(p);
    }

    //Checks if the moves are legal
    //Calls each piece's checkMove depending on piece
    public boolean checkMove(int x, int y, int x1, int y1) {
        if (x == 10 || x1 == 10) {
            return false;
        }
        return board[x][y].getPiece().checkMove(x, y, x1, y1, this);
    }

    //Makes a new copy of board so data isn't messed up due to references
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

    //Checks inCheck but looking in each direction, kinda long
    public boolean checkInCheck(int x, int y, int x1, int y1, ChessBoard b) {
        int kX = 0;
        int kY = 0;
        ChessBoard c = boardCopy(b);
        c.setPiece(x, y, x1, y1);
        if(x == 10 || y == 10 || x1 == 10 || y1 == 10){
            return true;
        }
        if (c.getPiece(x1, y1).getIsWhite()) {
            for (int i = 0; i < 8; i++) {
                for (int j = 0; j < 8; j++) {
                    if (c.getPiece(i, j) != null && c.getPiece(i, j).getIsWhite() && c.getPiece(i, j).toString().equals("King")) {
                        kX = i;
                        kY = j;
                    }
                }
            }
        } else {
            for (int i = 0; i < 8; i++) {
                for (int j = 0; j < 8; j++) {
                    if (c.getPiece(i, j) != null && !c.getPiece(i, j).getIsWhite() && c.getPiece(i, j).toString().equals("King")) {
                        kX = i;
                        kY = j;
                    }
                }
            }
        }
        System.out.println(kX + "   " + kY);
        for (int i = 1; i < 8; i++) {
            if (kX + i < 8 && c.getPiece(kX + i, kY) != null && c.getPiece(kX + i, kY).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if(kX + i < 8 && c.getPiece(kX + i, kY) != null && c.getPiece(kX + i, kY).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && !(c.getPiece(kX + i, kY).toString().equals("Rook") || c.getPiece(kX + i, kY).toString().equals("Queen"))){
                break;
            }
            if (kX + i < 8 && c.getPiece(kX + i, kY) != null && c.getPiece(kX + i, kY).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX + i, kY).toString().equals("Rook") || c.getPiece(kX + i, kY).toString().equals("Queen"))) {
                return true;
            }
        }
        for (int i = 1; i < 8; i++) {

            if (kX - i >= 0 && c.getPiece(kX - i, kY) != null && c.getPiece(kX - i, kY).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if(kX -i >= 0  && c.getPiece(kX - i, kY) != null && c.getPiece(kX - i, kY).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && !(c.getPiece(kX - i, kY).toString().equals("Rook") || c.getPiece(kX - i, kY).toString().equals("Queen"))){
                break;
            }
            if (kX - i >= 0 && c.getPiece(kX - i, kY) != null && c.getPiece(kX - i, kY).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX - i, kY).toString().equals("Rook") || c.getPiece(kX - i, kY).toString().equals("Queen"))) {
                System.out.println("????");
                return true;
            }
        }
        for (int i = 1; i < 8; i++) {
            if (kY + i < 8 && c.getPiece(kX, kY + i) != null && c.getPiece(kX , kY+i).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if(kY + i < 8 && c.getPiece(kX, kY+i) != null && c.getPiece(kX , kY+i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && !(c.getPiece(kX, kY+i).toString().equals("Rook") || c.getPiece(kX, kY+i).toString().equals("Queen"))){
                break;
            }
            if (kY + i < 8 && c.getPiece(kX, kY + i) != null && c.getPiece(kX , kY+i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX, kY + i).toString().equals("Rook") || c.getPiece(kX, kY + i).toString().equals("Queen"))) {
                return true;
            }
        }
        for (int i = 1; i < 8; i++) {
            if (kY - i >= 0 && c.getPiece(kX, kY - i) != null && c.getPiece(kX , kY-i).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if(kY - i >= 0 && c.getPiece(kX, kY-i) != null && c.getPiece(kX , kY-i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && !(c.getPiece(kX, kY-i).toString().equals("Rook") || c.getPiece(kX, kY-i).toString().equals("Queen"))){
                break;
            }
            if (kY - i >= 0 && c.getPiece(kX, kY - i) != null && c.getPiece(kX , kY-i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX, kY - i).toString().equals("Rook") || c.getPiece(kX, kY - i).toString().equals("Queen"))) {
                return true;
            }
        }
        for (int i = 1; i < 8; i++) {
            if (kY + i < 8 && kX + i < 8 && c.getPiece(kX + i, kY + i) != null && c.getPiece(kX+i , kY+i).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if (kY + i < 8 && kX + i < 8 && c.getPiece(kX + i, kY + i) != null && c.getPiece(kX+i , kY+i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX + i, kY + i).toString().equals("Bishop") || c.getPiece(kX + i, kY + i).toString().equals("Queen"))) {
                return true;
            }
        }
        for (int i = 1; i < 8; i++) {
            if (kY - i >= 0 && kX - i >= 0 && c.getPiece(kX - i, kY - i) != null && c.getPiece(kX-i , kY-i).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
                break;
            }
            if (kY - i >= 0 && kX - i >= 0 && c.getPiece(kX - i, kY - i) != null && c.getPiece(kX-i , kY-i).getIsWhite() != c.getPiece(kX, kY).getIsWhite() && (c.getPiece(kX - i, kY - i).toString().equals("Rook") || c.getPiece(kX - i, kY - i).toString().equals("Queen"))) {
                return true;
            }
        }
        int xInc = c.getPiece(kX, kY).getIsWhite() ? -1 : 1;
        if (checkOnBoard(kX + xInc, kY + 1) && c.getPiece(kX + xInc, kY + 1) != null && c.getPiece(kX + xInc, kY + 1).toString().equals("Pawn") && c.getPiece(kX + xInc, kY + 1).getIsWhite() != c.getPiece(kX, kY).getIsWhite()) {
            return true;
        } else if (checkOnBoard(kX + xInc, kY - 1) && c.getPiece(kX + xInc, kY - 1) != null && c.getPiece(kX + xInc, kY - 1).toString().equals("Pawn") && c.getPiece(kX + 1, kY - 1).getIsWhite()!= c.getPiece(kX, kY).getIsWhite()) {
            return true;
        }
        return checkKnights(kX, kY, c) || diagonalCheck(kX, kY, c) || kingCheck(kX, kY, c);
    }
    public boolean diagonalCheck(int kX,int kY, ChessBoard c){
        return diagonalHelp(kX, kY,1,1,c) || diagonalHelp(kX, kY,-1,1,c) ||diagonalHelp(kX, kY,-1,-1,c) ||diagonalHelp(kX, kY,1,-1,c) ;
    }
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
    //King moved into check
    public boolean kingCheck(int kX,int kY, ChessBoard c){
        for(int i = -1; i < 2; i++){
            for(int j = -1; j < 2; j++){
                if((i != j || i != 0) && checkOnBoard(kX+i,kY+j) && c.getPiece(kX+i,kY+j) != null && c.getPiece(kX+i,kY+j).toString().equals("King"))
                    return true;
            }
        }
        return false;
    }
    //Not finished; for a rainy day
    public boolean checkGameEnd(boolean whitesTurn) {
        return true;
    }
    //Checks that the spot you are checking for is on the board
    public boolean checkOnBoard(int x, int y) {
        return x >= 0 && x < 8 && y >= 0 && y < 8;
    }
    //Knights
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
