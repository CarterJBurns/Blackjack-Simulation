This project is a Blackjack simulation game built with Flask for the web interface, Matplotlib for data visualization, and Python for the simulation logic. Users can select different betting strategies, run simulations, and view their results to try and achieve higher scores. The application securely manages sessions and dynamically generates plots of game outcomes to enhance user engagement. A live CSV maker captures and stores gameplay data in real-time, enabling detailed analysis. Additionally, the application features a machine learning model that predicts the number of hands played based on the selected strategy and game parameters.

## Project Structure

- `BlackJack.py`: This file contains the logic for the Blackjack simulation. It includes the game rules, player and dealer actions, and various betting strategies that users can choose from.
- `Blackjackgraphs.py`: This file is responsible for generating the graph using Matplotlib to visualize the results of the Blackjack simulations. It creates plots that show the total money over the hands played.
- `templates/index.html`: This HTML file is the main web interface for the application. It allows users to select a betting strategy, run the simulation, and view the results.
- `app.py`: This file contains the Flask web application. It handles user interactions, runs the simulation, and serves the HTML content.
- `BlackJackPML.py`: Implements a stacking ensemble model to predict the number of Blackjack hands played based on user-selected strategies and gameplay data.
- `csv_maker.py`: Updates CSV file containing detailed Blackjack gameplay data for use in model training and analysis.
- `blackjackdata.csv`: Contains raw gameplay data used for training and evaluating the machine learning model.


