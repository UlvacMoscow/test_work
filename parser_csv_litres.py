import os
import csv
from collections import OrderedDict
from datetime import datetime, timedelta



class ParserCsv:
# path = '/var/www/litres/2_5431638534144394596/Orders.csv'
    
    def __init__(self):
        self.sum_profit = 0
        self.profit_product = {}
        self.all_delta_delivery = []


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


    def write_out_top_product(self, sort_order_dict, rank=10) -> None:
        print('Топ - {} лучших товаров'.format(rank))
        print(list(sort_order_dict.items())[:rank])
        print('Топ - {} худших товаров товаров'.format(rank))
        print(list(sort_order_dict.items())[:len(sort_order_dict.items()) - rank:-1])


    def add_delta_delivery(self, order_data, delivery_data) -> None:
        create_order_data = datetime.strptime(order_data, '%m/%d/%y').date()
        complited_delivery_data = datetime.strptime(delivery_data, '%m/%d/%y').date()        
        self.all_delta_delivery.append((complited_delivery_data - create_order_data).days)


    def write_out_avg_delivery(self) -> print:
        avg_delivery_days = self.all_delta_delivery
        sum_days = sum(avg_delivery_days)
        count_delivery = len(avg_delivery_days)
        return print('средний срок доставки {} дн.'.format(int(round(sum_days/count_delivery, 0))))
        
        


    def counter_sum_profit(self, profit:float) -> None:
        if profit:
            self.sum_profit += profit

    def csv_reader(self, file_obj):
        """
        Read a csv file
        """
        reader = csv.DictReader(file_obj, delimiter=';')
        sum_profit = 0
    
        for line in reader:
            profit = float('.'.join(line["Profit"].split(',')))
            quantity = int(line["Quantity"])
            self.counter_sum_profit(profit) 
            self.create_profit_product(line['Product Name'], profit, quantity)
            self.add_delta_delivery(line['Order Date'], line['Ship Date'])
        print(round(sum_profit, 2))
        finish_profit = self.calculate_profit_product(self.profit_product)
        self.write_out_top_product(finish_profit)
        self.write_out_avg_delivery()
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