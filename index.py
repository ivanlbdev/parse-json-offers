import csv
import json

data_site = []
json_data = ''
xml_and_id = {}
categories = {}
errors = []
errors_actual = []
except_cat = 'Элементы питания'
cat_width_bat = [
    'Лазерные дальномеры',
    'Фонари',
    'Лазерные нивелиры и уровни',
    'Автомобильные аксессуары',
]
how_much_but = []


def open_json():
    """
    Открывает json файл по директории
    :return: python список из json
    """
    with open("json/Temp_relatedOffers_2022_03_30_10_55_42.json", "r", encoding='utf-8') as read_file:
        return json.load(read_file)


def open_csv():
    """
    Открывает csv и записывает данные в несколько переменных
    :return: ничего не возвращает
    """
    with open('datasite.csv', encoding='utf-8', newline='') as csv_file:
        data_csv = csv.DictReader(csv_file, delimiter=',')
        for row in data_csv:
            item_elem = {
                'xml_id': row['Внешний код'],
                'name': row['Название'],
                'site_id': row['ID'],
                'category': row['Основной раздел'],
            }
            xml_and_id[row['Внешний код']] = row['ID']  # Пишем в словарь для вычленения id
            categories[row['ID']] = row['Основной раздел']  # Пишем в словарь для вычленения категории
            data_site.append(item_elem)


class MakeListOrders:
    """
    Клас занимается созданием списка товаров и сопутки.

    """

    def __init__(self, data_items):
        self.json_data = data_items
        self.object_item = {
            'xml_id': '',
            'all_count': 0,
            'all_offers': [],
        }
        self.items = []

    @staticmethod
    def check_actual_item(xml_id):
        """
        проверяет, есть ли товар такой на основне передаваемого словаря
        :param xml_id: словарь
        :return: возвращает True, есть есть, иначе False
        """
        try:
            smth = xml_and_id[xml_id]
            return True
        except Exception as e:
            errors_actual.append(e)
            return False

    def make_items(self, it_object):
        """
        Делает предварительный список только с нужными данными
        :param it_object: идентификатор словаря с сопуткой
        :return: ничего не возвращает, заполняет self.items нужными данными
        """
        for item in self.json_data:
            ok = self.check_actual_item(item['xmlId'])
            if ok:
                self.object_item['xml_id'] = item['xmlId']
                self.check_actual_item(item['xmlId'])
                self.object_item['all_count'] = item['countRelatedOffers']
                for off_item in item[it_object]:
                    self.object_item['all_offers'].append(off_item['offers'])
                self.items.append(self.object_item)
                self.object_item = {
                    'xml_id': '',
                    'all_offers': [],
                }
        # print(self.items[0])

    @staticmethod
    def check_cat(item_id, head_item):
        """
        Проверяет категорию на исключение
        :param item_id: id товара
        :return: возвращает товар, если у него категория не исключение
        """
        try:
            head_item_id = xml_and_id[head_item]
            cat_head_item_id = categories[head_item_id]
            if cat_head_item_id in cat_width_bat:
                return item_id
            else:
                if categories[item_id] != except_cat:
                    return item_id
                else:
                    return False
        except Exception as e:
            errors.append(e)
            return False

    @staticmethod
    def id_in_xml(xml_id):
        """
        Ищет id по номенклатурнику
        :param xml_id: номенклатурник
        :return: возвращает id товара
        """
        return xml_and_id[xml_id]

    def big_list(self, item):
        count = 0
        pre_offer_list = []
        start = True
        len_offers = len(item['all_offers'])
        list_end = 0
        while len(pre_offer_list) < 12 and start:
            for list_item in item['all_offers']:
                if len(list_item) > count and len(pre_offer_list) < 12:
                    try:
                        if self.check_cat(self.id_in_xml(list_item[count]), item['xml_id']):
                            pre_offer_list.append(self.id_in_xml(list_item[count]))
                        else:
                            continue
                    except Exception as e:
                        errors.append(e)
                if len(list_item) < count:
                    list_end += 1
                if len_offers == list_end:
                    start = False

            count += 1
        return pre_offer_list

    def small_list(self, item):
        pre_offer_list = []
        for list_item in item['all_offers']:
            for one_item in list_item:
                try:
                    if self.check_cat(self.id_in_xml(one_item), item['xml_id']):
                        pre_offer_list.append(self.id_in_xml(one_item))
                    else:
                        continue
                except Exception as e:
                    errors.append(e)
        return pre_offer_list

    def make_list_offers(self):
        for item in self.items:
            if item['all_count'] > 12:
                item['all_offers'] = self.big_list(item)
            else:
                item['all_offers'] = self.small_list(item)
        print(self.items)
        return self.items


class MakeCsv:
    """
    Класс пишет в csv файл и умеет реформатировать список для этого
    """
    def __init__(self, list_data):
        self.list_data = list_data
        self.done_list = []

    def make_done_list(self):
        objects_item = []
        for item in self.list_data:
            objects_item.append(item['xml_id'])
            for i in item['all_offers']:
                objects_item.append(i)
            self.done_list.append(objects_item)
            objects_item = []

    def write_csv(self):
        self.make_done_list()
        with open('done_data.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.done_list)
            # for item in self.done_list:
            #     writer.writerow(item)


if __name__ == '__main__':
    open_csv()
    json_data = open_json()
    # print(xml_and_id)
    # print(json_data['data']['data']['offers'])
    offers = MakeListOrders(json_data['data']['data']['offers'])
    offers.make_items('relatedOffers')
    done = offers.make_list_offers()
    MakeCsv(done).write_csv()
    print(len(errors))
    print(len(errors_actual))
    print(len(how_much_but))