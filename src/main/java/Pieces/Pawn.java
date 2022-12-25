package Pieces;

import Game.ChessBoard;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;

public class Pawn implements Piece<Pawn>{
    private ImageIcon whiteV, blackV;
    private final int x;
    private final int y;
    private final boolean isWhite;
    private boolean moved;

    public Pawn(int x, int y, boolean isWhite) {
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
            Image image = ImageIO.read(new File("Pieces/images/whitepawn.png"));
            Image image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            whiteV = new ImageIcon(image1);
            image = ImageIO.read(new File("Pieces/images/blackpawn.png"));
            image1 = image.getScaledInstance(100, 100, java.awt.Image.SCALE_SMOOTH);
            blackV = new ImageIcon(image1);
        } catch (IOException io) {

        }
    }
    public boolean checkMove(int x, int y, int x1, int y1, ChessBoard c) {
        Piece<?> p = c.getPiece(x, y);
        int xInc = p.getIsWhite() ? -1 : 1;
        if (x1 - x == xInc*2 && !p.getMoved() && c.getPiece(x + xInc, y) == null && c.getPiece(x + 2*xInc, y) == null && y1 - y == 0) {
            return true;
        } else if (x1 - x == xInc && c.getPiece(x + xInc, y) == null && y1 - y == 0) {
            return true;
        } else if (x1 - x == xInc && y1 - y == 1 && c.getPiece(x + 1, y + 1) != null && c.getPiece(x1, y1).getIsWhite() != p.getIsWhite()) {
            return true;
        } else return x1 - x == xInc && y1 - y == -1 && c.getPiece(x + 1, y - 1) != null && c.getPiece(x1, y1).getIsWhite() != p.getIsWhite();
    }
    @Override
    public Pawn getSelf() {
        return this;
    }
}

