package Game;

import java.awt.Color;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import Pieces.*;

public class ChessFrame extends javax.swing.JFrame implements ActionListener {
    private javax.swing.JButton bishopBUT;
    private javax.swing.JPanel boardPAN;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JButton knightBUT;
    private javax.swing.JPanel promotionPAN;
    private javax.swing.JButton queenBUT;
    private javax.swing.JButton rookBUT;
    
    //Chessboard, 2 sets of coords, which color's turn, two arrays for two boards (black + white)
    private ChessBoard chess;
    private int prevX, prevY, newX, newY;
    private int turnStage;
    private JButton[][] squares;

    public ChessFrame() {
        initComponents();
        initialize();
    }

    /**
     * Sets up the chess game and the chess GUI
     */
    public void initialize() {
        chess = new ChessBoard();
        turnStage = 0;
        boardPAN.setLayout(new GridLayout(8, 8));
        squares = new JButton[8][8];
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                squares[i][j] = new JButton();
                squares[i][j].addActionListener(this);
                boardPAN.add(squares[i][j]);
            }
        }
        knightBUT.setBackground(new Color(145, 131, 120));
        bishopBUT.setBackground(new Color(145, 131, 120));
        queenBUT.setBackground(new Color(145, 131, 120));
        rookBUT.setBackground(new Color(145, 131, 120));
        knightBUT.setIcon(chess.getSquare(0, 1).getPiece().getIcon());
        bishopBUT.setIcon(chess.getSquare(0, 2).getPiece().getIcon());
        queenBUT.setIcon(chess.getSquare(0, 3).getPiece().getIcon());
        rookBUT.setIcon(chess.getSquare(0, 0).getPiece().getIcon());
        coloring();
        setPieces();
    }
    /**
     * Colors in the squares on the chessboard in GUI
     */
    public void coloring() {
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (i % 2 == 1) {
                    if (j % 2 == 0) {
                        squares[i][j].setBackground(new Color(139, 69, 19));
                    } else {
                        squares[i][j].setBackground(Color.WHITE);
                    }
                } else {
                    if (j % 2 == 0) {
                        squares[i][j].setBackground(Color.WHITE);
                    } else {
                        squares[i][j].setBackground(new Color(139, 69, 19));
                    }
                }
            }
        }
    }
    /**
     * Places down a piece whre it belongs at the start of a game
     */
    public void setPieces() {
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (chess.getSquare(i, j).getPiece() != null) {
                    squares[i][j].setIcon(chess.getSquare(i, j).getPiece().getIcon());
                } else {
                    squares[i][j].setIcon(null);
                }
            }
        }
    }
    /**
     * Turns a queening pawn into a bishop
     *
     * @param evt Event that has been triggered
     */
    private void bishopBUTActionPerformed(java.awt.event.ActionEvent evt) {
        // TODO add your handling code here:
        for(int i = 0; i < 8; i++){
            if(chess.getPiece(0,i) != null && chess.getPiece(0,i).toString().equals("Pawn")){
                chess.setPiece(0,i, new Bishop(0,i,true));
                setPieces();
            }
            if(chess.getPiece(7,i) != null && chess.getPiece(7, i).toString().equals("Pawn")){
                chess.setPiece(7,i, new Bishop(7,i,false));
                setPieces();
            }
        }
    }
    /**
     * Turns a queening pawn into a knight
     *
     * @param evt Event that has been triggered
     */
    private void knightBUTActionPerformed(java.awt.event.ActionEvent evt) {
        for(int i = 0; i < 8; i++){
            if(chess.getPiece(0,i) != null && chess.getPiece(0,i).toString().equals("Pawn")){
                chess.setPiece(0,i, new Knight(0,i,true));
                setPieces();
            }
            if(chess.getPiece(7,i) != null && chess.getPiece(7, i).toString().equals("Pawn")){
                chess.setPiece(7,i, new Knight(7,i,false));
                setPieces();
            }
        }
    }
    /**
     * Turns a queening pawn into a rook
     *
     * @param evt Event that has been triggered
     */
    private void rookBUTActionPerformed(java.awt.event.ActionEvent evt) {
        for(int i = 0; i < 8; i++){
            if(chess.getPiece(0,i) != null && chess.getPiece(0,i).toString().equals("Pawn")){
                chess.setPiece(0,i, new Rook(0,i,true));
                setPieces();
            }
            if(chess.getPiece(7,i) != null && chess.getPiece(7, i).toString().equals("Pawn")){
                chess.setPiece(7,i, new Rook(7,i,false));
                setPieces();
            }
        }
    }
    /**
     * Turns a queening pawn into a queen
     *
     * @param evt Event that has been triggered
     */
    private void queenBUTActionPerformed(java.awt.event.ActionEvent evt) {
        for(int i = 0; i < 8; i++){
            if(chess.getPiece(0,i) != null && chess.getPiece(0,i).toString().equals("Pawn")){
                chess.setPiece(0,i, new Queen(0,i,true));
                setPieces();
            }
             if(chess.getPiece(7,i) != null && chess.getPiece(7, i).toString().equals("Pawn")){
                chess.setPiece(7,i, new Queen(7,i,false));
                setPieces();
            }
        }
    }

    public static void main(String args[]) {
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new ChessFrame().setVisible(true);
            }
        });
    }
    /**
     * Initializes all the components on the GUI screen
     */
    private void initComponents() {
        boardPAN = new javax.swing.JPanel();
        promotionPAN = new javax.swing.JPanel();
        queenBUT = new javax.swing.JButton();
        bishopBUT = new javax.swing.JButton();
        knightBUT = new javax.swing.JButton();
        rookBUT = new javax.swing.JButton();
        jLabel1 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setPreferredSize(new java.awt.Dimension(1280, 1280));
        getContentPane().setLayout(null);
        boardPAN.setPreferredSize(new java.awt.Dimension(800, 800));
        javax.swing.GroupLayout boardPANLayout = new javax.swing.GroupLayout(boardPAN);
        boardPAN.setLayout(boardPANLayout);
        boardPANLayout.setHorizontalGroup(
                boardPANLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 800, Short.MAX_VALUE)
        );
        boardPANLayout.setVerticalGroup(
                boardPANLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 800, Short.MAX_VALUE)
        );

        getContentPane().add(boardPAN);
        boardPAN.setBounds(20, 80, 800, 800);
        queenBUT.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                queenBUTActionPerformed(evt);
            }
        });
        promotionPAN.add(queenBUT);
        bishopBUT.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                bishopBUTActionPerformed(evt);
            }
        });
        promotionPAN.add(bishopBUT);
        knightBUT.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                knightBUTActionPerformed(evt);
            }
        });
        promotionPAN.add(knightBUT);
        rookBUT.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                rookBUTActionPerformed(evt);
            }
        });
        promotionPAN.add(rookBUT);
        getContentPane().add(promotionPAN);
        promotionPAN.setBounds(860, 50, 200, 800);
        jLabel1.setFont(new java.awt.Font("Engravers MT", 1, 48)); // NOI18N
        jLabel1.setText("White");
        jLabel1.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);
        getContentPane().add(jLabel1);
        jLabel1.setBounds(290, 20, 270, 60);
        jLabel2.setFont(new java.awt.Font("Engravers MT", 1, 48)); // NOI18N
        jLabel2.setText("Black");
        getContentPane().add(jLabel2);
        jLabel2.setBounds(1370, 20, 260, 56);

        pack();
    }
    /**
     * Activated when there has been any action on the board
     * Will tell handler how to manage event
     * Either piece is selected to move or square where piece should end up has selected
     * @param ae Event that has occurred and triggered this function
     */
    public void actionPerformed(ActionEvent ae) {
        //Finds source of button press
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (ae.getSource() == squares[i][j]) {
                    switch (turnStage) {
                        case 0: //White side has decided which piece ot move
                            if (chess.getSquare(i, j).getPiece() != null && chess.getPiece(i, j).getIsWhite() && !chess.checkGameEnd(true)) {
                                squares[i][j].setBackground(Color.RED);
                                prevX = i;
                                prevY = j;
                                turnStage++;
                            }
                            break;
                        case 1: //White side has decided where to move its piece
                            coloring();
                            newX = i;
                            newY = j;
                            ChessBoard p = chess;
                            if (chess.checkMove(prevX, prevY, newX, newY) && !chess.checkInCheck(prevX, prevY, newX, newY, p)) {
                                //Checks for castling
                                if (chess.getPiece(prevX, prevY).toString().equals("King") && Math.abs(newY - prevY) == 2) {
                                    if (newY - prevY == 2 && chess.getPiece(7, 7) != null && !chess.getPiece(7, 7).getMoved()) {
                                        chess.setPiece(7, 7, 7, 5);
                                        chess.setPiece(prevX, prevY, newX, newY);
                                        turnStage++;
                                    } else if (newY - prevY == -2 && chess.getPiece(7, 0) != null && !chess.getPiece(7, 0).getMoved()) {
                                        chess.setPiece(7, 0, 7, 3);
                                        chess.setPiece(prevX, prevY, newX, newY);
                                        turnStage++;
                                    }else{
                                        System.out.println("Failed");
                                        turnStage = 0;
                                    }
                                }else{
                                    chess.setPiece(prevX, prevY, newX, newY);
                                    turnStage++;
                                }
                            } else {
                                turnStage = 0;
                            }
                            prevX = prevY = newX = newY = 10;
                            setPieces();
                            break;
                        case 2: //Black piece has selected a piece
                            if (chess.getSquare(i, j).getPiece() != null && !chess.getPiece(i, j).getIsWhite() && !chess.checkGameEnd(true)) {
                                squares[i][j].setBackground(Color.RED);
                                prevX = i;
                                prevY = j;
                                turnStage++;
                            }
                            break;
                        case 3: //Black side has decided where to move its piece
                            coloring();
                            newX = i;
                            newY = j;
                            ChessBoard pp = chess;
                            if (chess.checkMove(prevX, prevY, newX, newY) && !chess.checkInCheck(prevX, prevY, newX, newY, pp) && !chess.checkGameEnd(false)) {
                                if (chess.getPiece(prevX, prevY).toString().equals("King") && Math.abs(newY - prevY) == 2) {
                                    if (newY - prevY == 2 && chess.getPiece(0, 7) != null && !chess.getPiece(0, 7).getMoved()) {
                                        chess.setPiece(0, 7, 0, 5);
                                        chess.setPiece(prevX, prevY, newX, newY);
                                        turnStage = 0;
                                    } else if (newY - prevY == -2 && chess.getPiece(0, 0) != null && !chess.getPiece(0, 0).getMoved()) {
                                        chess.setPiece(0, 0, 0, 3);
                                        chess.setPiece(prevX, prevY, newX, newY);
                                        turnStage = 0;
                                    }else{
                                        turnStage = 2;
                                    }
                                }else{
                                    chess.setPiece(prevX, prevY, newX, newY);
                                    turnStage = 0;
                                }
                            } else {
                                turnStage = 2;
                            }
                            setPieces();
                            prevX = prevY = newX = newY = 10;
                    }
                }
            }
        }
    }

}
