# LOLStats

The League of Legends Match Tracker is a Python-based web application that allows users to view their match history and details of live games in real-time. This app uses the Riot Games API to access player data and display it to users.

## Features

### Match History

Users can view their match history and see details such as the game mode, date played, and the outcome of the match. The app also provides a summary of the user's performance in each match, including the champion played, KDA (kills, deaths, assists) ratio, and total gold earned.

### Live Match Tracking

The app allows users to track the details of their live games, including the summoner names and champion names of all players in the game. Users can see the real-time stats of each player, such as their KDA, items purchased, and total gold earned. Additionally, the app can display the current objective status, including the location of epic monsters like the dragon and Baron Nashor.

### Search for Other Players

Users can search for the match history and live games of other players. The app provides a summary of the searched player's performance, including their most played champions and their win rate.

## Requirements

To run this app, you must have a valid Riot Games API key. You can obtain an API key by creating a developer account at the Riot Games Developer Portal.

Additionally, you must have Python 3.x installed on your system. The following Python libraries are also required:

- Flask
- Requests

## Installation

1. Clone the repository to your local machine.
2. Install the required Python libraries using pip install -r requirements.txt.
3. Set your Riot Games API key as an environment variable named RIOT_API_KEY.
4. Run the app using python app.py.

## Usage

To use the app, open a web browser and navigate to <http://localhost:5000>.

### Viewing Match History

1. Enter your summoner name and region in the provided fields and click "Search".
2. Select the "Match History" tab to view a list of your recent matches.
3. Click on a match to view its details.

### Tracking a Live Game

1. Enter your summoner name and region in the provided fields and click "Search".
2. If you are currently in a live game, the "Live Game" tab will become active. Click on this tab to view the details of the game in real-time.

### Searching for Other Players

1. Enter the summoner name and region of the player you wish to search in the provided fields and click "Search".
2. Select the "Match History" or "Live Game" tab to view the searched player's performance and current game data.

## Conclusion

The League of Legends Match Tracker provides an easy-to-use interface for players to view their match history and track live games. The app is designed to be fast, reliable, and responsive, providing real-time updates on game data. This app can be easily extended to include more features and data, providing users with a more in-depth view of their performance in the game.
