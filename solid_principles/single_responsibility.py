

# Reference - https://www.enjoyalgorithms.com/blog/single-responsibility-principle-in-oops

class DosaMaker:
    def makeDosa():
        pass
    def makeBatter():
        pass
    def cook():
        pass
    def serve():
        pass
    def takeOrder():
        pass
    def takePayment():
        pass


class Cashier:
    
    def take_order(self, dish):
        print(f"Order received: {dish}")
    
    def process_payment(self):
        print("Payment Processed")


class Chef:
    def prepare_dish(self, dish):
        print(f"Preparing {dish}")

class Waiter:
    def serve_dish(self, dish):
        print(f"Serving {dish}")


class DosaMaker:
    def __init__(self, cashier: Cashier, chef: Chef, waiter: Waiter):
        self.cashier = cashier
        self.chef = chef
        self.waiter = waiter

    def make_dosa(self, dish):
        self.cashier.take_order(dish)
        self.cashier.process_payment()
        self.chef.prepare_dish(dish)
        self.waiter.serve_dish(dish)


def main():
    cashier = Cashier()
    chef = Chef()
    waiter = Waiter()

    dosa_maker = DosaMaker(cashier, chef, waiter)
    dish = "Masala Dosa"
    dosa_maker.make_dosa(dish)


if __name__ == "__main__":
    main()

