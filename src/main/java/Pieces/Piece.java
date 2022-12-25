package Pieces;

import Game.ChessBoard;

import javax.swing.*;

public interface Piece<T> {
    public ImageIcon getIcon();

    public boolean getIsWhite();

    public boolean getMoved();

    public void setMoved();

    //public void changeFirstMove();
    public  boolean checkMove(int x, int y, int x1, int y1, ChessBoard c);

    public T getSelf();
}
