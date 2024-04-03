import json

def generate_seat_layout(columns, rows):
    seats = []
    for row in range(1, rows + 1):
        for col in columns:
            seat = {'seatcol': col, 'seatrow': row}
            seats.append(seat)
    return seats

def write_seat_layout_to_json(columns, rows, filename):
    seats = generate_seat_layout(columns, rows)
    with open(filename, 'w') as file:
        json.dump(seats, file)

columns = 'ABCDEGHJK'
rows = 72
filename = 'seat_layout.json'
write_seat_layout_to_json(columns, rows, filename)
