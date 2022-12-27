# Chess

## Details

* Pieces: 
  * Stored in an array of sets
  * Must update the set each time you move it
  * Erase if it is captured
  * Need to add array of taken pieces
* Pinned:
  * If there is an attacking piece and on the other side is the king
  * Find if axis between king lines up
    * Then check that one direction
* Check
  * Check for pawns (just check board)
  * Check for Knights (orientation)
  * Check each piece to see if it is correct orientation
    * Then check if there is anything between the two
* CheckMate
  * You are in check
  * All valid squares are covered
  * Every Piece that can block is pinned and cannot take pinned piece
  * Cant take the attacking piece
* Things to handle:
  * Promotion
  * Edge cases of handling positions