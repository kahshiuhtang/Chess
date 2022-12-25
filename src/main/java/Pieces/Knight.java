package Pieces;

import Game.ChessBoard;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public class Knight implements Piece<Knight>{

    private ImageIcon whiteV, blackV;
    private int x, y;
    private boolean isWhite, moved;

    public Knight(int x, int y, boolean isWhite) {
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
    public void loadImages() {
        try {
            Image image = ImageIO.read(new File("images/whiteknight.png"));
            Image image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            whiteV = new ImageIcon(image1);
            image = ImageIO.read(new File("images/blackknight.png"));
            image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            blackV = new ImageIcon(image1);
        } catch (IOException io) {

        }
    }
    public boolean checkMove(int x, int y, int x1, int y1, ChessBoard c) {
        if (Math.abs(x - x1) == 1 && Math.abs(y - y1) == 2 && (c.getPiece(x1, y1) == null || c.getPiece(x1, y1).getIsWhite() != c.getPiece(x, y).getIsWhite())) {
            return true;
        } else return Math.abs(x - x1) == 2 && Math.abs(y - y1) == 1 && (c.getPiece(x1, y1) == null || c.getPiece(x1, y1).getIsWhite() != c.getPiece(x, y).getIsWhite());
    }
    @Override
    public Knight getSelf() {
        return this;
    }
    @Override
    public String toString(){
        return "Knight";
    }
}
