Скрипт парсит json определенного формата и возвращает список словарей вида:<br>
[<br>
{'xml_id': 'X40013283', 'all_offers': ['167905', '721384', '696557', '696327', '1084692', '167901', '696748', '167904', '721386', '696384', '696225', '695381'], 'all_count': 67},<br>
{'xml_id': 'Х130833132', 'all_offers': ['1095114', '504584', '389388', '1094772', '577836', '695878', '1096670', '504565', '389397', '1094774', '577833', '696444'], 'all_count': 39}<br>
]

Затем этот список записывает в csv, который пригоден для стандартного импорта csv в bitrix

Скрипт формирует список сопутки.<br>
Макисмальное количество сопутки - 12 штук.<br>
Скрипт исключает из сопутки батарейки для всех товаров, кроме тех,<br>
что лежат в следующих категориях: Лазерные дальномеры, Фонари, Лазерные нивелиры и уровни, Автомобильные аксессуары