class Share():
    def __init__(self, member_name, amount, members_count = 1):
        self.member_name = member_name
        self.amount = amount
        self.members_count = members_count
        self.money = 0.0

    def print_data(self):
        print(
            self.member_name, 
            "have" if self.members_count > 1 else "has",
            self.amount
        )
        print("Total share:", float(self.money))
        if self.members_count > 1:
            print("Each one takes:", float(self.money) / self.members_count)
    
