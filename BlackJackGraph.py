import BlackJack
import matplotlib.pyplot as plt  
import base64
import io


def main(total_money_list):
    img = io.BytesIO()
    hands_xaxis = list(range(1, len(total_money_list) + 1))   
    
    fig, ax = plt.subplots(facecolor = '#0a9d2585')
    ax.plot(hands_xaxis, total_money_list, marker='o', linestyle='-', color='black', label='Total Money', linewidth=1)


    ax.set_title('Balance Over Hands', fontsize=12)

    ax.set_xlabel('Hands Played')
    ax.set_ylabel('Total Money ($)')
    ax.grid(True)
    ax.legend()

    fig.tight_layout(rect=[0, 0, 1, 0.95])  
    fig.savefig(img, format='png')
    plt.close(fig)
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url



if __name__ == "__main__":
    main()
