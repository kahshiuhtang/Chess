import Game.ChessFrame;

public class Test {

    public static void main(String[] args) {
        //Runs the GUI && sets up
        ChessFrame cf = new ChessFrame();
        cf.setTitle("Chess");
        cf.setBounds(0, 0, 2000, 1000);
        cf.setVisible(true);
    }
}
