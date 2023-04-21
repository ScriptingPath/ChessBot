# ChessBot

![изображение](https://user-images.githubusercontent.com/74320985/233668838-432f877f-10e6-4605-a73d-9eb133a4bf22.png)

How to use the bot:
1. Create an empty folder in any location.
2. Download the latest version of the program (app.exe) [here](https://github.com/ScriptingPath/ChessBot/releases/), then place it in folder.
3. Download the latest version of Stockfish [here](https://stockfishchess.org/download/) and place it in folder. Extract the executable file from the archive and change it name to "stockfish.exe".
4. Install the Tampermonkey extension in your browser.
5. Download [lichess.user.js](https://github.com/ScriptingPath/ChessBot/releases/download/v1.0.0/lichess.user.js) and install it in Tampermonkey.
6. Done! Run app.exe and enter the game.

The first time you run it, a file is created with the bot's settings. You can edit it.
The bot works only if app.exe is running.

The engine is Stockfish, other chess engines are not supported at the moment.

If the program closes immediately after launching, open a command line and run the program. After that an error should appear in the console. If it is engine related, try the following:
1. Open settings.json and enter there the absolute path to the engine executable.
2. If that doesn't help, try downloading a more compatible version of the engine [here](https://stockfishchess.org/download/).
3. If none of the above helps you, describe your problem [here](https://github.com/ScriptingPath/ChessBot/issues).
