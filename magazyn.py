class Manager:
    def __init__(self):
        self.balance = 0.0
        self.inventory = {}
        self.history = []
        self.commands = {}
        self.load_data()

    def assign(self, name, function):
        self.commands[name] = function

    def execute(self, name):
        if name in self.commands:
            self.commands[name]()
            if name != "koniec":
                self.history.append(name)
        else:
            print("Nieznana komenda.")

    def save_data(self):
        with open("data.txt", "w") as file:
            file.write(f"balance:{self.balance}\n")
            file.write(f"inventory:{str(self.inventory)}\n")
            file.write(f"history:{str(self.history)}\n")

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                for line in file:
                    key, value = line.strip().split(":", 1)
                    if key == "balance":
                        self.balance = float(value)
                    elif key == "inventory":
                        self.inventory = eval(value) if value else {}
                    elif key == "history":
                        self.history = eval(value) if value else []
        except FileNotFoundError:
            print("Brak danych. Rozpoczynanie od zera.")
        except Exception:
            print("Błąd wczytywania danych. Rozpoczynanie od zera.")

    def saldo(self):
        amount = float(input("Podaj kwotę do dodania lub odjęcia z konta: "))
        self.balance += amount
        print(f"Nowe saldo: {self.balance}")

    def sale(self):
        name = input("Podaj nazwę produktu: ")
        price = float(input("Podaj cenę produktu: "))
        quantity = int(input("Podaj liczbę sztuk: "))
        if name in self.inventory and self.inventory[name] >= quantity:
            self.inventory[name] -= quantity
            self.balance += price * quantity
            print(f"Sprzedano {quantity} sztuk {name}. Nowe saldo: {self.balance}")
        else:
            print("Brak wystarczającej ilości produktu w magazynie.")

    def purchase(self):
        name = input("Podaj nazwę produktu: ")
        price = float(input("Podaj cenę produktu: "))
        quantity = int(input("Podaj liczbę sztuk: "))
        if self.balance >= price * quantity:
            self.inventory[name] = self.inventory.get(name, 0) + quantity
            self.balance -= price * quantity
            print(f"Zakupiono {quantity} sztuk {name}. Nowe saldo: {self.balance}")
        else:
            print("Brak wystarczającego salda na zakup.")

    def account_status(self):
        print(f"Stan konta: {self.balance}")

    def list(self):
        if self.inventory:
            print("Stan magazynu:")
            for product, quantity in self.inventory.items():
                print(f"{product}: {quantity} sztuk")
        else:
            print("Magazyn jest pusty.")

    def warehouse_status(self):
        name = input("Podaj nazwę produktu: ")
        if name in self.inventory:
            print(f"Stan magazynu dla {name}: {self.inventory[name]} sztuk")
        else:
            print(f"Produkt {name} nie znajduje się w magazynie.")

    def view(self):
        start_index = input("Podaj początkowy indeks: ")
        end_index = input("Podaj końcowy indeks: ")
        start_index = int(start_index) if start_index else 0
        end_index = int(end_index) if end_index else len(self.history) - 1

        if 0 <= start_index <= end_index < len(self.history):
            print("Przegląd działań:")
            for i in range(start_index, end_index + 1):
                print(f"{i}: {self.history[i]}")
        else:
            print("Indeks spoza zakresu.")

    def end(self):
        print("Kończę działanie programu.")
        self.save_data()
        exit()

manager = Manager()
manager.assign("saldo", manager.saldo)
manager.assign("sprzedaż", manager.sale)
manager.assign("zakup", manager.purchase)
manager.assign("konto", manager.account_status)
manager.assign("lista", manager.list)
manager.assign("magazyn", manager.warehouse_status)
manager.assign("przegląd", manager.view)
manager.assign("koniec", manager.end)

while True:
    print("\nWybierz opcję:")
    print("1. saldo")
    print("2. sprzedaż")
    print("3. zakup")
    print("4. konto")
    print("5. lista")
    print("6. magazyn")
    print("7. przegląd")
    print("8. koniec")
    option = input("Wybór: ")
    options_map = {
        "1": "saldo",
        "2": "sprzedaż",
        "3": "zakup",
        "4": "konto",
        "5": "lista",
        "6": "magazyn",
        "7": "przegląd",
        "8": "koniec"
    }
    command = options_map.get(option)
    if command:
        manager.execute(command)
    else:
        print("Spróbuj ponownie.")
