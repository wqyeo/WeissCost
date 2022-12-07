# WeissCost
Program to find cost of a Weiss Schwarz deck on [EncoreDeck](https://www.encoredecks.com/).<br>
All prices are searched from [Yuyutei](https://yuyu-tei.jp/game_ws/), and output prices are in Yen.

## Usage (With Exported EncoreDeck profile)

Export a target deck from [EncoreDeck](https://www.encoredecks.com/) into a **.txt**. file.
> The export button is on the top-right of the website.

Place the text file into the same directory as the program.<br>
With **python 3**, run `main.py`, then input the file name into the program.

#### With EncoreDeck URL

Just paste in the link to the deck profile directly.<br>
**But** this operation might be inaccurate due to the long loading time it takes to fetch a website off EncoreDecks.<br>
Hence, you are better off exporting the deck into a **.txt** file yourself, and give it to the program.
