package Pieces;

import Game.ChessBoard;

import java.awt.Image;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;

public class Bishop implements Piece<Bishop> {

    private ImageIcon whiteV, blackV;
    private int x, y;
    private boolean isWhite, moved;

    public Bishop(int x, int y, boolean isWhite) {
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
            Image image = ImageIO.read(new File("images/whitebishop.png"));
            Image image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            whiteV = new ImageIcon(image1);
            image = ImageIO.read(new File("images/blackbishop.png"));
            image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            blackV = new ImageIcon(image1);
        } catch (Exception io) {
            System.out.println(io.toString());
        }
    }

    public boolean checkMove(int x, int y, int x1, int y1, ChessBoard c) {
        if (Math.abs(x - x1) != Math.abs(y - y1)) return false;
        int xInc = x1 - x > 0 ? 1 : -1;
        int yInc = y1 - y > 0 ? 1 : -1;
        for (int i = 1; i < Math.abs(x - x1); i++) {
            x += xInc;
            y += yInc;
            if (c.getPiece(x , y) != null) {
                return false;
            }
        }
        return true;
    }

    @Override
    public Bishop getSelf() {
        return this;
    }

    public String toString() {
        return "Bishop";
    }

}

