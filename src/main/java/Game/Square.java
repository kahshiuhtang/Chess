package Game;

import Pieces.Piece;
public class Square<T extends Piece<?>> {
    private Piece<T> currentPiece;
    /**
     * Constructor for when you are notgiven a piece to put on square
     */
    public Square(){
        this.currentPiece = null;
    }
    /**
     * Constructor for when you are given a piece to put on square
     *
     * @param cP
     */
    public Square(Piece<T> cP){this.currentPiece = cP;}
    /**
     * Setting a piece on this square
     *
     * @param p Piece that is about to be set
     */
    public void setPiece(Piece<T> p){
        this.currentPiece = p;
    }
    /**
     * Retrieving whatever piece is on this square
     */
    public Piece<T> getPiece(){
        return currentPiece;
    }
    /**
     * Removing whatever piece is on this square
     */
    public void removePiece(){
        currentPiece = null;
    }
}
