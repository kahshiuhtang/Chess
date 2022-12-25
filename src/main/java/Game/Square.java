package Game;

import Pieces.Piece;
public class Square {
    private Piece<?> currentPiece;
    public Square(){
        this.currentPiece = null;
    }
    public Square(Piece<?> cP){this.currentPiece = cP;}
    public void setPiece(Piece<?> p){
        this.currentPiece = p;
    }
    public Piece<?> getPiece(){
        return currentPiece;
    }
    public void removePiece(){
        currentPiece = null;
    }
}
