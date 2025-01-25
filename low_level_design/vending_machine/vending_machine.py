from abc import ABC, abstractmethod
from enum import Enum


class StateType(Enum):
    READY = "READY"
    SELECT_PRODUCT = "SELECT_PRODUCT"
    DISPENSE_PRODUCT = "DISPENSE_PRODUCT"
    DISPENSE_CHANGE = "DISPENSE_CHANGE"
    CANCEL_TRANSACTION = "CANCEL_TRANSACTION"


class State(ABC):

    @abstractmethod
    def collect_cash(self, machine: 'VendingMachine', amount: float):
        pass

    @abstractmethod
    def select_item(self, machine: 'VendingMachine', item_id: int):
        pass

    @abstractmethod
    def dispense_product(self, machine: 'VendingMachine', item_id: int):
        pass

    @abstractmethod
    def dispense_change(self, machine: 'VendingMachine', amount: float):
        pass

    @abstractmethod
    def cancel_transaction(self, machine: 'VendingMachine'):
        pass


class ReadyState(State):
    
    def collect_cash(self, machine: 'VendingMachine', amount: float):
        machine.add_collected_amount(amount)
        machine.set_state(StateType.SELECT_PRODUCT)

    def select_item(self, machine: 'VendingMachine', item_id: int):
        print("Please insert the required amount of cash before selecting an item.")

    def dispense_product(self, machine: 'VendingMachine', item_id: int):
        print("Txn not initiated, Unable to dispense item")

    def dispense_change(self, machine: 'VendingMachine', amount: float):
        print("Txn not initiated, Unable to dispense change")

    def cancel_transaction(self, machine: 'VendingMachine'):
        print("Txn not initiated, Unable to cancel transaction")


class SelectProductState(State):
    
    def collect_cash(self, machine: 'VendingMachine', amount: float):
        machine.add_collected_amount(amount)

    def select_item(self, machine: 'VendingMachine', item_id: int):
        if machine.inventory.is_product_available(item_id):
            product = machine.inventory.get_product(item_id)
            if product.price <= machine.collected_amount:
                machine.set_state(StateType.DISPENSE_PRODUCT)
                machine.dispense_product(item_id)
            else:
                print("Insufficient funds. Please insert more cash.")
        else: 
            print("Product not available. Please select another item.")

    def dispense_product(self, machine: 'VendingMachine', item_id: int):
        print("Txn not initiated, Unable to dispense item")

    def dispense_change(self, machine: 'VendingMachine', item_id: int):
        print("Txn not initiated, Unable to dispense change")

    def cancel_transaction(self, machine: 'VendingMachine'):
        machine.set_state(StateType.CANCEL_TRANSACTION)
        machine.cancel_transaction()
            
class DispenseProductState(State):

    def collect_cash(self, machine: 'VendingMachine', amount: float):
        print("Dispensing an item, Unable to collect cash")

    def select_item(self, machine: 'VendingMachine', item_id: int):
        print("Dispensing an item, Unable to select item")

    def dispense_product(self, machine: 'VendingMachine', item_id: int):
        product = machine.inventory.get_product(item_id)
        product.decrement_quantity()
        machine.set_state(StateType.DISPENSE_CHANGE)
        print("Product {} dispensed successfully.".format(product.get_name()))
        machine.set_state(StateType.DISPENSE_CHANGE)
        machine.dispense_change(machine.collected_amount - product.price)

    def dispense_change(self, machine: 'VendingMachine', amount: float):
        print("Dispensing an item, Unable to dispense change")

    def cancel_transaction(self, machine: 'VendingMachine'):
        print("Dispensing an item, Unable to cancel transaction")

class DispenseChangeState(State):

    def collect_cash(self, machine: 'VendingMachine', amount: float):
        print("Dispensing change, Unable to collect cash")

    def select_item(self, machine: 'VendingMachine', item_id: int):
        print("Dispensing change, Unable to select item")

    def dispense_product(self, machine: 'VendingMachine', item_id: int):
        print("Dispensing change, Unable to dispense item")

    def dispense_change(self, machine: 'VendingMachine', amount: float):
        print(f"Change  {amount} dispensed successfully.")
        machine.set_state(StateType.READY)
        machine.reset_collected_amount()

    def cancel_transaction(self, machine: 'VendingMachine'):
        print("Dispensing change, Unable to cancel transaction")

class CancelTransactionState(State):

    def collect_cash(self, machine: 'VendingMachine', amount: float):
        print("Cancelling the transaction, Unable to collect cash")

    def select_item(self, machine: 'VendingMachine', item_id: int):
        print("Cancelling the transaction, Unable to select item")

    def dispense_product(self, machine: 'VendingMachine', item_id: int):
        print("Cancelling the transaction, Unable to dispense item")

    def dispense_change(self, machine: 'VendingMachine'):
        print("Cancelling the transaction, Unable to dispense change")

    def cancel_transaction(self, machine: 'VendingMachine'):
        print("Cancelled the transaction. Please collect the cash")
        machine.set_state(StateType.DISPENSE_CHANGE)
        machine.dispense_change(machine.collected_amount)


class Inventory:

    def __init__(self):
        self.products = {}

    def add_product(self, product: 'Product'):
        self.products[product.id] = product

    def get_product(self, product_id: int):
        return self.products.get(product_id)

    def remove_product(self, product_id: int):
        del self.products[product_id]

    def is_product_available(self, product_id: int):
        if product_id in self.products and self.products[product_id].quantity > 0:
            return True
        return False

class Product:
    def __init__(self, id: int, name: str, price: float, quantity: int):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def decrement_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            return True
        return False

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def update_quantity(self, quantity):
        self.quantity = quantity

class VendingMachine:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.collected_amount = 0
        self.state_map = {
            StateType.READY: ReadyState(),
            StateType.SELECT_PRODUCT: SelectProductState(),
            StateType.DISPENSE_PRODUCT: DispenseProductState(),
            StateType.DISPENSE_CHANGE: DispenseChangeState(),
            StateType.CANCEL_TRANSACTION: CancelTransactionState(),
        }
        self.state =self.state_map[StateType.READY]

    def add_collected_amount(self, amount):
        self.collected_amount += amount

    def get_collected_amount(self):
        return self.collected_amount

    def reset_collected_amount(self):
        self.collected_amount = 0

    def set_state(self, state):
        self.state =self. state_map[state]

    def get_state(self, state):
        return self.state

    def collect_cash(self, amount: float):
        self.state.collect_cash(self, amount)
    
    def select_item(self, item_id: int):
        self.state.select_item(self, item_id)

    def dispense_product(self, item_id: int):
        self.state.dispense_product(self, item_id)

    def dispense_change(self, amount: float):
        self.state.dispense_change(self, amount)

    def cancel_transaction(self):
        self.state.cancel_transaction(self)


if __name__ == "__main__":

    product1 = Product(1, "Coke", 40.0, 10)
    product2 = Product(2, "Pepsi", 50.0, 10)
    product3 = Product(3, "Sprite", 30.0, 10)

    inventory = Inventory()
    inventory.add_product(product1)
    inventory.add_product(product2)
    inventory.add_product(product3)

    machine = VendingMachine(inventory)
    
    # case 1
    machine.collect_cash(20.0)
    machine.select_item(1)
    machine.collect_cash(40.0)
    machine.select_item(1)

    # case 2
    machine.collect_cash(20.0)
    machine.select_item(1)
    machine.cancel_transaction()
    
    # case 3
    machine.collect_cash(60.0)
    machine.select_item(2)



