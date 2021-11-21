            ------------------------
           |        CASINO BOT      |
            ------------------------

Logs into https://stake.games/casino/bets website using credentials given in credentials.json
Makes a CSV of all the users that were registered under 24 hours.

INSTALLATION:
========================================================================================
Download & Install the latest version of Python from https://www.python.org/downloads/

On Microsoft Windows:
    After running the installer, on the first page there will be `ADD to PATH` option 
    make sure to check (click) while installing.

    after install, open command prompt (cmd) as administrator
    and run the below command to install dependencies:
    -------------------------------------------
    pip install selenium bs4 numpy pandas lxml 
    ------------------------------------------

On MacOS or Linux:
    after install, open terminal
    and run the below command to install dependencies:
    -------------------------------------------
    pip3 install selenium bs4 numpy pandas lxml 
    -------------------------------------------

    Navigate to the directory where script using cd command in terminal
    and run the below command

    On MacOS
    --------------------------------------------
    chmod +x resources/drivers/macos/geckodriver
    --------------------------------------------

    On Linux
    --------------------------------------------
    chmod +x resources/drivers/linux/geckodriver
    --------------------------------------------
=======================================================================================

RUNNING:
=======================================================================================
Navigate to the script directory if not already there using cd command in terminal/cmd

On Windows:
----------------------------------
python casino.py
----------------------------------

On MacOS or Linux:
----------------------------------
python3 casino.py
----------------------------------
=======================================================================================

NOTE: 
=======================================================================================
The script will save the list of users who joined under 24 hours in `under24.csv` file
and it will also the list of other users in `others.csv'.
The files will be updated every 30 minutes. 
Do not open the files when the script is running, if you want to open the files then
better copy it to somewhere else because if you open the file when the file was about
to save then it will cause error.
=======================================================================================
