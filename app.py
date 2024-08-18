from flask import Flask, render_template, request, render_template_string, session, jsonify
import matplotlib
import matplotlib.pyplot as plt
import io
import BlackJack
import base64
import BlackJackPML
import BlackJackGraph


matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = 'BlackJack' 

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            strategy = request.form['strategy']
            starting_bet = int(request.form['starting_bet'])
            total_cash = int(request.form['total_cash'])

            if total_cash < starting_bet:
                return jsonify({'error': 'Total cash amount must be greater than or equal to the starting bet.'}), 400

            
            print(f"Received POST request with strategy: {strategy}, starting_bet: {starting_bet}, total_cash: {total_cash}")

            
            print("Running BlackJack simulation with strategy:", strategy)
            BlackJack.main(strategy, total_cash, starting_bet)
            predictionfinal = BlackJackPML.main(strategy, starting_bet, total_cash) 
            print(f'Predict final: {predictionfinal}')
            
            total_money_list = BlackJack.total_money_list
            total_money = total_money_list[-1]
            play_of_hand_count = BlackJack.play_of_hand_count
            blackjackcount = BlackJack.blackjackcount
            win_loss_history = BlackJack.win_loss_history
            wins = win_loss_history.count("win")
            losses = win_loss_history.count("loss")
            pushes = win_loss_history.count("push")

           
            winpercentage = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0

            max_winstreak, max_losstreak = BlackJack.max_win_loss(win_loss_history)

        
            high_score = session.get('high_score', 0)
            if play_of_hand_count > high_score:
                session['high_score'] = play_of_hand_count
                high_score = play_of_hand_count

            
            plot_url = BlackJackGraph.main(total_money_list)
            print("Plot URL generated.")
          

            return jsonify({
                'plot_url': plot_url,
                'play_of_hand_count': play_of_hand_count,
                'blackjackcount': blackjackcount,
                'wins': wins,
                'losses': losses,
                'pushes': pushes,
                'winpercentage': f"{winpercentage:.2f}",
                'max_money': max(total_money_list),
                'max_winstreak': max_winstreak,
                'max_losstreak': max_losstreak,
                'high_score': high_score,
                'predictionfinal': predictionfinal
            })

        except ValueError:
            return jsonify({'error': 'Please enter valid numeric values for starting bet and total cash.'}), 400

    
    print("Rendering initial page")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
