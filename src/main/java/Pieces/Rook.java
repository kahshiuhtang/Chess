package Pieces;

import Game.ChessBoard;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public class Rook implements Piece<Rook>{
    private ImageIcon whiteV, blackV;
    private int x, y;
    private boolean isWhite, moved;

    public Rook(int x, int y, boolean isWhite) {
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
            Image image = ImageIO.read(new File("images/whiterook.png"));
            Image image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            whiteV = new ImageIcon(image1);
            image = ImageIO.read(new File("images/blackrook.png"));
            image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            blackV = new ImageIcon(image1);
        } catch (IOException io) {

        }
    }
    @Override
    public boolean checkMove(int x, int y, int x1, int y1, ChessBoard c) {
        if(x-x1 != 0 && y-y1 != 0) return false;
        int xInc = Integer.compare(x1 - x, 0);
        int yInc = Integer.compare(y1 - y, 0);
        int j = Math.max(Math.abs(x - x1), Math.abs(y - y1));
        for (int i = 1; i < j; i++){
            x += xInc;
            y += yInc;
            if (c.getPiece(x, y) != null) {
                return false;
            }
        }
        return c.getPiece(x1, y1) == null || c.getPiece(x1, y1).getIsWhite() != c.getPiece(x, y).getIsWhite();
    }
    @Override
    public Rook getSelf() {
        return this;
    }
}
