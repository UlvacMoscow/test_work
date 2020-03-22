import os
import csv
from collections import OrderedDict



class ParserCsv:
# path = '/var/www/litres/2_5431638534144394596/Orders.csv'
    
    def __init__(self):
        self.profit_product = {}


    def create_profit_product(self, product_id: str, profit: float, quantity: int) -> None:
        if product_id in self.profit_product:
            profit = self.profit_product[product_id][0] + profit
            quantity = self.profit_product[product_id][1] + quantity
        
        self.profit_product[product_id] = [round(profit, 2), quantity]


    def calculate_profit_product(self, temp_dict: dict) -> object:
        new_dict = {}
        for key, values in temp_dict.items():
            new_dict[key] = round(values[0]/values[1], 2)
        return OrderedDict(sorted(new_dict.items(), key=lambda t: t[1], reverse=True))


    def write_out_top_data(self, sort_order_dict, rank=10) -> None:
        print('Топ - {} лучших товаров'.format(rank))
        print(list(sort_order_dict.items())[:rank])
        print('Топ - {} худших товаров товаров'.format(rank))
        print(list(sort_order_dict.items())[:len(sort_order_dict.items()) - rank:-1])


    def csv_reader(self, file_obj):
        """
        Read a csv file
        """
        reader = csv.DictReader(file_obj, delimiter=';')
        sum_profit = 0
    
        for line in reader:
            profit = float('.'.join(line["Profit"].split(',')))
            quantity = int(line["Quantity"])
            self.create_profit_product(line['Product Name'], profit, quantity)
            sum_profit += profit
        print(round(sum_profit, 2))
        finish_profit = self.calculate_profit_product(self.profit_product)
        self.write_out_top_data(finish_profit)
        # print(calculate_profit_product(profit_product))
   


if __name__ == "__main__": 
    csv_path = os.path.normpath('/var/www/litres/2_5431638534144394596/Orders.csv')
    # csv_path = os.path.normpath(input('input path for file.csv '))

    if os.path.isfile(csv_path):
        new_parser = ParserCsv()
        with open(csv_path, "r") as csv_obj:
            new_parser.csv_reader(csv_obj)
    else:
        print('Указанный путь не является файлом! Попробуйте еще раз')