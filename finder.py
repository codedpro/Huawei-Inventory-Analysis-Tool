import csv

def search_csv(file_path, search_word):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if any(search_word in cell for cell in row):
                    print(f"Found '{search_word}' in row: {row}")
                    return
            print(f"'{search_word}' not found in the CSV file.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

file_path = "04_05_2024/Huawei_Inventory_Board.csv"
search_word = "NS723U3"
search_csv(file_path, search_word)
