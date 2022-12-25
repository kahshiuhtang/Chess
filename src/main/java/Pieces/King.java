package Pieces;

import Game.ChessBoard;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public class King implements Piece<King>{
    private ImageIcon whiteV, blackV;
    private int x, y;
    private final boolean isWhite;
    private boolean moved;

    public King(int x, int y, boolean isWhite) {
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
            Image image = ImageIO.read(new File("Pieces/images/whiteking.png"));
            Image image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            whiteV = new ImageIcon(image1);
            image = ImageIO.read(new File("Pieces/images/blackking.png"));
            image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            blackV = new ImageIcon(image1);
        } catch (IOException io) {
            System.out.println(io.toString());
        }
    }
    @Override
    public King getSelf() {
        return this;
    }
    public boolean checkMove(int x, int y, int x1, int y1, ChessBoard c) {
        Piece<?> temp = c.getPiece(x, y);
        if(Math.abs(y1 - y) == 2 && !temp.getMoved()){
            int xRow = temp.getIsWhite() ? 7 : 0;
            if (y1 - y == 2 && x1 == x && x == xRow) {
                return c.getPiece(xRow, 6) == null && c.getPiece(xRow, 5) == null;
            } else if (y1 - y == -2 && x1 == x && x == xRow) {
                return c.getPiece(xRow, 1) == null && c.getPiece(xRow, 2) == null && c.getPiece(xRow, 3) == null;
            }
        }else if(Math.abs(y - y1) <= 1 && Math.abs(x - x1) <= 1){
            return c.getPiece(x1,y1) == null || c.getPiece(x1, y1).getIsWhite() != temp.getIsWhite();
        }
        return false;
    }
}
