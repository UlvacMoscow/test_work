import os
import csv
from collections import OrderedDict
from datetime import datetime, timedelta


class ParserCsv:

    profit_product = {}
    all_delivery_client = []
    
    def __init__(self, csv_path: str) -> None:
        self.sum_profit = 0
        self.avg_delivery_days = 0
        self.fieldnames = ['Product name', 'profit', 'quantity', 'sale']
        if os.path.isfile(csv_path):
            self.path = csv_path
        else:
            raise TypeError('Указанный путь не является файлом! Попробуйте еще раз')
            
    # task 1
    def create_profit_product(self, product_id: str, profit: float, quantity: int) -> None:
        sale = 1 
        if product_id in self.profit_product:
            profit = self.profit_product[product_id][0] + profit
            quantity = self.profit_product[product_id][1] + quantity
            sale = self.profit_product[product_id][2] + 1
        self.profit_product[product_id] = [round(profit, 2), quantity, sale]

    # task 2 & 3
    def calculate_profit_product(self, temp_dict: dict) -> object:
        new_dict = {}
        for key, values in temp_dict.items():
            new_dict[key] = round(values[0]/values[1], 2)
        return OrderedDict(sorted(new_dict.items(), key=lambda t: t[1], reverse=True))

    #task 2 & 3
    def write_out_top_product(self, sort_order_dict: dict, rank: int=10) -> None:
        print('Топ - {} лучших товаров'.format(rank))
        print(list(sort_order_dict.items())[0:rank])
        print('Топ - {} худших товаров товаров'.format(rank))
        print(list(sort_order_dict.items())[:len(sort_order_dict.items()) - rank:-1])

    #task 4
    def add_delta_delivery(self, order_data: str, delivery_data: str) -> None:
        create_order_data = datetime.strptime(order_data, '%m/%d/%y').date()
        complited_delivery_data = datetime.strptime(delivery_data, '%m/%d/%y').date()        
        self.all_delivery_client.append((complited_delivery_data - create_order_data).days)

    #task 4
    def write_out_avg_delivery(self) -> None:
        avg_delivery_days = self.all_delivery_client
        sum_days = sum(avg_delivery_days)
        count_delivery = len(avg_delivery_days)
        self.avg_delivery_days = int(round(sum_days/count_delivery, 0))
        print('средний срок доставки {} дн.'.format(self.avg_delivery_days))

    # task 5
    def avg_deviation_delivery(self) -> None:
        delta_all_delivery = [abs(el - self.avg_delivery_days) for el in self.all_delivery_client]
        avg_deviation = int(round(sum(delta_all_delivery) / len(delta_all_delivery), 0))
        print('стандартное отклонение от среднего срока доставки {} дн.'.format(avg_deviation))
  
    # task 6
    def csv_writer(self) -> None:
        """
        Write data to a CSV file path
         """
        csv_product_data = []
        
        for key, values in self.profit_product.items():
            temp_dict_data = dict(zip(self.fieldnames, [key] + values))
            csv_product_data.append(temp_dict_data)
                
        with open(os.path.join(os.path.dirname(csv_path), 'profit_product.csv'), "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=temp_dict_data)
            writer.writeheader()
            for value in csv_product_data:
                writer.writerow(value)

    def counter_sum_profit(self, profit:float) -> None:
        if profit:
            self.sum_profit += profit

    def csv_reader(self) -> None:
        """
        Read a csv file
        """
        with open(self.path, "r") as csv_obj:
            reader = csv.DictReader(csv_obj, delimiter=';')

            for line in reader:
                profit = float('.'.join(line["Profit"].split(',')))
                quantity = int(line["Quantity"])
                self.counter_sum_profit(profit) 
                self.create_profit_product(line['Product Name'], profit, quantity)
                self.add_delta_delivery(line['Order Date'], line['Ship Date'])

            print('Общий профит ', round(self.sum_profit, 2))
            finish_profit = self.calculate_profit_product(self.profit_product)
            self.write_out_top_product(finish_profit)
            self.write_out_avg_delivery()
            self.avg_deviation_delivery()
            self.csv_writer()
    

if __name__ == "__main__": 
    csv_path = os.path.normpath(input('input path for file.csv '))
    new_parser = ParserCsv(csv_path)
    new_parser.csv_reader()

