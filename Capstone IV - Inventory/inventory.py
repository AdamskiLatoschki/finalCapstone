# ========The beginning of the class==========
# This project below read data from a file and prepare a presentation of the products in inventory
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Method returns cost of the product
    def get_cost(self):
        return self.cost

    # Method returns quantity of the certain product
    def get_quantity(self):
        return self.quantity

    # String representation of the class
    def __str__(self):
        output = '======================\n'
        output += f'Country    {self.country}\n'
        output += f'Code:\t   {self.code}\n'
        output += f'Product:   {self.product}\n'
        output += f'Cost:\t   £{self.cost}\n'
        output += f'Quantity:  {self.quantity}\n'
        output += '====================='
        return output


# The list will be used to store a list of objects of shoes.
shoe_list = []


# ==========Functions outside the class==============
# Function read from file, loop through each line , create an array of objects
def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as inventory_file:
            file = inventory_file.readlines()

            for line in file[1:]:
                line = line.strip('\n')
                country, code, product, cost, quantity = line.split(',')
                cost = int(cost)
                quantity = int(quantity)
                shoes_object = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoes_object)

    except FileNotFoundError as error:
        print('\nFile does not exist', error)


def capture_shoes():
    # Function takes user inputs for the new product, creates a new object, append this object inside the shoe list
    # and write a product details to the file.
    try:
        product_country = input('Enter the country of origin of the new product: ')
        product_code = input('Enter the code of the new product: ')
        product_name = input('Enter the name of the new product: ')
        product_cost = int(input('Enter the price of the new product: '))
        product_quantity = int(input('Enter the quantity of the new product you would like to add to stock: '))

        shoes_object = Shoe(product_country, product_code, product_name, product_cost, product_quantity)
        shoe_list.append(shoes_object)
        with open('inventory.txt', 'a+') as file:
            file.write(
                f'{shoes_object.country},{shoes_object.code},{shoes_object.product},{shoes_object.cost},{shoes_object.quantity}\n')
        print('\nYour product has been added to inventory')
    except ValueError:
        print('Invalid input. Try again!')


def view_all():
    # Function iterate over the shoe_list and prints all products from inventory
    for item in shoe_list:
        print(item)


def re_stock():
    # This function sort stock quantity products and prints the lowest quantity for the user.
    # User can restock the item by adding a new quantity for this product what is then written back to the file.
    lowest_stock = min(shoe_list, key=lambda shoes: shoes.quantity)
    print(f'{lowest_stock.product} is the smallest quantity product with only {lowest_stock.quantity} in stock')
    restock = input('Would you like to restock this product? Y or N: ').lower()
    if restock == 'Y'.lower():
        while True:
            try:
                with open('inventory.txt', 'w') as inventory_file:

                    restock_quantity = int(input('Please enter the number of new stock: '))
                    lowest_stock.quantity += restock_quantity
                    inventory_file.write('Country,Code,Product,Cost,Quantity\n')
                    for item in shoe_list:
                        inventory_file.write(f'{item.country},{item.code},{item.product},{item.cost},{item.quantity}\n')

                break

            except ValueError:
                print('Invalid entry')

    # else:
    #     print('\nThank you')


def search_shoe():
    # This function allow user to search specific product by product code.
    shoe_code = input('Enter the shoe code you would like to search for: ')
    shoe_found = False
    for item in shoe_list:
        if shoe_code == item.code:
            shoe_found = True
            print(item)

    if not shoe_found:
        print('\nNo shoe found')


def value_per_item():
    # This function prints total value of each product, depends on the stock quantity in inventory
    for item in shoe_list:
        item_value = int(item.get_cost()) * int(item.get_quantity())
        print(f"The total stock value for product {item.product} is £{item_value}")


def highest_qty():
    # This function sort stock quantity products and prints the highest quantity for the user.
    # User can put this product on sale.
    highest_stock = max(shoe_list, key=lambda shoes: shoes.quantity)
    print(f'{highest_stock.product} is the highest quantity with {highest_stock.quantity} in stock')
    on_sale = input('Would you like to put this product on sale? Y or N: ').lower()

    if on_sale == 'Y'.lower():
        print(f'{highest_stock.product} is on sale now!')


# ==========Main Menu=============

read_shoes_data()
while True:
    choice = input('\nPlease choose what would you like to do:\n'
                   'd - display all stock in inventory\n'
                   's - search product by code\n'
                   'l - display the product with lowest quantity\n'
                   'v - calculate the total value of each stock item\n'
                   'h - display highest stock item and on sale\n'
                   'a - add a new product to inventory\n'
                   ':')
    if choice == 'd':
        view_all()
    elif choice == 's':
        search_shoe()
    elif choice == 'l':
        re_stock()
    elif choice == 'v':
        value_per_item()
    elif choice == 'h':
        highest_qty()
    elif choice == 'a':
        capture_shoes()
    else:
        exit()
