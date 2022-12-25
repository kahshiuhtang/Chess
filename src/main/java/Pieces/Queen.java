package Pieces;

import Game.ChessBoard;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public class Queen implements Piece<Queen>{
    private ImageIcon whiteV, blackV;
    private int x, y;
    private boolean isWhite, moved;

    public Queen(int x, int y, boolean isWhite) {
        this.x = x;
        this.y = y;
        this.isWhite = isWhite;
        moved = false;
        loadImages();
    }

    public ImageIcon getIcon() {
        return isWhite ? whiteV : blackV;
    }

    @Override
    public boolean getIsWhite() {
        return isWhite;
    }

    @Override
    public boolean getMoved() {
        return moved;
    }

    @Override
    public void setMoved() {
        moved = true;
    }

    @Override
    public boolean checkMove(int x, int y, int x1, int y1, ChessBoard c) {
        Rook r1 = new Rook(x,y,this.isWhite);
        Bishop b1 = new Bishop(x,y,this.isWhite);
        return r1.checkMove(x,y,x1,y1,c) || b1.checkMove(x,y,x1,y1,c);
    }

    public void loadImages() {
        try {
            Image image = ImageIO.read(new File("images/whitequeen.png"));
            Image image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            whiteV = new ImageIcon(image1);
            image = ImageIO.read(new File("images/blackqueen.png"));
            image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            blackV = new ImageIcon(image1);
        } catch (IOException io) {

        }
    }
    @Override
    public Queen getSelf() {
        return this;
    }
}
