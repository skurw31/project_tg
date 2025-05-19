import asyncio
import sqlite3
import random
import re
import openai
import schedule
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



TOKEN_API = 'YOUR_TOKEN'

bot = Bot(token=TOKEN_API)
dp = Dispatcher()
 


yes_udon = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Конечно!")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

yes_ramen = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Кoнечно!")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

yes_chick = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Конечнo!")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

yes_konk = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Приступим")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

yes_borsh = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Гoтoв")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

yes_carb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Гoтов")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

# Да или Нет( Для Болоньезе)
yes_bolon = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Готов")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)

# Да или Нет( Для BOURGUIGNON)
yes_bour = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Дa")],
    [KeyboardButton(text="Нет")],
    
], resize_keyboard=True)
# Да или Нет( Для жульена)
yes_or_no = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Да")],
    [KeyboardButton(text="Нет")],
], resize_keyboard=True)
# Оценка
response = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Все было очень вкусно!")],
    [KeyboardButton(text="Не особо понравилось")],
], resize_keyboard=True)

# Меню start 
main_menu_but = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Главное меню")],
    [KeyboardButton(text="Поддержка")],
    [KeyboardButton(text="Помощь")],
    [KeyboardButton(text="Wiki")],
], resize_keyboard=True)  # Создаем клавиатуру и передаем список кнопок

# Меню при нажатии на главное меню
menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🛎️ Страна 🛎️"),
        KeyboardButton(text="⏰Таймер⏰"),
        ],
    [
        KeyboardButton(text="🎵 Музыка 🎵"),
        KeyboardButton(text='Назад')
    ]
], resize_keyboard=True)
# меню музыки
music_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Бодрая"),
        KeyboardButton(text="Веселся"),
        KeyboardButton(text="Спокойная")
        ],
    [
        KeyboardButton(text="Грустная"),
        KeyboardButton(text='Назад')
     ]
], resize_keyboard=True
)
# Выбор формата времени(секунды/минуты/часы)
choice = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Секунды")],
    [KeyboardButton(text="Минуты")],
    [KeyboardButton(text="Часы")],
], resize_keyboard=True) 
# секунды
second = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="10")],
    [KeyboardButton(text="15")],
    [KeyboardButton(text="30")],
    [KeyboardButton(text="45")],
], resize_keyboard=True) 
# минуты
minute = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="1"),
        KeyboardButton(text="3"),
        KeyboardButton(text="5")
        ],
    [
        KeyboardButton(text="10"),
        KeyboardButton(text='15'),
        KeyboardButton(text="30"),        
     ],
    [
        KeyboardButton(text="40"),
        KeyboardButton(text="45"),
        KeyboardButton(text="50")
        ],
], resize_keyboard=True
) 
# часы
hour = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="1"),
        KeyboardButton(text="1.5"),
        KeyboardButton(text="2")
        ],
    [
        KeyboardButton(text="3"),
        KeyboardButton(text='4')
     ]
], resize_keyboard=True
)
# Меню стран кулинарии
country_menu = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Франция"),
            KeyboardButton(text="Италия"),
            KeyboardButton(text="Япония")
        ],
        [
            KeyboardButton(text="Мексика"),
            KeyboardButton(text="Россия"),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)


fr_cook_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Блюда")],
    [KeyboardButton(text="История")]
], resize_keyboard=True)

it_cook_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Блюда")],
    [KeyboardButton(text="История")]
], resize_keyboard=True)

mx_cook_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Блюда")],
    [KeyboardButton(text="История")]
], resize_keyboard=True)

ru_cook_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Блюда")],
    [KeyboardButton(text="История")]
], resize_keyboard=True)

jp_cook_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Блюда")],
    [KeyboardButton(text="История")]
], resize_keyboard=True)

# итальянские блюда  
italy = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Лазания")],
    [KeyboardButton(text="Болоньезе")],
    [KeyboardButton(text="Карбонара")]
], resize_keyboard=True)

# французские блюда  
france = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Жульен")],
    [KeyboardButton(text="Беф-бургиньон")],
], resize_keyboard=True)
# русские блюда 
russia = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Борщ")]
], resize_keyboard=True)
# мексиканские блюда \
mexico = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Чили кон карне")]    
], resize_keyboard=True)
# японские блюда

japan = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Лапша удон с курицей")],
    [KeyboardButton(text="Рамен")],
    [KeyboardButton(text="Курица терияки")],
], resize_keyboard=True)

# помощь с выбором вина для блюда  
bourguignon_vine = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Хочу узнать про вино")],
    [KeyboardButton(text="Не стоит")],
], resize_keyboard=True)

HELP_COMMAND = '''
конечно мы поможем, данный бот покажет вам, что готовка это шикарно. Но главное помните, что рецептов бывает много, и не обязательно использовать именно наш
'''


WIKI = '''
Знаете....

Данный бот был создан чтоб поделиться, поделиться блюдами. Чтоб вы тоже влюбились в кулинарию, как я. Ведь готовка, это холст, а ты художник. Именно за тобой выбор, что, как и при аких обстоятельствах будет создано.

Главное помните, рецепты в боте не единственные, если много различных рецептов одних и тех же блюд. В моем боте, рецепты которые я использую и который нравятся конкретно мне.

Творите!❤️❤️❤️
'''


###############################################
'''РЕЦЕПТЫ'''


'''FRANCE'''
JULIEN = '''
• Куриное филе: 800 грамм
• Шампиньоны: 200-300 грамм
• Молоко: 1 литр
• Приправы Maggi(как на фото): 2 пачки с грибами
• Сыр(можно почти любой, главное чтобы он таял,  не плавился)
''' 

BOURGUIGNON = '''
• Говядина: 2-3 кг
• Мясной бульон: 800 мл(можно из кубиков)
• Бекон: 300 грамм
• Лук репчатый: 2 головки
• Морковь: 4 штуки
• Чеснок: 6 зубчиков
• Томатная паста: 3-4 ст. л.
• Мука 4 ст. л.
• Вино красное сухое: 1-1.5 литра
• Лавровый лист: 4 штуки
'''

BOURGUIGNON_VINE = '''
Я бы посоветовл вам взять австралию или францию, их вина идеально гармонируют с мясом.
Так же он придает нежный привкус, в отличие от других, но это не означает, что другие вина плохие, просто эти лучше😁
Если же советовать по самим винам, то я бы порекомендовал:
Pinot Noir, Франция(Бургундия)
Gamay, Франция(Божоле)
Merlot, Франция(Бордо)
Cabernet Franc, Франция(Луара)
Syrah, Франция/Австралия(Рона)
'''

'''ITALY'''

BOLOGNESE = '''
• Фарш говяжий: 800 грамм
• Фарш домашний: 250 грамм
• Томатная паста: 600 грамм
• Спагетти( можно барилла №5)
• Лук репчатый: 1 луковица
'''

CARBONARA = '''
• Яйца куриные: 4 штуки
• Сыр Пармезан: 150 грамм
• Спагетти: Пачка
• Бекон: 200-300 грамм
• Сливки: 400 мл(20%)
'''

'''RUSSIA'''

BORSH = '''
• Говядина - 500 грамм
• Свёкла - 1 шт.
• Картофель - 2 шт.
• Капуста белокочанная - 200 грамм
• Морковь - 1 шт.
• Лук репчатый - 1 шт.
• Томатная паста - 1 ст. ложка
• Масло растительное - 2 ст. ложки
• Уксус - 1 ч. ложка
• Лавровый лист - 1 шт.
• Перец чёрный горошком - 2-3 шт.
• Соль - 2 ч. ложки (по вкусу)
• Вода - 1,5 л
• Зелень укропа и/или петрушки (для подачи) - 3-4 веточки
'''



'''MEXICO'''

KON_KARNE = '''
• Филе говядины 250 грамм
• Фасоль (отварная или консервированная) 200 грамм
• Болгарский перец  1 шт.
• Стебель сельдерея 0.5  шт.
• Лук 1  шт.
• Чеснок 1  зубч.
• Помидоры (в собственной соку) 150  грамм
• Растительное масло 1  стол.л.
• Соль 1  чайн. л.
• Перец острый молотый по вкусу
• Вода 1 стакан  
'''



'''JAPAN'''

UDON_NOODLES = '''
• Растительное масло 50 мл
• Лимон 1 штука
• Чеснок 4 зубчика
• Перец чили 1 штука
• Имбирь 50 грамм
• Зеленый лук 100 грамм
• Куриное филе 400 грамм
• Куриный бульон 2 л
• Соевый соус 50 мл
• Анис (бадьян) 2 штуки
• Вешенки 200 грамм
• Лапша удон 400 грамм
• Сладкий перец 1 штука
'''

TERIYAKI_CHIKEN = '''
• Репчатый лук 50 грамм
• Растительное масло 50 мл
• Чеснок 2 зубчика
• Имбирь 10 грамм
• Зеленый лук по вкусу
• Куриное филе 600 грамм
• Саке 3 столовые ложки
• Коричневый сахар 3 столовые ложки
• Легкий соевый соус 70 мл
• Кунжут по вкусу
'''

RAMEN = '''
• Сахар 2 столовые ложки
• Куриное яйцо 4 штуки
• Чеснок 2 зубчика
• Имбирь 50 грамм
• Зеленый лук 50 грамм
• Куриный бульон 1 л
• Соевый соус 140 мл
• Кинза по вкусу
• Анис (бадьян) 2 штуки
• Свиная грудинка 500 грамм
• Ростки сои 150 грамм
• Лапша рамен 200 грамм
• Мисо-паста 1 столовая ложка
• Рисовое вино 80 мл

''' 
###############################################


'''ПРИВЕТСТВИЕ'''
# start(появляется аля привета)
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=main_menu_but)
    
# Обработчик нажатия кнопки "Начнем"(тоже самое что и /start)
# Обработчик нажатия кнопки "Главное меню"


'''START'''
#команда для юза админа

    
# кнопка Главного меню  
@dp.message(lambda message: message.text == "Главное меню")
async def support_command(message: Message):
    await message.answer("Отлично!!! Теперь выбери, с чем тебе помочь", reply_markup=menu)
    
    
#команда для юза админа
@dp.message(Command("support"))
async def support_command(message: Message):
    admin_username = 'skurw'
    await message.answer(f"Конечно мы поможем!, вот наш админ -> @{admin_username}", reply_markup=main_menu_but)

# кнопка для юза админа   
@dp.message(lambda message: message.text == "Поддержка")
async def support_command(message: Message):
    admin_username = 'skurw'
    await message.answer(f"Конечно мы поможем!, вот наш админ -> @{admin_username}", reply_markup=main_menu_but)

# команда help        
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_COMMAND)

# Обработчик нажатия кнопки "Помощь"(тоже самое что и /help)
@dp.message(lambda message: message.text == "Помощь")
async def help_button(message: Message):
    await message.answer(HELP_COMMAND, reply_markup=main_menu_but)


@dp.message(lambda message: message.text == "Wiki")
async def support_command(message: Message):
    await message.answer(WIKI, reply_markup=main_menu_but)

'''МЕНЮ ПРИ НАЖАТИИ НА ГЛАВНОЕ МЕНЮ'''

##########################################################



@dp.message(lambda message: message.text == "⏰Таймер⏰")
async def support_command(message: Message):
    await message.answer("Добро пожаловать в таймер!")
    await message.answer("Выбери что тебе надо(секунды, минуты или часа)")
    await message.answer('Вот список блюд:', reply_markup=choice)
# Секунды
@dp.message(lambda message: message.text == "Секунды")
async def support_command(message: Message):  
    await message.answer('Сколько секунд тебе надо?:', reply_markup=second) 

@dp.message(lambda message: message.text == "15")
async def support_command(message: Message):  
    def task():  
        schedule.every(15).minutes.do(task)

while True:
    schedule.run_pending() # Вызываем все задачи, время которых подошло
    time.sleep(1)
    break 

# кол-во минут

# Часы
@dp.message(lambda message: message.text == "Часы")
async def support_command(message: Message):  
    await message.answer('Сколько часов тебе надо?:', reply_markup=hour) 
# кол-во часов  
    
    
    
##########################################################    
# Музыка
@dp.message(lambda message: message.text == "🎵 Музыка 🎵")
async def ask_time_input(message: Message, state: FSMContext):
    await message.answer(f'Отлично!!!!')
    await message.answer("Какую музыку вам подобрать?", reply_markup=music_menu)


'''ПРИ НАЖАТИИ НА СТРАНА'''
    
@dp.message(lambda message: message.text == "🛎️ Страна 🛎️")
async def support_command(message: Message):
    await message.answer("Потрясающе!")
    await message.answer("У нас есть кухни таких стран:", reply_markup=country_menu)

'''ФРАНЦИЯ'''

# Франция
@dp.message(lambda message: message.text == "Франция")
async def support_command(message: Message):
    await message.answer("Шикарная страна и кухня!")
    await message.answer("Моя любимая)")
    await message.answer('Вот список блюд:', reply_markup=france)
    
# Жульен
@dp.message(lambda message: message.text == "Жульен")
async def support_command(message: Message):
    await message.answer("Потрясающий выбор!")
    await message.answer("Для данного блюда, вам понадовится:(на 5 порций)")
    await message.answer(JULIEN) 
    await message.answer('Приступить к рецепту?', reply_markup=yes_or_no)

# Рецепт жульена
@dp.message(lambda message: message.text == "Да")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")
    await message.answer(" Сначалаа мы все подготовим, а затем начнем делать")
    await message.answer('Перед готовкой, включите духовку на 180 - 200 градусов Цельсия( или 356 - 392 градусов Фарангейта)\n\n'
                         '1.  Возьмите курицу и нарежьте ее кубиками, примерно по 2-3 см \n\n'
                         '2.  Если вы купили обычные шампиньоны, тогда отрежьте ножку и нарежьте на дольки( если замороженные, ничего не делаем\n\n'
                         '3.  Сыр натрите на терке(но лично я нарезаю на кубики и кидаю в блендер, так быстрее😇)\n\n'
                         '4.  Теперь наливаем масло в сковородкку и включаем плиту( я наливю оливковое, но можно и сливочное)\n\n'
                         '5.  Обжариваем курицу до бела\n\n'
                         '6.  В это время делаем соус, смешиваем молоко со специей, тщательно перемeшиваем\n\n'
                         '7.  Закидываем грибы к курице\n\n'
                         '8.  Как только грибы стали мягкими и дали сок, добавляем наш соус и включем средний огонь( главное помешивать со дном, тк пригорает!)\n\n'
                         '9.  Когда соус згустел, засекаем минуту и снимаем с огня\n'
                         '10.  Зиливем нашу курица с соусом в посуду, которую можно постаавить в духовку\n\n'
                         '11.  Посыпаем сыром(тут все индивидуельно\n\n'
                         '12.  Ставим в духовку на 20 минут\n\n'
                         '13.  После 20 минут достаем и можно есть\n\n'
                         '14.  Приятного аппетита!😇😇\n\n')
    await message.answer('Советы: \n\n'
                         '1. Не берите пармезан в качестве сыра\n'
                         '2. В качестве гарнира используйте макароны\n'
                         )
    await message.answer('Вам все понравилось?', reply_markup=response)
    
    
# Мелкая справка по bourguignon  
@dp.message(lambda message: message.text == "Беф-бургиньон")
async def support_command(message: Message):  
    await message.answer("Потрясающий выбор!")  
    await message.answer("Но я бы настоятельно порекомандовал бы, сначала узнать про вино для этого блюда")
    await message.answer('Желаешь?', reply_markup=bourguignon_vine)

# Продукты со справкой о вине
@dp.message(lambda message: message.text == "Хочу узнать про вино")
async def support_command(message: Message):  
    await message.answer("Я очень рад что тебе интересно!")  
    await message.answer("Держи!!!!❤️")
    await message.answer(BOURGUIGNON_VINE)  
    await message.answer("Теперь можем приступить")
    await message.answer("Для данного блюда, вам понадовится:(на 8 порций)")
    await message.answer(BOURGUIGNON)
    await message.answer('Приступить к рецепту?', reply_markup=yes_bour)   
    
# Продукты без справки о вине
@dp.message(lambda message: message.text == "Не стоит")
async def support_command(message: Message):
    await message.answer("И зря, это важно и интересно")
    await message.answer("Тогда держи рецепт")
    await message.answer(BOURGUIGNON)
    await message.answer('Приступить к рецепту?', reply_markup=yes_bour)
    
# Рецепт Boeuf bourguignon
@dp.message(lambda message: message.text == "Дa")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")    
    await message.answer(" Сначалаа мы все подготовим, а затем начнем делать")
    await message.answer('Перед готовкой, включите духовку на 180 - 200 градусов Цельсия( или 356 - 392 градусов Фарангейта)\n\n'
                        '1. Бекон нарезать кубиками, лук и морковь очистить и нарезать не очень мелко\n\n' 
                        '2. Мясо нарезать порционными кусочками, вымыть и как следует обсушить бумажным полотенцем (каждый кусочек)\n\n'
                        '3. В глубокой кастрюле (казанке) с тяжелым дном, которую можно затем поставить в духовку, разогреть оливковое масло и обжарить сначала бекон до золотистого цвета\n\n'
                        '4. Как только будет готов, достать его из кастрюли с помощью шумовки и отложить в сторону\n\n'
                        '5. В той же кастрюле на оставшемся от бекона жиру обжарить частями мясо на достаточно сильно огне. У меня обычно получается обжарить в два захода. Не выкладывайте сразу все мясо! Кусочки должны хорошо поджариться со всех сторон\n\n'
                        '6. Готовое мясо выложить в миску с беконом\n\n'
                        '7. И теперь в кастрюлю выкладываем подготовленные овощи, обжариваем несколько минут, время от времени помешивая\n\n'
                        '8. Затем добавляем к овощам мясо и бекон. Посолить, поперчить и присыпать мукой. Как следует перемешать и дать всему содержимому обжариться еще пару-тройку минут\n\n'
                        '9. Теперь залить всё нашим мясным бульоном\n\n'
                        '10. Влить красное вино \n\n'
                        '11. Добавить лавровый лист, томатный концентрат и выдавить чеснок. Как следует осторожно все перемешать\n\n'
                        '12. Накрываем крышкой, ставим в нашу духовку, ставим 190°C(374°F)'
                        '13. Теперь забываем о мясе на 2-2.5 часа'                       
                         )
    await message.answer('Советы: \n\n'
                         '1. Лично я убираю в духовку на 2 часа, при обычном режиме, а потом на полчаса при режиме конвекции, при 160°C(320°F)\n'
                         '2. В качестве гарнира можно использовать:\n'
                        '1. Булгур\n'
                        '2. Батат(запеченный)\n'
                        '3. Рис\n'
                         )
    await message.answer('Вам все понравилось?', reply_markup=response)
    
   
@dp.message(lambda message: message.text == "Нет")
async def support_command(message: Message):
    await message.answer("Как скажешь!", reply_markup=main_menu_but)    
        
'''ИТАЛИЯ'''

# Выбрал Италию
@dp.message(lambda message: message.text == "Италия")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer("Вина, пасты, луга и каналы....")
    await message.answer("Итак, выбери блюдо", reply_markup=italy)
    
# Пользователь берет Болоньезе   
@dp.message(lambda message: message.text == "Болоньезе")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(BOLOGNESE)
    await message.answer('Приступить к рецепту?', reply_markup=yes_bolon)
    
@dp.message(lambda message: message.text == "Готов")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")    
    await message.answer(" Сначалаа мы все подготовим, а затем начнем делать")  
    await message.answer('1. Нарежим лук(можно дольками, можно кубиками\n\n)'
                         '2. Обжарьте лук(до золотистого цвета)\n\n'
                         '3. Как лук будет готов, закиньте фарш\n\n'
                         '4. Посолите и поперчите фарш\n\n'
                         '5. Обжарьте фарш до коричневого цвета\n\n'
                         '6. Добавьте томатны кондецат(пасту)\n\n'
                         '7. Добавьте воду, чтоб вода была выше фарша(на 2-3 см)\n\n'
                         '8. Закройте крышкой, сделайте минимальный огонь\n\n'
                         '9. Сварите спагетти\n\n'
                         '10. Добавить в тарелку пасту, а сверху фарш\n\n'
                         '11. Посыпать сверху пармезан\n\n'
                         ) 
    await message.answer('Вам все понравилось?', reply_markup=response)    
    
# Рецепт Карбонары   
@dp.message(lambda message: message.text == "Карбонара")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(CARBONARA)
    await message.answer('Приступить к рецепту?', reply_markup=yes_carb)
 
@dp.message(lambda message: message.text == "Гoтов")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")
    await message.answer(" Сначалаа мы все подготовим, а затем начнем делать")
    await message.answer('1. Нарежьте бекон полоскам(дольками)\n\n'
                         '2. Натрите сыр( лучше  на мелкой части терки)\n\n'
                         '3. Подготовьте яйца, нам нужен желток\n\n'
                         '4. Включите сковороду(масло не добавлять!)\n\n'
                         '5. Как сковорода разогреется, закидываем туда бекон\n\n'
                         '6. Обжариваем бекон до золотистого цвета(но не до хруста!)\n\n'
                         '7. Как бекон обжарится, уменьшаем огонь\n\n'
                         '8. Вливаем сливки, и ждем пока они прогреются(главное не доводить до кипения)\n\n'
                         '9. Как прогрели сливки, аккуратно, не торопясь, вливаем желтки( Лучше делать по 1 желтку, 1 добавили и быстро мешаем, главное чтобы делтокк не схватился)\n\n'                         
                         '10. Добавляем сыр, порциями, что бы сыр был в соусе и не расплавился\n\n'
                         '11. Все готово!\n\n'
                         'Берем желемый гарнир, и можно есть\n\n'
                         )    
    
    await message.answer('Вам все понравилось?', reply_markup=response)        
'''РОССИЯ'''

# Рецепт Борща    
@dp.message(lambda message: message.text == "Борщ")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(BORSH)
    await message.answer('Приступить к рецепту?', reply_markup=yes_borsh)
    
@dp.message(lambda message: message.text == "Гoтoв")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")
    await message.answer(" Сначалаа мы все подготовим, а затем начнем делать")
    await message.answer('1. Говядину нарезать крупными кусками\n\n'
                         '2. Залить мясо в кастрюле холодной водой, довести до кипения, снять пену. Варить бульон примерно 1,5 часа на небольшом огне\n\n'
                         '3. В конце варки посолить\n\n'
                         '4. Свёклу очистить, нарезать соломкой\n\n'
                         '5. Морковь очистить, натереть на крупной терке\n\n'
                         '6. Лук очистить, мелко нарезать\n\n'
                         '7. Капусту нашинковать\n\n'
                         '8. Картофель очистить, нарезать кубиками\n\n'
                         '9. На сковороде разогреть растительное масло. Свёклу, морковь и лук выложить на сковороду и тушить на среднем огне (пассеровать), помешивая, 5-7 минут\n\n'                         
                         '10. В конце добавить уксус и томатную пасту. Перемешать. Готовить овощи ещё 3-4 минуты, помешивая\n\n'
                         '11. В кипящий бульон выложить картофель и капусту, варить 10 минут. (Молодую капусту добавлять за 5 минут до окончания приготовления борща.)\n\n'
                         '12. Затем добавить пассерованные овощи, лавровый лист и перец. Варить борщ с говядиной еще 5-7 минут\n\n'
                         '13.  Готовому борщу дать настояться 10-15 минут. Зелень нарезать\n\n'
                         'Все готово!'
                         )    
    await message.answer("Я б посоветовал есть его со сметаной!")
    await message.answer('Вам все понравилось?', reply_markup=response)  
    
'''ЯПОНИЯ''' 

@dp.message(lambda message: message.text == "Япония")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer("Итак, выбери блюдо", reply_markup=japan)
# Лапша удон с курицей
@dp.message(lambda message: message.text == "Лапша удон с курицей")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(UDON_NOODLES)
    await message.answer('Приступить к рецепту?', reply_markup=yes_udon)    
    
@dp.message(lambda message: message.text == "Конечно!")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")    
    await message.answer(
        '1. Разогреть сковородку вок и раскалить в ней растительное масло. На раскаленном масле обжарить нарезанный тонкой соломкой имбирь, нарезанную тонкими ломтиками курицу, нарезанные тонкими ломтиками грибы вешенки и мелко нарубленный чеснок. Итогом трудов должно стать такое состояние куриного мяса и грибов, при котором их уже можно было бы есть без дальнейших приключений. Грибы должны успеть пустить сок. Сок же должен успеть испариться под действием высоких температур, а вешенки обязаны приобрести приятную корич­не­вую корочку и заполонить всю кухню настырным ароматом свежеподжаренных грибов\n\n'
        '2. В этот момент надо добавить в сковородку соевый соус, звездочки бадьяна, мелко нарезанный сладкий перец и нарезанный тонкими кольцами перец чили, перемешать, потушить минуту и залить куриным бульоном. Варить суп пять минут\n\n'
        '3. За это время в любой подходящей кастрюльке отварить в подсоленной воде лапшу удон\n\n'
        '4. Снять с огня суп, выжать в него сок лимона, бросить стебли лука, лапшу удон, перемешать и подавать к столу\n\n'
    )  
    await message.answer('Вам все понравилось?', reply_markup=response)   
    
# Рамен      
@dp.message(lambda message: message.text == "Рамен")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(RAMEN)
    await message.answer('Приступить к рецепту?', reply_markup=yes_ramen)   
     
@dp.message(lambda message: message.text == "Кoнечно!")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")   
    await message.answer(   
        '1. Подготовить необходимые ингредиенты\n\n'
        '2. Грудинку обсушить от влаги и обжарить на растительном масле со всех сторон до золотистой корочки\n\n'
        '3. Затем в кастрюлю влить 250 мл воды, 80 мл соевого соуса, рисовое вино, добавить 2 столовые ложки сахара, довести до кипения и поместить туда мясо, крупно нарезанные зеленый лук и имбирь. Готовить на низком огне под крышкой в течение часа. Периодически поливать мясо соусом\n\n'
        '4. Разогреть бульон, добавить крупно нарезанный имбирь, зубчики чеснока и анис, поварить 30 минут\n\n'
        '5. Смешать половник горячего бульона с пастой мисо до однородной массы и перелить ее в кастрюлю с бульоном. Туда же добавить соевый соус\n\n'
        '6. Сварить яйца в умеренно кипящей воде в течение 7–8 минут. Лапшу сварить согласно инструкции на упаковке\n\n'        
        '7. Собрать суп прямо в тарелке: Положить лапшу, несколько ломтиков мяса\n\n'
        '8. Залить бульоном\n\n'
        '9. Добавить нарезанный кольцами лук, рубленую кинзу\n\n'       
        '10. Добавить половинки яйца, колечки чили и ростки сои.\n\n'                  
    )   
    await message.answer('Вам все понравилось?', reply_markup=response)      
# Курица терияки      
@dp.message(lambda message: message.text == "Курица терияки")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(TERIYAKI_CHIKEN)
    await message.answer('Приступить к рецепту?', reply_markup=yes_chick)  
     
@dp.message(lambda message: message.text == "Конечнo!")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")   
    await message.answer(
        '1. Подготовить необходимые ингредиенты\n\n'
        '2. На мелкой терке натереть имбирь и лук\n\n'
        '3. Чеснок раздавить чеснокодавкой\n\n'
        '4. Смешать соевый соус, сахар, саке, имбирь, чеснок и лук\n\n'
        '5. Нарезать филе крупными кусками и положить в маринад, оставить на 30 минут\n\n'
        '6. На сковороде разогреть растительное масло\n\n'        
        '7. Обжарить куски курицы со всех сторон до карамельной корочки. Отложить\n\n'
        '8. В ту же сковородку вылить маринад, уварить его в течение 3–4 минут\n\n'
        '9. Вернуть курицу в сковороду и готовить, помешивая, еще пару минут, мясо должно покрыться соусом, как глазурью\n\n'
        '10. Подавать, украсив семенами кунжута и зеленым луком\n\n'
    )              
    await message.answer('Вам все понравилось?', reply_markup=response) 
    
'''МЕКСИКА'''

# Выбрал Италию
@dp.message(lambda message: message.text == "Мексика")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer("Итак, выбери блюдо", reply_markup=mexico)


@dp.message(lambda message: message.text == "Чили кон карне")
async def support_command(message: Message):
    await message.answer("Шикарный выбор")
    await message.answer('Держите список продуктов:')
    await message.answer(KON_KARNE)
    await message.answer('Приступить к рецепту?', reply_markup=yes_konk)


@dp.message(lambda message: message.text == "Приступим")
async def support_command(message: Message):
    await message.answer("Отлично, приступим!")  
    await message.answer(
        '1. Филе говядины промойте под проточной холодной водой и обсушите. Говядину можно пропустить через мясорубку или мелко нарезать острым ножом. Я буду нарезать\n\n'
        '2. Лук,чеснок очистите от шкурки. Их мелко нарежьте вместе с сельдереем. Глубокую сковороду или кастрюлю с толстым дном поставьте на огонь, разогрейте. Налейте растительное масло и обжарьте до прозрачности подготовленные овощи\n\n'
        '3. Добавьте к обжаренным овощам нарезанную говядину или фарш. Обжаривайте мясо с овощами на среднем огне около 10 минут. Если используется фарш в приготовлении, то при обжаривании нужно стараться разбивать кусочки, чтобы не было комочков\n\n'
        '4. Перец помойте, уберите семена и плодоножку. Нарежьте перец произвольно и добавьте к мясу, добавьте молотую паприку и сухие специи. Обжаривайте всё вместе, помешивая, 5 - 7 минут. Если в приготовлении используется свежий острый перец, то на этом этапе его тоже следует добавить\n\n'
        '5. Добавьте измельчённые помидоры и перемешайте. Для более насыщенного вкуса можно добавить чайную ложку томатной пасты. Посолите и добавьте чёрный молотый перец\n\n'
        '6. Добавьте подготовленную фасоль, перемешайте. Залейте блюдо кипятком так, чтобы жидкость полностью прикрывала содержимое сковороды. Тушите на среднем огне под крышкой до готовности. Если фасоль сварена до готовности, то пока её не добавляйте, а тушите мясо без неё около часа. Затем добавьте фасоль и тушите уже всё вместе ещё минут 30. С консервированной фасолью тушите 10 минут\n\n'
        '7. Готовому чили кон карне дайте настояться в сковороде под крышкой 10- 15 минут и можно подавать к столу\n\n'                                           
    )
    await message.answer("Я б посоветовал есть его с отварным картофелем")
    await message.answer('Вам все понравилось?', reply_markup=response)  





'''ОЦЕНКА'''
# Положительная
@dp.message(lambda message: message.text == "Все было очень вкусно!")
async def support_command(message: Message):
    await message.answer("Мы очень рады! \n\nТак же попробуйте другие блюда, они тоже очень вкусные!😁😁\n\nВы вернулись в основное меню...", reply_markup=main_menu_but)    
    
    
# Отрицательная
@dp.message(lambda message: message.text == "Не особо понравилось")
async def support_command(message: Message):
    await message.answer("Очень жаль🥺🥺\n\nно вы можете попробать другие блюда, до скорогоn\n\nВы вернулись в основное меню...", reply_markup=main_menu_but)        
    
    
    
'''Возврат в меню'''   
# В случае отказа от рецепта
@dp.message(lambda message: message.text == "Нет")
async def support_command(message: Message):
    await message.answer("Очень жаль🥺🥺\n\n до скорого!", reply_markup=main_menu_but)
    
# Кнопка назад
@dp.message(lambda message: message.text == "Назад")
async def support_command(message: Message):
    await message.answer("Вы вернулись в основное меню...", reply_markup=main_menu_but)   
    
    
    
    
    
async def main():
    await dp.start_polling(bot)
    

    
if __name__ == '__main__':
    asyncio.run(main())
