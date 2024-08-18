import csv
import BlackJack

# Run the main function from the BlackJack module
#BlackJack.main()
def main():
# Prepare the row to write
    row_to_write = [BlackJack.method, BlackJack.total_money_list[0], BlackJack.bet_amount,BlackJack.play_of_hand_count+1]

# Debug print to check the row to write
    print("Row to write:", row_to_write)

# Initialize existing_data as an empty list in case the file doesn't exist
    existing_data = []

# Try to read the existing data from the CSV file
    try:
        with open('newdatalol.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            existing_data = list(reader)
        # Debug print to check existing data
            #print("Existing data:", existing_data)
    except FileNotFoundError:
    # File doesn't exist, proceed with creating a new one
        print("File not found, creating new file.")

# Append the new row to the existing data
    existing_data.append(row_to_write)

# Debug print to check combined data
    #print("Combined data:", existing_data)

# Write the combined data back to the CSV file
    with open('newdatalol.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)

    print("Data written to file successfully.")



if __name__ == "__main__":
    main()
