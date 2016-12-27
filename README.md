# ExchangeConflict2016

## Project Summary
Have you ever played [Trade Wars](https://en.wikipedia.org/wiki/Trade_Wars "Trade Wars Wiki")?  

This is my fun project on the Trade Wars theme.  I'm looking to up the bar on Universe generation 
and I hope to use this as a fun playground of experimenting with AI and game development.

This project is not currently playable in any way.
 
TradeWars is available [here](http://www.eisonline.com/ "EIS")!  

## The Workflow
In order to experiment with the game you will need to complete the following steps:

1. Run bigbang.py to "Build a Universe"
2. (optional) Run uniview.py to review the game Universe
3. Run wars.py to "Play the Game"

### Building a Universe
The game universe is created by the bigbang.py script.  

I am using a program called StarGen to simulate planetary systems in each sector.  In order to run bigbang.py you will need to extract StarGen into a folder named WinStarGen within the main project folder.  If you are running on a non-Windows platform you will need to work with the file paths and folder names to get this to work at this point....sorry!

StarGen is available [here](http://www.eldacur.com/~brons/NerdCorner/StarGen/StarGen.html "StarGen")!

### Reviewing the Universe
You can get a visual representation of the game universe you created using the uniview.py script.  

I am using a library called networkx-viewer to show the Universe graph.  The library allows for modifications to its default GUI but I have not added any yet.  The systems/sectors with ports/stations are colored green and systems without stations are colored red.  The "Centrality" system has red label text.  You can click on a system to see the planetary and/or station data connected to it.  You typically need to use the mouse scroll wheel to zoom out when the GUI opens in order to see the graph.    

networkx-viewer is available [here](https://github.com/jsexauer/networkx_viewer "networkx-voewer")!

### Playing the Game
You play the game by running wars.py!

The game is currently changing very rapidly.  type in a section number to jump to the next sector.  You can enter Q to save and quit the game (if you don't exit via Q nothing you do is saved at this point).  Entering V on the command prompt will give you a list of the sectors you've visted and how many times you've visited it.
