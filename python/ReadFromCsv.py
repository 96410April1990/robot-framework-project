import csv

def read_csv(file_path):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                print(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError:
        print(f"IO error occurred while accessing the file: {file_path}")

