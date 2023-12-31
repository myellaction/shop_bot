from random import choice
from loader import db
import asyncio

menu_dict = {'Bintang': {'category_id': 4,
             'img': 'AgACAgIAAxkBAANJY9ZOTZn204PrONk7Q5UwhbP8-QMAAi_JMRvD57FKrhfPoUFvAkIBAAMCAANzAAMtBA',
             'price': 60,
             'subcategory_id': 13},
 'Carlsberg': {'category_id': 4,
               'img': 'AgACAgIAAxkBAANIY9ZNyzHKjzKhil46UTzzUndnJhkAAi3JMRvD57FK05AMuI28zBcBAAMCAANzAAMtBA',
               'price': 120,
               'subcategory_id': 13},
 'Dr. Pepper': {'category_id': 4,
                'img': 'AgACAgIAAxkBAAM9Y9ZMLxAHIlJ5AtD5VFED2m3Fk_AAAiPJMRvD57FKzFoGfugWWAgBAAMCAANzAAMtBA',
                'price': 120,
                'subcategory_id': 11},
 'Heineken': {'category_id': 4,
              'img': 'AgACAgIAAxkBAANHY9ZNmtiP9_BwDnMlFzVRhgWgAk8AAizJMRvD57FK_5KxbU1VpCEBAAMCAANzAAMtBA',
              'price': 100,
              'subcategory_id': 13},
 'Ананасовый сок': {'category_id': 4,
                    'img': 'AgACAgIAAxkBAANDY9ZNBoXMYHrvFtadBW5yiGP6aJUAAinJMRvD57FKrUzlJrUmXvgBAAMCAANzAAMtBA',
                    'price': 80,
                    'subcategory_id': 12},
 'Барбекю': {'category_id': 1,
             'img': 'AgACAgIAAxkBAAMYY9Y6CgNNUYIldlKUs-oOQSefP-sAArrIMRvD57FKTyMLAAEhryL9AQADAgADcwADLQQ',
             'price': 250,
             'subcategory_id': 3},
 'Биф чипс': {'category_id': 1,
              'img': 'AgACAgIAAxkBAAMcY9Y77RznICb-dnXU7M82rwlDZJwAAsXIMRvD57FK4huQfnCXMYMBAAMCAANzAAMtBA',
              'price': 240,
              'subcategory_id': 4},
 'Вегетерианская': {'category_id': 1,
                    'img': 'AgACAgIAAxkBAAMpY9ZGh4LWtW6PVTMGWsfBcU_bYXgAAvnIMRvD57FKyVTFN1cgbcgBAAMCAANzAAMtBA',
                    'price': 200,
                    'subcategory_id': 6},
 'Ветчена и грибы': {'category_id': 1,
                     'img': 'AgACAgIAAxkBAAMVY9Y4LxEsOGLn7CpoPB7QxccORwIAAqvIMRvD57FKxlKcLq2hO3ABAAMCAANzAAMtBA',
                     'price': 300,
                     'subcategory_id': 2},
 'Гавайская': {'category_id': 1,
               'img': 'AgACAgIAAxkBAAMlY9ZFW2v6PSOxV-0tsJOkV_Bd7ysAAu3IMRvD57FK7uV0gp2m8UYBAAMCAANzAAMtBA',
               'price': 300,
               'subcategory_id': 6},
 'Греческая': {'category_id': 1,
               'img': 'AgACAgIAAxkBAAMdY9Y8F6ASuLv6YSpTKIA0UQmgGsQAAsbIMRvD57FKpwwPogW2HzkBAAMCAANzAAMtBA',
               'price': 350,
               'subcategory_id': 4},
 'Гриль микс': {'category_id': 1,
                'img': 'AgACAgIAAxkBAAMZY9Y6j4YEKB9TmNCnL8DGO10WvzwAAr7IMRvD57FKvgABOOLBmFydAQADAgADcwADLQQ',
                'price': 350,
                'subcategory_id': 3},
 'Делюкс': {'category_id': 1,
            'img': 'AgACAgIAAxkBAAMhY9Y88gFq6xK9gmDNrXTlM3uXv0YAAszIMRvD57FKXshaR6QBajoBAAMCAANzAAMtBA',
            'price': 240,
            'subcategory_id': 5},
 'Кантри': {'category_id': 1,
            'img': 'AgACAgIAAxkBAAMbY9Y7JjyVNrehiut6liR9TUWTjV8AAsHIMRvD57FKujOdmb7wAAHcAQADAgADcwADLQQ',
            'price': 240,
            'subcategory_id': 3},
 'Карбонара': {'category_id': 1,
               'img': 'AgACAgIAAxkBAAMaY9Y62_FeTYr1afypeS4o7zWiavUAAsDIMRvD57FKVGS3Vqy8pmcBAAMCAANzAAMtBA',
               'price': 350,
               'subcategory_id': 3},
 'Карри': {'category_id': 1,
           'img': 'AgACAgIAAxkBAAMNY9Y2gLm7Rc8Hy1EWxj38e4ds9MgAAprIMRvD57FKLWUMzkou1xUBAAMCAANzAAMtBA',
           'price': 200,
           'subcategory_id': 1},
 'Картошка по-селянски': {'category_id': 2,
                          'img': 'AgACAgIAAxkBAAMtY9ZH5JCiYOZBPh7tJraSyFMLnU8AAv3IMRvD57FK3-rKE1PO18UBAAMCAANzAAMtBA',
                          'price': 80,
                          'subcategory_id': 7},
 'Картошка фри': {'category_id': 2,
                  'img': 'AgACAgIAAxkBAAMsY9ZHjyrhDEOvU4ffuIa111awfmMAAvzIMRvD57FKvv8JAjYx1J8BAAMCAANzAAMtBA',
                  'price': 100,
                  'subcategory_id': 7},
 'Кетчуп': {'category_id': 2,
            'img': 'AgACAgIAAxkBAAM5Y9ZLnMNtAS39GaC1cW2jHlY1URgAAh_JMRvD57FKOm3f5ZDJk9EBAAMCAANzAAMtBA',
            'price': 20,
            'subcategory_id': 10},
 'Кисло-сладкая': {'category_id': 1,
                   'img': 'AgACAgIAAxkBAAMPY9Y2yhO6CHczdp72o5rFA-1MqPkAAp7IMRvD57FKJq5F6GCU0XIBAAMCAANzAAMtBA',
                   'price': 200,
                   'subcategory_id': 1},
 'Клубничный сок': {'category_id': 4,
                    'img': 'AgACAgIAAxkBAANEY9ZNME3NCqmsYTBOpxo7IYMSqzkAAirJMRvD57FK5CuMylAbdG8BAAMCAANzAAMtBA',
                    'price': 80,
                    'subcategory_id': 12},
 'Кола': {'category_id': 4,
          'img': 'AgACAgIAAxkBAAM7Y9ZL6zdukd0OsyFzuI_MiYeNEO0AAiHJMRvD57FKHmAn7UJX_QkBAAMCAANzAAMtBA',
          'price': 100,
          'subcategory_id': 11},
 'Крылышки': {'category_id': 2,
              'img': 'AgACAgIAAxkBAAMvY9ZJI_vGolmhDrtR5mEZE1bpSNkAAgbJMRvD57FKGXH2FywtgfMBAAMCAANzAAMtBA',
              'price': 150,
              'subcategory_id': 8},
 'Курица гриль': {'category_id': 2,
                  'img': 'AgACAgIAAxkBAAMwY9ZJOX8UGhiuUjMJLvJRCn8Olz8AAgfJMRvD57FKajfahCeOeDcBAAMCAANzAAMtBA',
                  'price': 100,
                  'subcategory_id': 8},
 'Курица дор-блю': {'category_id': 1,
                    'img': 'AgACAgIAAxkBAAMmY9ZFgUZDnhBInaKTiJ1Fl_1uPq4AAvDIMRvD57FKsHmLgFxIKVoBAAMCAANzAAMtBA',
                    'price': 200,
                    'subcategory_id': 6},
 'Лимонный сок': {'category_id': 4,
                  'img': 'AgACAgIAAxkBAANCY9ZM52eb2eDp8Qw-ZOXvl9i-XHIAAijJMRvD57FKzBW5micYtjUBAAMCAANzAAMtBA',
                  'price': 80,
                  'subcategory_id': 12},
 'Майонезный соус': {'category_id': 2,
                     'img': 'AgACAgIAAxkBAAM2Y9ZK3NbZcuPqQOR2Q5obhXkgSgsAAhjJMRvD57FK5eCqejsiWdUBAAMCAANzAAMtBA',
                     'price': 15,
                     'subcategory_id': 10},
 'Манхэттен': {'category_id': 1,
               'img': 'AgACAgIAAxkBAAMTY9Y3e6jasMU9pik5pFY8YgH9dI4AAqDIMRvD57FK4Joj15V0lgwBAAMCAANzAAMtBA',
               'price': 250,
               'subcategory_id': 2},
 'Маргарита': {'category_id': 1,
               'img': 'AgACAgIAAxkBAAMXY9Y5zd3mErI3WDf9Ve0166aHtM0AArHIMRvD57FKORdYMI-qgE8BAAMCAANzAAMtBA',
               'price': 250,
               'subcategory_id': 3},
 'Митца': {'category_id': 1,
           'img': 'AgACAgIAAxkBAAMiY9Y9DqmX8O_VrgAB3A8R9ZXQ3EBKAALPyDEbw-exSrLz7SOdwTAXAQADAgADcwADLQQ',
           'price': 200,
           'subcategory_id': 5},
 'Нагитсы': {'category_id': 2,
             'img': 'AgACAgIAAxkBAAMxY9ZJa48RxefaY9MPsLMv52U9zg4AAgnJMRvD57FKXw4rYf06mYcBAAMCAANzAAMtBA',
             'price': 80,
             'subcategory_id': 8},
 'Пеперони': {'category_id': 1,
              'img': 'AgACAgIAAxkBAAMUY9Y4Cf6BCRQK0QkxqwhTkMFUn4cAAqHIMRvD57FKcoSLWq2GBEQBAAMCAANzAAMtBA',
              'price': 250,
              'subcategory_id': 2},
 'Пепси': {'category_id': 4,
           'img': 'AgACAgIAAxkBAAM8Y9ZMCfMCSzAnCurHJJlt7AjhGBYAAiLJMRvD57FKiZXME37l1VIBAAMCAANzAAMtBA',
           'price': 120,
           'subcategory_id': 11},
 'Прованс': {'category_id': 1,
             'img': 'AgACAgIAAxkBAAMfY9Y8W8KDKpGgY1ADL8120mI1CF4AAsjIMRvD57FKyBZ7jpbU-PwBAAMCAANzAAMtBA',
             'price': 200,
             'subcategory_id': 4},
 'Пять сыров': {'category_id': 1,
                'img': 'AgACAgIAAxkBAAMnY9ZFrgOBg6uZdyDRX0bjEKumq90AAvHIMRvD57FKuIa3usir9GsBAAMCAANzAAMtBA',
                'price': 250,
                'subcategory_id': 6},
 'Роял чизбургер': {'category_id': 1,
                    'img': 'AgACAgIAAxkBAAMkY9Y9XQiqP20wfFqG3j8qS0cjQZYAAtPIMRvD57FK0H-UDkVmR0QBAAMCAANzAAMtBA',
                    'price': 200,
                    'subcategory_id': 5},
 'Сок мультифрукт': {'category_id': 4,
                     'img': 'AgACAgIAAxkBAANBY9ZM0xZctaTX4alHKwGkYwABUJpdAAInyTEbw-exStd8iuy5mrJzAQADAgADcwADLQQ',
                     'price': 120,
                     'subcategory_id': 12},
 'Сок с арбузом': {'category_id': 4,
                   'img': 'AgACAgIAAxkBAANAY9ZMxFuqf81YUZhYGGq1lCVbdZAAAiXJMRvD57FKL2mfGDAP-wQBAAMCAANzAAMtBA',
                   'price': 60,
                   'subcategory_id': 12},
 'Соус горчичный': {'category_id': 2,
                    'img': 'AgACAgIAAxkBAAM4Y9ZLKHCF_bL9O37vAAG4V5jF5-A8AAIbyTEbw-exSklkRsjDeT0PAQADAgADcwADLQQ',
                    'price': 20,
                    'subcategory_id': 10},
 'Соус карри': {'category_id': 2,
                'img': 'AgACAgIAAxkBAAM3Y9ZK90h5BahXpgGABq--5txler8AAhnJMRvD57FKWqa0VoZ-8lIBAAMCAANzAAMtBA',
                'price': 15,
                'subcategory_id': 10},
 'Спрайт': {'category_id': 4,
            'img': 'AgACAgIAAxkBAAM-Y9ZMiafOpganBIQ_OSIUTv5HSXEAAiTJMRvD57FKyuNzwB0EDbkBAAMCAANzAAMtBA',
            'price': 80,
            'subcategory_id': 11},
 'Техас': {'category_id': 1,
           'img': 'AgACAgIAAxkBAAMWY9Y4WDQzce8bs0Fn4Kjd7Xy8xHkAAqzIMRvD57FKa5L0eTv773EBAAMCAANzAAMtBA',
           'price': 240,
           'subcategory_id': 2},
 'Тоскана': {'category_id': 1,
             'img': 'AgACAgIAAxkBAAMeY9Y8NhnBo5aJDxBTgbnkuCAjyoEAAsfIMRvD57FKwEmjVntGlMoBAAMCAANzAAMtBA',
             'price': 250,
             'subcategory_id': 4},
 'Хлебцы с сыром': {'category_id': 2,
                    'img': 'AgACAgIAAxkBAAMzY9ZKXquv9LCvJEjxeP70SkNSlAoAAhPJMRvD57FKJ5-p-RZsqTcBAAMCAANzAAMtBA',
                    'price': 150,
                    'subcategory_id': 9},
 'Хлебцы с яйцом и рисом': {'category_id': 2,
                            'img': 'AgACAgIAAxkBAAM0Y9ZKjsNdF8X0vnTbO0u7kC9uuYwAAhTJMRvD57FKhblP50p7w0UBAAMCAANzAAMtBA',
                            'price': 80,
                            'subcategory_id': 9},
 'Чикен кебаб': {'category_id': 1,
                 'img': 'AgACAgIAAxkBAAMgY9Y8guEnxHx3v_BS6EOzplS61yoAAsrIMRvD57FKXErSzoEp4aEBAAMCAANzAAMtBA',
                 'price': 300,
                 'subcategory_id': 4},
 'Чили': {'category_id': 1,
          'img': 'AgACAgIAAxkBAAMRY9Y28Z1XL35r4Iv4fLsRISLgA6YAAp_IMRvD57FKODH8hhCQeWwBAAMCAANzAAMtBA',
          'price': 200,
          'subcategory_id': 1},
 'Шпинат и фета': {'category_id': 1,
                   'img': 'AgACAgIAAxkBAAMoY9ZFxVlgQ5DDfe4UkRrnHXTB8XsAAvLIMRvD57FKW9tlfohFR7gBAAMCAANzAAMtBA',
                   'price': 300,
                   'subcategory_id': 6},
 'Экстравагантная': {'category_id': 1,
                     'img': 'AgACAgIAAxkBAAMjY9Y9Lq7PIQSRpnQsmgmT0_kqVA0AAtDIMRvD57FKAxtGYAYwSBUBAAMCAANzAAMtBA',
                     'price': 350,
                     'subcategory_id': 5}}

menu_list = ['Карри', 'Кисло-сладкая', 'Чили', 'Ветчена и грибы', 'Манхэттен',
             'Пеперони', 'Техас', 'Барбекю', 'Гриль микс', 'Кантри', 'Карбонара',
             'Маргарита', 'Биф чипс', 'Греческая', 'Прованс', 'Тоскана', 'Чикен кебаб',
             'Делюкс', 'Митца', 'Роял чизбургер', 'Экстравагантная', 'Вегетерианская',
             'Гавайская', 'Курица дор-блю', 'Пять сыров', 'Шпинат и фета', 'Картошка по-селянски',
             'Картошка фри', 'Крылышки', 'Курица гриль', 'Нагитсы', 'Хлебцы с сыром',
             'Хлебцы с яйцом и рисом', 'Кетчуп', 'Майонезный соус', 'Соус горчичный',
             'Соус карри', 'Dr. Pepper', 'Кола', 'Пепси', 'Спрайт', 'Ананасовый сок',
             'Клубничный сок', 'Лимонный сок', 'Сок мультифрукт', 'Сок с арбузом', 'Bintang',
             'Carlsberg', 'Heineken']

categories =['🍕 Пицца', '🥙 Снеки', '1', "🥤 Напитки"]
subcategories={1:['🍕 Паназиатские вкусы', '🍕 Лучшая цена','🍕 Классическая пицца','🍕 Необычная пицца',
                  "🍕 Файнест", '🍕 Гурме'],
               2: ['🍟 Картошка', "🍗 Курица", "🍞 Хлебцы", "🍛 Соусы"],
               4:['🥤 Вода', '🍹 Соки','🍺 Пиво']}

async def make_data(menu_list, menu_dict):
    for i in categories:
        await db.add_category(i)
    for i in subcategories:
        for j in subcategories[i]:
            await db.add_subcategory(j,i)
    for i in menu_list:
        name = i
        price = menu_dict[i].get('price')
        category_id = menu_dict[i]['category_id']
        subcategory_id = menu_dict[i]['subcategory_id']
        img = menu_dict[i]['img']
        await db.add_item(name = name, price= price, category_id = category_id,
                          subcategory_id = subcategory_id, img = img)


#loop = asyncio.get_event_loop()
#loop.run_until_complete(make_data(menu_list, menu_dict))




