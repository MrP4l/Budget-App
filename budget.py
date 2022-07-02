class Category:

    def __init__(self,name):
        self.name = name
        self.ledger = []
        self.balance = self.spent = 0

    def deposit(self,amount,description=""):
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self,amount,description=""):
        if self.check_funds(amount):
            self.balance -= amount
            self.spent += amount
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        return self.balance

    def transfer(self,amount,transfer):
        if self.withdraw(amount,f"Transfer to {transfer.name}"):
            transfer.deposit(amount,f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self,amount):
        return self.balance >= amount

    def __str__(self):
        stars = int(15 - (len(self.name) / 2))
        final = ("*" * stars + self.name + "*" * stars)
        for i in self.ledger:
            final += "\n" + i["description"][:23]
            amount = str(round(i["amount"],2))
            if not "." in amount:
                amount += ".00"
            elif ".0" in amount:
                amount += "0"
            
            final += " " * (30 - (len(i["description"][:23]) + len(amount[:7])))
            final += amount[:7]
        final += f"\nTotal: {self.balance}"
        return final


def create_spend_chart(categories):
    total = 0
    final = "Percentage spent by category\n"
    for i in categories:
        total += i.spent
    final += f"100|          \n"
    for i in range(90,-10,-10):
        if i == 0:
            final += " "
        final += f" {i}|"
        for j in categories:
            if round(j.spent / 10)*10/total * 100 >= i:
                final += " o "
            else:
                final += "   "
        final += " \n"
    final += "    " + "-" * ((len(categories) * 3) + 1)
    fails = greatest = 0
    for i in categories:
        if len(i.name) > greatest:
            greatest = len(i.name)
    for j in range(greatest):
        fails = 0
        final += "\n     "
        for i in categories:
            try:
                if fails > 0:
                    final += "   "
                final += i.name[j] + "  "
            except:
                fails += 1
    return final