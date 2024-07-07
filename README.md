This project is a Blackjack simulation game built with Flask for the web interface, Matplotlib for data visualization, and Python for the simulation logic. 
Users can select different betting strategies, run simulations, and view their results to try and achieve higher scores. 
The application securely manages sessions and dynamically generates plots of game outcomes to enhance user engagement.

## Project Structure

- `BlackJack.py`: This file contains the logic for the Blackjack simulation. It includes the game rules, player and dealer actions, and various betting strategies that users can choose from.
- `Blackjackgraphs.py`: This file is responsible for generating graphs using Matplotlib to visualize the results of the Blackjack simulations. It creates plots that show the total money over the hands played.
- `templates/index.html`: This HTML file is the main web interface for the application. It allows users to select a betting strategy, run the simulation, and view the results.
- `app.py`: This file contains the Flask web application. It handles user interactions, runs the simulation, and serves the HTML content.

## Requirements

To run this project, you need to have Python installed along with the following packages:
- Flask
- Matplotlib
- Python-dotenv (optional, for managing environment variables)
