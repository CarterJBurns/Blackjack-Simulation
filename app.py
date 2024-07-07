from flask import Flask, render_template, request, render_template_string, session
import matplotlib
import matplotlib.pyplot as plt
import io
import BlackJack
import BlackjackGraphs
import base64

# Set the matplotlib backend to Agg
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = 'BlackJack'  # Replace with a secure secret key


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        strategy = request.form['strategy']

        # Debug print
        print(f"Received POST request with strategy: {strategy}")

        # Run the blackjack simulation to populate total_money_list
        print("Running BlackJack simulation with strategy:", strategy)
        BlackJack.main(strategy)

        # Collect results from BlackJack module
        total_money = BlackJack.total_money
        play_of_hand_count = BlackJack.play_of_hand_count
        blackjackcount = BlackJack.blackjackcount
        win_loss_history = BlackJack.win_loss_history
        total_money_list = BlackJack.total_money_list
        wins = win_loss_history.count("win")
        losses = win_loss_history.count("loss")
        pushes = win_loss_history.count("push")

        # Calculate win percentage, handle division by zero
        winpercentage = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0

        max_winstreak, max_losstreak = BlackJack.max_win_loss(win_loss_history)

        # Check and update high score for hands played
        high_score = session.get('high_score', 0)
        if play_of_hand_count > high_score:
            session['high_score'] = play_of_hand_count
            high_score = play_of_hand_count

        # Generate the plot
        plot_url = BlackjackGraphs.generate_plot(total_money_list)
        print("Plot URL generated.")

        # Return the new plot and details as an HTML snippet
        return render_template_string('''
            <div class="content">
                <div class="plot">
                    <img src="data:image/png;base64,{{ plot_url }}" alt="Title 1">
                </div>
                <div class="details">
                     <p style="font-size: 20px;">Hands played: {{ play_of_hand_count }}</p>
                <p style="font-size: 20px;">BlackJacks: {{ blackjackcount }}</p>
                <p style="font-size: 20px;">Wins: {{ wins }}</p>
                <p style="font-size: 20px;">Losses: {{ losses }}</p>
                <p style="font-size: 20px;">Pushes: {{ pushes }}</p>
                <p style="font-size: 20px;">Win %: {{ winpercentage }}%</p>
                <p style="font-size: 20px;">Most Money Obtained: {{ max_money }}</p>
                <p style="font-size: 20px;">Max Winstreak: {{ max_winstreak }}</p>
                <p style="font-size: 20px;">Max Losstreak: {{ max_losstreak }}</p>
                <br>
                <p style="font-size: 20px;">High Score (Hands Played): {{ high_score }}</p>
                </div>
            </div>
            <style>
                .content {
                    display: flex;
                    flex-direction: row;
                    align-items: flex-start;
                }
                .plot {
                    flex: 1;
                }
                .details {
                    flex: 1;
                    margin-left: 20px;
                    font-size: 18px;
                }
                .details p {
                    margin: 5px 0;
                }
            </style>
        ''', plot_url=plot_url, total_money=total_money, play_of_hand_count=play_of_hand_count,
           blackjackcount=blackjackcount, wins=wins, losses=losses, pushes=pushes,
           winpercentage=f"{winpercentage:.2f}",  # Format winpercentage to 2 decimal places
           max_money=max(total_money_list), max_winstreak=max_winstreak, max_losstreak=max_losstreak,
           high_score=high_score)

    # Initial page load
    print("Rendering initial page")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
