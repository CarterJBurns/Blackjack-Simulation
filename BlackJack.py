import random
import csvmaker


blackjackcount = 0
win_loss_history = []
total_money = 0
total_money_list = []
play_of_hand_count = 0
#method = ""
bet_amount = 0

def blackjack_book(player_total: int, dealer_up_card: int, first_card: int, second_card: int) -> str:
    hard_totals = {
        8: "Hit", 9: "Double" if 3 <= dealer_up_card <= 6 else "Hit",
        10: "Double" if dealer_up_card <= 9 else "Hit",
        11: "Double", 12: "Stand" if 4 <= dealer_up_card <= 6 else "Hit",
        13: "Stand" if dealer_up_card <= 6 else "Hit",
        14: "Stand" if dealer_up_card <= 6 else "Hit",
        15: "Stand" if dealer_up_card <= 6 else "Hit",
        16: "Stand" if dealer_up_card <= 6 else "Hit",
        17: "Stand", 18: "Stand", 19: "Stand", 20: "Stand", 21: "Stand"
    }

    soft_totals = {
        13: "Hit", 14: "Hit", 15: "Hit", 16: "Hit", 17: "Hit",
        18: "Stand" if 2 <= dealer_up_card <= 8 else "Hit",
        19: "Stand", 20: "Stand", 21: "Stand"
    }

    if 11 in (first_card, second_card):
        return soft_totals.get(player_total, "Hit")
    else:
        return hard_totals.get(player_total, "Hit")

def play_of_hand(first_card: int, second_card: int, dealer_up_card: int, player_total: int, bet_amount: int, total_money: int) -> (str, int):
    global play_of_hand_count
    play_of_hand_count += 1
    nomoney = False
    while player_total < 21:
        if not nomoney:
            choice = blackjack_book(player_total, dealer_up_card, first_card, second_card)
        else:
            choice = "Hit"
        if choice == "Hit":
            player_total += random.randint(1, 11)
        elif choice == "Stand":
            break
        elif choice == "Double":
            if bet_amount * 2 <= total_money:
                player_total += random.randint(1, 11)
                bet_amount *= 2
                total_money -= bet_amount // 2  
            else:
                nomoney = True
            break

    while dealer_up_card < 17:
        dealer_up_card += random.randint(1, 11)

    if player_total > 21:
        total_money -= bet_amount
        return "loss", total_money
    elif dealer_up_card > 21:
        total_money += bet_amount
        return "win", total_money
    elif player_total > dealer_up_card:
        total_money += bet_amount
        return "win", total_money
    elif player_total == dealer_up_card:
        return "push", total_money
    else:
        total_money -= bet_amount
        return "loss", total_money


def automation(initial_bet_amount: int, method: str, total_money: int) -> (int, list, list):
    global blackjackcount, win_loss_history, total_money_list, play_of_hand_count

    bet_amount = initial_bet_amount

    first_card = random.randint(1, 11)
    second_card = random.randint(1, 11)
    dealer_up_card = random.randint(1, 11)
    player_total = first_card + second_card
    bj = False

    if player_total == 21:
        win_loss_history.append("win")
        blackjackcount += 1
        play_of_hand_count += 1
        total_money += bet_amount * 1.5
        bj = True
    else:
        result, total_money = play_of_hand(first_card, second_card, dealer_up_card, player_total, bet_amount, total_money)
        win_loss_history.append(result)

    if win_loss_history[-1] == "win" and not bj:
        if method == "R":
            bet_amount *= 2
        elif method == "P" and len(win_loss_history) >= 3 and win_loss_history[-3:] == ['win', 'win', 'win']:
            bet_amount = 10
        elif method == "F":
            bet_amount = 10
    elif win_loss_history[-1] == "loss":
        if method == "M":
            bet_amount = min(bet_amount * 2, total_money)
        else:
            bet_amount = 10

    total_money_list.append(total_money)
    return total_money, win_loss_history, total_money_list



def max_win_loss(win_loss_history):
    max_winstreak = max_losstreak = current_winstreak = current_losstreak = 0

    for result in win_loss_history:
        if result == 'win':
            current_winstreak += 1
            current_losstreak = 0
            max_winstreak = max(max_winstreak, current_winstreak)
        elif result == 'loss':
            current_losstreak += 1
            current_winstreak = 0
            max_losstreak = max(max_losstreak, current_losstreak)
    return max_winstreak, max_losstreak


def main(strategy="F", initial_money=500, initial_bet=10) -> None:
    global blackjackcount, win_loss_history, total_money, total_money_list, play_of_hand_count, bet_amount, method

    total_money = initial_money
    blackjackcount = 0
    bet_amount = initial_bet
    win_loss_history = []
    total_money_list = [total_money]
    play_of_hand_count = 0
    method = strategy
    
    while total_money > 0 and total_money >= bet_amount and len(total_money_list) < 10000:
        total_money, win_loss_history, total_money_list = automation(bet_amount, method, total_money)
    max_win_loss(win_loss_history)
    
    print(f'Method: {method}')
    print(f"Final bet total: {total_money}\n")
    print(f'Hands played: {play_of_hand_count}\n')
    print(f"BlackJacks: {blackjackcount}\n")
    wins = win_loss_history.count("win")
    losses = win_loss_history.count("loss")
    pushes = win_loss_history.count("push")
    print(f"Wins: {wins}\n")
    print(f"Losses: {losses}\n")
    print(f'Pushes: {pushes}\n')
    print(f'Initial Bet: {initial_bet}\n')
    print(f'Initial Money: {initial_money}\n')
    print(f'Most Money Obtained: {max(total_money_list)}')
    csvmaker.main()

    

if __name__ == "__main__":
    main()
