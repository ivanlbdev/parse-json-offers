import csv
import json
import os


data_site = []
json_data = ''
xml_and_id = {}
categories = {}
errors = []
except_cat = 'Элементы питания'


def open_json():
    with open("json/Temp_relatedOffers_2022_03_30_10_55_52.json", "r", encoding='utf-8') as read_file:
        return json.load(read_file)


def open_csv():
    with open('datasite.csv', encoding='utf-8', newline='') as csv_file:
        data_csv = csv.DictReader(csv_file, delimiter=',')
        for row in data_csv:
            item_elem = {
                'xml_id': row['Внешний код'],
                'name': row['Название'],
                'site_id': row['ID'],
                'category': row['Основной раздел'],
            }
            xml_and_id[row['Внешний код']] = row['ID']
            xml_and_id[row['ID']] = row['Основной раздел']
            data_site.append(item_elem)


class MakeListOrders:
    def __init__(self, data_items):
        self.json_data = data_items
        self.object_item = {
            'xml_id': '',
            'all_count': 0,
            'all_offers': [],
        }
        self.items = []

    def make_items(self, it_object):
        for item in self.json_data:
            self.object_item['xml_id'] = item['xmlId']
            self.object_item['all_count'] = item['countRelatedOffers']
            for off_item in item[it_object]:
                self.object_item['all_offers'].append(off_item['offers'])
            self.items.append(self.object_item)
            self.object_item = {
                'xml_id': '',
                'all_offers': [],
            }
        print(self.items[0])

    def check_cat(self, item_id):
        if categories[item_id] != except_cat:
            return item_id

    def id_in_xml(self, xml_id):
        self.check_cat(xml_and_id[xml_id])
        return xml_and_id[xml_id]

    def big_list(self, item):
        count = 0
        pre_offer_list = []
        while len(pre_offer_list) < 12:
            for list_item in item['all_offers']:
                if len(list_item) > count:
                    if len(pre_offer_list) < 12:
                        try:
                            pre_offer_list.append(self.id_in_xml(list_item[count]))
                        except Exception as e:
                            errors.append(e)
            count += 1
        return pre_offer_list

    def small_list(self, item):
        pre_offer_list = []
        for list_item in item['all_offers']:
            for one_item in list_item:
                try:
                    pre_offer_list.append(self.id_in_xml(one_item))
                except Exception as e:
                    errors.append(e)
        return pre_offer_list

    def make_list_offers(self):
        for item in self.items:
            if item['all_count'] > 12:
                item['all_offers'] = self.big_list(item)
            else:
                item['all_offers'] = self.small_list(item)
        # print(self.items)
        return self.items


class MakeCsv:
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
    print(xml_and_id)
    # print(json_data['data']['data']['offers'])
    offers = MakeListOrders(json_data['data']['data']['offers'])
    offers.make_items('relatedOffers')
    done = offers.make_list_offers()
    MakeCsv(done).write_csv()
    print(os.getcwd())
    print(len(errors))