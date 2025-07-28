import sys
import csv
import json
import pickle

class Reader:
    def __init__(self, file):
        self.file = file
        self.data = []

    def read(self):
        if self.file.endswith('.csv'):
            with open(self.file) as f:
                self.data = [row for row in csv.reader(f)]
        elif self.file.endswith('.json'):
            with open(self.file) as f:
                self.data = json.load(f)
        elif self.file.endswith('.txt'):
            with open(self.file) as f:
                self.data = [line.strip().split(',') for line in f]
        elif self.file.endswith('.pickle'):
            with open(self.file, 'rb') as f:
                self.data = pickle.load(f)

class Writer:
    def __init__(self, file, data):
        self.file = file
        self.data = data

    def write(self):
        if self.file.endswith('.csv'):
            with open(self.file, 'w', newline='') as f:
                csv.writer(f).writerows(self.data)
        elif self.file.endswith('.json'):
            with open(self.file, 'w') as f:
                json.dump(self.data, f)
        elif self.file.endswith('.txt'):
            with open(self.file, 'w') as f:
                for row in self.data:
                    f.write(','.join(row) + '\n')
        elif self.file.endswith('.pickle'):
            with open(self.file, 'wb') as f:
                pickle.dump(self.data, f)

def change(data, changes):
    for c in changes:
        parts = c.split(',')
        if len(parts) != 3:
            print(f"Ignoring invalid change: {c}")
            continue
        x, y, v = parts
        try:
            data[int(y)][int(x)] = v
        except (IndexError, ValueError):
            print(f"Could not apply change: {c}")
    return data

def main():
    if len(sys.argv) < 3:
        print("Usage: python dziedziczenie.py <input> <output> <change1> <change2> ...")
        return

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    changes = sys.argv[3:]

    r = Reader(in_file)
    r.read()
    d = r.data
    d = change(d, changes)

    for row in d:
        print(','.join(row))

    w = Writer(out_file, d)
    w.write()

if __name__ == '__main__':
    main()
