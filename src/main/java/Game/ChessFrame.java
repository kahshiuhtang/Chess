package Game;

import java.awt.Color;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import Pieces.*;

public class ChessFrame extends javax.swing.JFrame implements ActionListener {
    
    //Chessboard, 2 sets of coords, which color's turn, two arrays for two boards (black + white)
    private ChessBoard chess;
    private int prevX, prevY, newX, newY;
    private int turnStage;
    private JButton[][] squares, blackSquares;

    public ChessFrame() {
        initComponents();
        initialize();
    }
    
    //Stes up chessboard, arrays of JButtons and colors + middle queening buttons
    public void initialize() {
        chess = new ChessBoard();
        turnStage = 0;
        boardPAN.setLayout(new GridLayout(8, 8));
        blackBoardPAN.setLayout(new GridLayout(8, 8));
        squares = new JButton[8][8];
        blackSquares = new JButton[8][8];
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                squares[i][j] = new JButton();
                squares[i][j].addActionListener(this);
                boardPAN.add(squares[i][j]);
            }
        }
        for (int i = 7; i >= 0; i--) {
            for (int j = 7; j >= 0; j--) {
                blackSquares[i][j] = new JButton();
                blackSquares[i][j].addActionListener(this);
                blackBoardPAN.add(blackSquares[i][j]);
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
    
    //Colors in the JButtons depending on board
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
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (i % 2 == 1) {
                    if (j % 2 == 1) {
                        blackSquares[i][j].setBackground(Color.WHITE);
                    } else {
                        blackSquares[i][j].setBackground(new Color(139, 69, 19));
                    }
                } else {
                    if (j % 2 == 1) {
                        blackSquares[i][j].setBackground(new Color(139, 69, 19));
                    } else {
                        blackSquares[i][j].setBackground(Color.WHITE);
                    }
                }
            }
        }
    }
    
    //Sets each piece where it belongs depedning on chessboard class
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
        for (int i = 7; i >= 0; i--) {
            for (int j = 7; j >= 0; j--) {
                if (chess.getSquare(i, j).getPiece() != null) {
                    blackSquares[Math.abs(i)][Math.abs(j)].setIcon(chess.getSquare(i, j).getPiece().getIcon());
                } else {
                    blackSquares[Math.abs(i)][Math.abs(j)].setIcon(null);
                }
            }
        }
    }
    //Next is for queening
    //Checks that each spot has a pawn there and allows you to put a promoted piece there
    //I did not add restrictions so you can move with a pawn on the last rank
    //Just loops through each "end zone" and checks for pawns to replace


    private void bishopBUTActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_bishopBUTActionPerformed
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
    }//GEN-LAST:event_bishopBUTActionPerformed

    private void knightBUTActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_knightBUTActionPerformed
        // TODO add your handling code here:
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
    }//GEN-LAST:event_knightBUTActionPerformed

    private void rookBUTActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_rookBUTActionPerformed
        // TODO add your handling code here:
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
    }//GEN-LAST:event_rookBUTActionPerformed

    private void queenBUTActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_queenBUTActionPerformed
        // TODO add your handling code here:
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
    }//GEN-LAST:event_queenBUTActionPerformed

    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(ChessFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(ChessFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(ChessFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(ChessFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new ChessFrame().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton bishopBUT;
    private javax.swing.JPanel blackBoardPAN;
    private javax.swing.JPanel boardPAN;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JButton knightBUT;
    private javax.swing.JPanel promotionPAN;
    private javax.swing.JButton queenBUT;
    private javax.swing.JButton rookBUT;
    // End of variables declaration//GEN-END:variables
    private void initComponents() {

        blackBoardPAN = new javax.swing.JPanel();
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

        blackBoardPAN.setPreferredSize(new java.awt.Dimension(800, 800));

        javax.swing.GroupLayout blackBoardPANLayout = new javax.swing.GroupLayout(blackBoardPAN);
        blackBoardPAN.setLayout(blackBoardPANLayout);
        blackBoardPANLayout.setHorizontalGroup(
                blackBoardPANLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 800, Short.MAX_VALUE)
        );
        blackBoardPANLayout.setVerticalGroup(
                blackBoardPANLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGap(0, 800, Short.MAX_VALUE)
        );

        getContentPane().add(blackBoardPAN);
        blackBoardPAN.setBounds(1080, 80, 800, 800);

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

        //promotionPAN.setLayout(new AbsoluteLayout());

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
    @Override
    //What to do when a button is pressed
    public void actionPerformed(ActionEvent ae) {
        //Finds source of button press
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                if (ae.getSource() == squares[i][j]) {
                    //Whose turn and which stage of turn
                    //First stage of moving is selecting the piece
                    //Second stage is choosing which squrre to move that piece to
                    switch (turnStage) {
                        //For White
                        case 0:
                            //Checks that the piece is white and sets the coords for piece
                            if (chess.getSquare(i, j).getPiece() != null && chess.getPiece(i, j).getIsWhite() && chess.checkGameEnd(true)) {
                                squares[i][j].setBackground(Color.RED);
                                prevX = i;
                                prevY = j;
                                turnStage++;
                            }
                            break;
                        case 1:
                            //Redraws board so the selected piece is highighted red
                            coloring();
                            newX = i;
                            newY = j;
                            //chesssboard to pass as parameter
                            ChessBoard p = (ChessBoard) chess;
                            //Checks for check and whether move is legal
                            if (chess.checkMove(prevX, prevY, newX, newY) && !chess.checkInCheck(prevX, prevY, newX, newY, p)) {
                                //Sets piece and marks it as moved
                                chess.setPiece(prevX, prevY, newX, newY);
                                chess.getPiece(newX, newY).setMoved();
                                //Checks for castling privledges + acts accordingly
                                if (chess.getPiece(newX, newY).toString().equals("King") && Math.abs(newY - prevY) == 2) {
                                    if (newY - prevY == 2 && chess.getPiece(7, 7) != null && !chess.getPiece(7, 7).getMoved()) {
                                        chess.setPiece(7, 7, 7, 5);
                                    } else if (newY - prevY == -2 && chess.getPiece(7, 0) != null && !chess.getPiece(7, 0).getMoved()) {
                                        chess.setPiece(7, 0, 7, 3);
                                    }
                                }
                                //Move up to blacks turn
                                turnStage++;
                            } else {
                                //Else, resets and you have to rechoose which piece to move
                                turnStage = 0;
                            }
                            //resets these values
                            prevX = prevY = newX = newY = 10;
                            setPieces();
                            break;

                    }
                   //Same thing but for black 
                } else if (ae.getSource() == blackSquares[i][j]) {
                    switch (turnStage) {
                        case 2:
                            if (chess.getSquare(i, j).getPiece() != null && !chess.getPiece(i, j).getIsWhite()) {
                                blackSquares[i][j].setBackground(Color.RED);
                                prevX = i;
                                prevY = j;
                                turnStage++;
                            }
                            break;
                        case 3:
                            coloring();
                            newX = i;
                            newY = j;
                            ChessBoard pp = (ChessBoard) chess;
                            if (chess.checkMove(prevX, prevY, newX, newY) && !chess.checkInCheck(prevX, prevY, newX, newY, pp) && chess.checkGameEnd(false)) {
                                chess.setPiece(prevX, prevY, newX, newY);
                                chess.getPiece(newX, newY).setMoved();
                                if (chess.getPiece(newX, newY).toString().equals("King") && Math.abs(newY - prevY) == 2) {
                                    if (newY - prevY == 2 && chess.getPiece(0, 7) != null && !chess.getPiece(0, 7).getMoved()) {
                                        chess.setPiece(0, 7, 0, 5);
                                    } else if (newY - prevY == -2 && chess.getPiece(0, 0) != null && !chess.getPiece(0, 0).getMoved()) {
                                        chess.setPiece(0, 0, 0, 3);
                                    }
                                }
                                turnStage = 0;
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
