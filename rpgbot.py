import asyncio
import json
import logging
import random
import threading
import datetime
import os
from background import keep_alive #импорт функции для поддержки работоспособности
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InputFile
from config import TOKEN
from time import time as now

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)




res_dt = datetime.datetime.now()

ADMIN_ID = 2023527964

cooldown = 1800
cdboss = 86400


pointer = lambda username: {
    "username": username,
    "money": 10000,
    "level": 1,
    "power": 5,
    "hp": 10,
    "pet": "Нет",
    "armor": "Броня из кожи",
    "dateofreg": res_dt.strftime("%d-%m-%Y %H:%M"),
    "apteka": 0,
    "wolf": 0,
    "enot": 0,
    "drone": 0,
    "randlist": 0,
    "plusmoney": 0,
    "pluslevel": 0,
    "bonus": 0,
    "id": user_id
}

pointerboss = lambda username: {
    "username": username,
    "hples": 5,
    "hpskelet": 10,
    "hpbarya": 20,
    "hpmag": 50,
    "hpjin": 80,
    "hpzombie": 140,
    "hpspider": 200,
    "hpfortuna": 1
}

@dp.message_handler(commands=['start']) # Старт и внесение пользователя в базу данных
async def start(message: types.Message):
    with open("C:/IT/RPGbot/database.json", "r") as f_o:
        data_from_json = json.loads(f_o.read())

    global user_id
    user_id = message.from_user.id
    firstname = message.from_user.username

        
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = pointer(firstname)
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
            

    with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
        databoss_from_json = json.loads(f_o.read())

    user_id = message.from_user.id
    firstname = message.from_user.username

    if str(user_id) not in databoss_from_json:
        databoss_from_json[user_id] = pointerboss(firstname)
        with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
            json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        bcmds = KeyboardButton("🛠️ Команды")
        markup.add(bcmds)
        await bot.send_message(message.from_user.id, "🗃️ Вы зарегестрированы\n🌟 Для продолжения и ознакомления с командами нажмите кнопку!", reply_markup=markup)



@dp.message_handler(lambda msg: msg.text.startswith('Оружие'))
async def weapon(message):
    pass

@dp.message_handler(lambda msg: msg.text.startswith('Поход'))
async def hike(message):
    pass

@dp.message_handler(lambda msg: msg.text.startswith('Локация'))
async def location(message):
    pass

@dp.message_handler(lambda msg: msg.text.startswith('🦇 Мегабосс'))
async def megaboss(message):
    with open("C:/IT/RPGbot/megaboss.json", "r") as f_o:
        megaboss = json.loads(f_o.read())
        mghp = megaboss["megabosshp"]
    if megaboss["megabosshp"] >= 0:
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🦇 Нанести урон Мегабоссу', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/megaboss.png'), caption=f"\
    Босс: 🦇 Мегабосс\n\
    Здоровье: {mghp} ❤️\n\
    \n\
    Награда за победу:\n\
    1. Монеты\n\
    ", reply_markup=markup)
    else:
        await message.answer("⏳ Босс еще не восстановился!")

@dp.message_handler(lambda msg: msg.text.startswith('🦇 Нанести урон Мегабоссу'))
async def damagemegaboss(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/megaboss.json", "r") as f_o:
            megaboss = json.loads(f_o.read())
        
        user_id = message.from_user.id
        if now() > megaboss["megabosstimer"] + cdboss:
            if megaboss["megabosshp"] >= 0:
                power = data_from_json[f"{user_id}"]["power"]
                megaboss["megabosshp"] -= power
                hpmb = megaboss["megabosshp"]
                await message.answer(f"🤕 Вы нанесли мегабоссу урон, здоровье босса: {hpmb}")
                if megaboss["megabosshp"] <= 0:
                    if now() > megaboss['megabosstimer'] + cdboss:
                        megaboss["megabosstimer"] = now()
                        randmon = random.randint(120000, 250000)
                        data_from_json[f"{user_id}"]["money"] += randmon
                        await message.answer(f"⚰️ Мегабосс повержен! Вы получили: {randmon}")
                    else:
                        seconds = megaboss["megabosstimer"]
                        result = (time.ctime(seconds))
                        timer = result[11:][:8]
                        await message.answer(f"⏳ Последний раз босс был убит в {timer}! Если вам не выдали награду за босса, то напишите в лс @solarezzov с доказательствами нанесения урона боссу.")
            else:
                await bot.send_message(message.from_user.id, "⚰️ Мегабосс уже повержен, если вам не выдали награду за босса, то напишите в лс @solarezzov с доказательствами нанесения урона боссу.")
        else:
            seconds = megaboss["megabosstimer"]
            result = (time.ctime(seconds))
            timer = result[11:][:8]
            await message.answer(f"⏳ Последний раз босс был убит в {timer}! Если вам не выдали награду за босса, то напишите в лс @solarezzov с доказательствами нанесения урона боссу.")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
        with open("C:/IT/RPGbot/megaboss.json", "w") as f_o:
            json.dump(megaboss, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('Админ панель'))
async def admpanel(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer("Админ панель:\nдатьденег - выдать монеты\nдатьрейтинг - дать рейтинг")

@dp.message_handler(lambda msg: msg.text.startswith('датьрейтинг'))
async def givemoney(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            
            message_options = message.text.split()[1:]
            data_from_json[f"{message_options[0]}"]["level"] += int(message_options[1])
            await bot.send_message(message.from_user.id, "💰 Вы выдали игроку рейтинг!")
            await bot.send_message(message_options[0], f"💰 Админ выдал вам {message_options[1]} рейтинг(а)!")
            
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

@dp.message_handler(lambda msg: msg.text.startswith('датьденег'))
async def givemoney(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            
            message_options = message.text.split()[1:]
            data_from_json[f"{message_options[0]}"]["money"] += int(message_options[1])
            await bot.send_message(message.from_user.id, "💰 Вы выдали игроку монеты!")
            await bot.send_message(message_options[0], f"💰 Админ выдал вам {message_options[1]} монет!")

        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

@dp.message_handler(lambda msg: msg.text.startswith('Продать рейтинг'))
async def selllevel(message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())

            message_options = message.text.split()[1:]
            if data_from_json[f"{user_id}"]["level"] >= int(message_options[1]):
                data_from_json[f"{user_id}"]["level"] -= int(message_options[1])
                data_from_json[f"{user_id}"]["money"] += int(message_options[1])*100
                await bot.send_message(message.from_user.id, "💰 Вы продали рейтинг!")
            else:
                await bot.send_message(message.from_user.id, "❌ У вас нет столько рейтинга!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except IndexError:
        await bot.send_message(message.from_user.id, "❌ Вы не указали кол-во уровня хотите продать! Напишите Продать рейтинг [сколько] БЕЗ СКОБОК!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('Чек'))
async def check(message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())

            message_options = message.text.split()[1:]
            usname = data_from_json[f"{message_options[0]}"]["username"]
            mon = data_from_json[f"{message_options[0]}"]["money"]
            lvl = data_from_json[f"{message_options[0]}"]["level"]
            arm = data_from_json[f"{message_options[0]}"]["armor"]
            pet = data_from_json[f"{message_options[0]}"]["pet"] # Переменная не использовалась, но была объявлена что заняло память и скорость
            power = data_from_json[f"{message_options[0]}"]["power"]
            health = data_from_json[f"{message_options[0]}"]["hp"]
            dateofregistr = data_from_json[f"{message_options[0]}"]["dateofreg"]
            await message.answer(f"\
Профиль {usname}:\n\
    ⚡ Никнейм: {usname}\n\
    💳 ID: {user_id}\n\
    💰 Монет: {mon}\n\
    ✨ Рейтинг: {round(lvl, 2)}\n\
    🛡️ Броня: {arm}\n\
    ⚔️ Сила: {power}\n\
    💊 Здоровье: {health}\n\
    🐾 Питомец: {pet}\n\
    📅 Дата регистрации: {dateofregistr}\
            ")
    except IndexError:
        await bot.send_message(message.from_user.id, "❌ Вы указали не верный ID пользователя! Напишите ""Чек [ID]"" БЕЗ СКОБОК!")

@dp.message_handler(lambda msg: msg.text.startswith('Передать'))
async def pay(message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())

            message_options = message.text.split()[1:]
            if data_from_json[f"{user_id}"]["money"] >= int(message_options[1]):
                data_from_json[f"{user_id}"]["money"] -= int(message_options[1])
                data_from_json[f"{message_options[0]}"]["money"] += int(message_options[1])
                await bot.send_message(message.from_user.id, "💰 Вы передали игроку монеты!")
                await bot.send_message(message_options[0], f"💰 Вам передали деньги в размере {message_options[1]} монет!")
            else:
                await bot.send_message(message.from_user.id, "❌ У вас нет столько монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError or IndexError:
        await bot.send_message(message.from_user.id, "❌ Вы указали не верный ID пользователя! Напишите ""Передать [ID] [сумма]"" БЕЗ СКОБОК!")


@dp.message_handler(lambda msg: msg.text.startswith('🎁 Бонус'))
async def present(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
        user_id = message.from_user.id 
        if now() > data_from_json[f'{user_id}']['bonus'] + cooldown:
            data_from_json[f'{user_id}']['bonus'] = now()
            data_from_json[f"{user_id}"]["money"] += 500
            await bot.send_message(message.from_user.id, "Вы получили бонус в размере 500 монет!")
        
        else:
            await bot.send_message(message.from_user.id, "Вы уже получали бонус за эти 30 минут.")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🛠️ Команды'))
async def cmds(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["📋 Профиль", "🎁 Бонус","🛒 Магазин", "🏹 Боссы", "🏆 Топ", "📢 Информация о боте"]])
    await bot.send_message(message.from_user.id, "🛠️ Команды:\n📋 Профиль\n🎁 Бонус\n🛒 Магазин\n💰 Передать\n💰 Продать рейтинг\n🏹 Боссы\n🏆 Топ\n📢 Информация о боте", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('📋 Профиль'))
async def profile(message: types.Message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
            firstname = message.from_user.first_name
            mon = data_from_json[f"{user_id}"]["money"]
            lvl = data_from_json[f"{user_id}"]["level"]
            arm = data_from_json[f"{user_id}"]["armor"]
            pet = data_from_json[f"{user_id}"]["pet"] # Переменная не использовалась, но была объявлена что заняло память и скорость
            power = data_from_json[f"{user_id}"]["power"]
            health = data_from_json[f"{user_id}"]["hp"]
            dateofregistr = data_from_json[f"{user_id}"]["dateofreg"]
        await bot.send_message(message.from_user.id, f"📋 Ваш профиль:\n\
    ⚡ Никнейм: {firstname}\n\
    💳 ID: {user_id}\n\
    💰 Монет: {mon}\n\
    ✨ Рейтинг: {round(lvl, 2)}\n\
    🛡️ Броня: {arm}\n\
    ⚔️ Сила: {power}\n\
    💊 Здоровье: {health}\n\
    🐾 Питомец: {pet}\n\
    📅 Дата регистрации: {dateofregistr}\
    ")
    except KeyError:
        await bot.send_message(message.from_user.id, "Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🛒 Магазин'))
async def shop(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["🩹 Аптечка", "🔮 Улучшения", "🛡️ Броня", "🐾 Питомцы", "🔙 Назад"]])
    await bot.send_message(message.from_user.id, "🛒 Выберите что хотите купить:\n  🩹 Аптечка - 1 hp = 10 монет", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('🩹 Аптечка'))
async def apteka(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "🩹 Введите количество здоровья, которое хотите восстановить:")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

    

@dp.message_handler(lambda msg: msg.text.startswith('🔮 Улучшения'))
async def upgrades(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["⚔️ Увеличить силу", "🔙 Назад"]])
    await bot.send_message(message.from_user.id, "🔮 Выберите улучшение:", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('🛡️ Броня'))
async def armores(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["🧥 Железная броня", "🧥 Медная броня", "🧥 Кольчужная броня", "🧥 Черепашья броня", "🧥 Алмазная броня", "🧥 Незеритовая броня", "🔙 Назад"]])
    await bot.send_message(message.from_user.id, "🛡️ Выберите тип брони:\n   🧥 Железная броня - 500 монет\n   🧥 Медная броня - 1.500 монет\n   🧥 Кольчужная броня - 4.000 монет\n   🧥 Черепашья броня - 6.500 монет\n   🧥 Алмазная броня - 10.000 монет\n   🧥 Незеритовая броня - 20.000 монет", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('🧥 Незеритовая броня'))
async def ironarmor(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
        if data_from_json[f"{user_id}"]["money"] >= 20000:
            data_from_json[f"{user_id}"]["money"] -= 20000
            data_from_json[f"{user_id}"]["armor"] = "Незеритовая броня"
            await bot.send_message(message.from_user.id, "🧥 Вы успешно купили Незеритовую броню")
        else: 
            await bot.send_message(message.from_user.id, "❌ У вас не достаточно монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧥 Алмазная броня'))
async def ironarmor(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
        if data_from_json[f"{user_id}"]["money"] >= 10000:
            data_from_json[f"{user_id}"]["money"] -= 10000
            data_from_json[f"{user_id}"]["armor"] = "Алмазная броня"
            await bot.send_message(message.from_user.id, "🧥 Вы успешно купили Алмазную броню")
        else: 
            await bot.send_message(message.from_user.id, "❌ У вас не достаточно монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧥 Черепашья броня'))
async def ironarmor(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
        if data_from_json[f"{user_id}"]["money"] >= 6500:
            data_from_json[f"{user_id}"]["money"] -= 6500
            data_from_json[f"{user_id}"]["armor"] = "Черепашья броня"
            await bot.send_message(message.from_user.id, "🧥 Вы успешно купили Черепашью броню")
        else: 
            await bot.send_message(message.from_user.id, "❌ У вас не достаточно монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧥 Кольчужная броня'))
async def ironarmor(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
        if data_from_json[f"{user_id}"]["money"] >= 4000:
            data_from_json[f"{user_id}"]["money"] -= 4000
            data_from_json[f"{user_id}"]["armor"] = "Кольчужная броня"
            await bot.send_message(message.from_user.id, "🧥 Вы успешно купили Кольчужную броню!")
        else: 
            await bot.send_message(message.from_user.id, "❌ У вас не достаточно монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧥 Медная броня'))
async def ironarmor(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
        if data_from_json[f"{user_id}"]["money"] >= 1500:
            data_from_json[f"{user_id}"]["money"] -= 1500
            data_from_json[f"{user_id}"]["armor"] = "Медная броня"
            await bot.send_message(message.from_user.id, "🧥 Вы успешно купили Медную броню!")
        else: 
            await bot.send_message(message.from_user.id, "❌ У вас не достаточно монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧥 Железная броня'))
async def ironarmor(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
        if data_from_json[f"{user_id}"]["money"] >= 500:
            data_from_json[f"{user_id}"]["money"] -= 500
            data_from_json[f"{user_id}"]["armor"] = "Железная броня"
            await bot.send_message(message.from_user.id, "🧥 Вы успешно купили Железную броню!")
        else: 
            await bot.send_message(message.from_user.id, "❌ У вас не достаточно монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🔙 Назад к боссам'))
async def bosses(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["🌲 Лесник", "💀 Скелетон", "🐻 Баря", "🧙🏼 Маг", "🧞‍♂️ Джин", "🧟‍♂️ Зомби", "🕷️ Паук", "🎰 Фортуна", "🦇 Мегабосс", "🔙 Назад", "📢 Информация о боте", '🏹 Восстановить здоровье боссов']])
    await bot.send_message(message.from_user.id, "🏹 Боссы:\n   🌲 Лесник\n   💀 Скелетон\n   🐻 Баря\n   🧙🏼 Маг\n   🧞‍♂️ Джин\n   🧟‍♂️ Зомби\n   🕷️ Паук\n   🎰 Фортуна\n   🦇 Мегабосс\n\n🔔 Всю информацию по боссам можно найти в пункте - \n\"📢 Информация о боте\"", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('🏹 Боссы'))
async def bosses(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["🌲 Лесник", "💀 Скелетон", "🐻 Баря", "🧙🏼 Маг", "🧞‍♂️ Джин", "🧟‍♂️ Зомби", "🕷️ Паук", "🎰 Фортуна", "🦇 Мегабосс", "🔙 Назад", "📢 Информация о боте", '🏹 Восстановить здоровье боссов']])
    await bot.send_message(message.from_user.id, "🏹 Боссы:\n   🌲 Лесник\n   💀 Скелетон\n   🐻 Баря\n   🧙🏼 Маг\n   🧞‍♂️ Джин\n   🧟‍♂️ Зомби\n   🕷️ Паук\n   🎰 Фортуна\n   🦇 Мегабосс\n\n🔔 Всю информацию по боссам можно найти в пункте - \n\"📢 Информация о боте\"", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('🎰 Фортуна'))
async def bosslesf(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🎰 Нанести урон Фортуне', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpf = databoss_from_json[f"{user_id}"]["hpfortuna"]
        if databoss_from_json[f"{user_id}"]["hpfortuna"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/fortuna.png'), caption=f"\
    Босс: 🎰 Фортуна\n\
    Здоровье: {hpf} ❤️\n\
    Сила: ∞\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    Этот босс создан для попытать удачу. При попытке его убить, он или убьет вас или оставит вам 1 здоровье, еще вы можете ему снести только 1 поинт здоровья(что я вляется его хп).\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🎰 Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🎰 Нанести урон Фортуне'))
async def damagefortuna(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpfortuna"] > 0:
                    randomminushp = [-1, 1]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] = randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    power = random.randint(1,100)
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы не смогли убить босса. Ваше здоровье: {myhp}")
                    if power == 34:
                        databoss_from_json[f"{user_id}"]["hpfortuna"] -= power
                        hpboss = databoss_from_json[f"{user_id}"]["hpfortuna"]
                        await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                        if databoss_from_json[f"{user_id}"]["hpfortuna"] <= 0:
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(10, 100)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(10000, 100000)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                        else:
                            await bot.send_message(message.from_user.id, f"💥 Вы ничего не нанесли боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                elif(databoss_from_json[f"{user_id}"]["hpfortuna"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🕷️ Паук'))
async def bosslesp(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🕷️ Нанести урон Пауку', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpsp = databoss_from_json[f"{user_id}"]["hpspider"]
        if databoss_from_json[f"{user_id}"]["hpspider"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/spider.png'), caption=f"\
    Босс: 🕷️ Паук\n\
    Здоровье: {hpsp} ❤️\n\
    Сила: 80, крит 100\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🕷️ Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🕷️ Нанести урон Пауку'))
async def damagespider(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpspider"] > 0:
                    randomminushp = [80, 100, 0, 80, 80, 80, 80, 80, 80, 80, 80, 80, 0, 0, 0]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hpspider"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hpspider"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hpspider"] <= 0:

                        
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(8, 9)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(1300, 1600)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hpspider"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧟‍♂️ Зомби'))
async def bosslesz(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🧟‍♂️ Нанести урон Зомби', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpz = databoss_from_json[f"{user_id}"]["hpzombie"]
        if databoss_from_json[f"{user_id}"]["hpzombie"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/zombie.png'), caption=f"\
    Босс: 🧟‍♂️ Зомби\n\
    Здоровье: {hpz} ❤️\n\
    Сила: 40, крит 60\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🧟‍♂️ Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")            

@dp.message_handler(lambda msg: msg.text.startswith('🧟‍♂️ Нанести урон Зомби'))
async def damagezombie(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpzombie"] > 0:
                    randomminushp = [40, 60, 40, 0, 40, 40, 40, 40, 40, 40, 40, 0, 0, 0]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hpzombie"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hpzombie"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hpzombie"] <= 0:

                        
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(7, 8)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(1000, 1500)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hpzombie"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧞‍♂️ Джин'))
async def bosslesj(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🧞‍♂️ Нанести урон Джину', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpj = databoss_from_json[f"{user_id}"]["hpjin"]
        if databoss_from_json[f"{user_id}"]["hpjin"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/jin.png'), caption=f"\
    Босс: 🧞‍♂️ Джин\n\
    Здоровье: {hpj} ❤️\n\
    Сила: 25, крит 35\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🧞‍♂️ Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧞‍♂️ Нанести урон Джину'))
async def damagejin(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpjin"] > 0:
                    randomminushp = [25, 25, 35, 25, 25, 25, 25, 25, 25, 25, 25, 35, 0, 0, 0]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hpjin"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hpjin"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hpjin"] <= 0:

                        
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(5, 7)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(700, 900)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hpjin"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")


@dp.message_handler(lambda msg: msg.text.startswith('🌲 Лесник'))
async def bossles(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🌲 Нанести урон Леснику', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpl = databoss_from_json[f"{user_id}"]["hples"]
        if databoss_from_json[f"{user_id}"]["hples"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/lesnik.png'), caption=f"\
    Босс: 🌲 Лесник\n\
    Здоровье: {hpl} ❤️\n\
    Сила: 1-5, крит 9\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🌲 Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🐻 Баря'))
async def bossbarya(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🐻 Нанести урон Баре', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpb = databoss_from_json[f"{user_id}"]["hpbarya"]
        if databoss_from_json[f"{user_id}"]["hpbarya"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/barya.png'), caption=f"\
    Босс: 🐻 Баря\n\
    Здоровье: {hpb} ❤️\n\
    Сила: 10-13, крит 17\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🐻 Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🐻 Нанести урон Баре'))
async def damagebarya(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpbarya"] > 0:
                    randomminushp = [10, 12, 13, 11, 17, 10, 12, 13, 13, 12, 13, 11, 10, 10, 0, 0, 0]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hpbarya"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hpbarya"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hpbarya"] <= 0:

                        
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(2, 3)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(250, 350)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hpbarya"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🌲 Нанести урон Леснику'))
async def damageforest(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hples"] > 0:
                    randomminushp = [1, 2, 3, 4, 5, 9, 1, 2, 3, 4, 5, 0, 0]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hples"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hples"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hples"] <= 0:

                        
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(1, 2)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(30, 150)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hples"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧙🏼 Маг'))
async def bosslesm(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['🧙🏼 Нанести урон Магу', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpm = databoss_from_json[f"{user_id}"]["hpmag"]
        if databoss_from_json[f"{user_id}"]["hpmag"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/mag.png'), caption=f"\
    Босс: 🧙🏼 Маг\n\
    Здоровье: {hpm} ❤️\n\
    Сила: 15, крит 20\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "🧙🏼 Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🧙🏼 Нанести урон Магу'))
async def damagemag(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpmag"] > 0:
                    randomminushp = [15, 15, 15, 15, 15, 20, 15, 15, 15]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hpmag"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hpmag"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hpmag"] <= 0:

                        
                            randomboss = ["Рейтинг", "Монеты"]
                            randomlist = random.choice(randomboss)
                            data_from_json[f"{user_id}"]["randlist"] = randomlist
                            rlist = data_from_json[f"{user_id}"]["randlist"]
                            await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {rlist}. Ваше здоровье: {hp}")
                            if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                    randomlevel = random.randint(3, 4)
                                    data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                    data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                    

                                    await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                            if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                                with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                    data_from_json = json.loads(f_o.read())

                                    randommonet = random.randint(400, 500)
                                    data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                    data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                    

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hpmag"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")


@dp.message_handler(lambda msg: msg.text.startswith('💀 Скелетон'))
async def bossless(message: types.Message):
    try:
        user_id = message.from_user.id
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(text) for text in ['💀 Нанести урон Скелетону', '🔙 Назад к боссам', '🏹 Восстановить здоровье боссов']])
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        hpske = databoss_from_json[f"{user_id}"]["hpskelet"]
        if databoss_from_json[f"{user_id}"]["hpskelet"] > 0:
            await bot.send_photo(message.chat.id, photo=InputFile('C:/IT/RPGbot/photobosses/skeleton.png'), caption=f"\
    Босс: 💀 Скелетон\n\
    Здоровье: {hpske} ❤️\n\
    Сила: 7-9, крит 15\n\
    \n\
    Награда за победу:\n\
    1. Рейтинг\n\
    2. Монеты\n\
    \n\n\
    ", reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "💀 Босс повержен!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('💀 Нанести урон Скелетону'))
async def damageskeleton(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
            databoss_from_json = json.loads(f_o.read())
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            if data_from_json[f"{user_id}"]["hp"] > 0 :
                if databoss_from_json[f"{user_id}"]["hpskelet"] > 0:
                    randomminushp = [7, 9, 15, 7, 9 ,7 ,9 ,7, 9, 0, 0]
                    randminhp = random.choice(randomminushp)
                    data_from_json[f"{user_id}"]["hp"] -= randminhp
                    hp = data_from_json[f"{user_id}"]["hp"]
                    databoss_from_json[f"{user_id}"]["hpskelet"] -= data_from_json[f"{user_id}"]["power"]
                    hpboss = databoss_from_json[f"{user_id}"]["hpskelet"]
                    myhp = data_from_json[f"{user_id}"]["hp"]
                    await bot.send_message(message.from_user.id, f"💥 Вы нанесли урон боссу. Здоровье босса: {hpboss}. Ваше здоровье: {myhp}")
                    if databoss_from_json[f"{user_id}"]["hpskelet"] <= 0:
                        with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                data_from_json = json.loads(f_o.read())

                        
                        randomboss = ["Рейтинг", "Монеты"]
                        randomlist = random.choice(randomboss)
                        data_from_json[f"{user_id}"]["randlist"] = randomlist
                        await bot.send_message(message.from_user.id, f"☠️ Вы убили босса! Вы получили - {randomlist}. Ваше здоровье: {hp}")
                        if data_from_json[f"{user_id}"]["randlist"] == "Рейтинг":
                                randomlevel = random.randint(1, 2)
                                data_from_json[f"{user_id}"]["pluslevel"] = randomlevel
                                data_from_json[f"{user_id}"]["level"] += data_from_json[f"{user_id}"]["pluslevel"]
                                

                                await bot.send_message(message.from_user.id, f"✨ Вы получили + {round(randomlevel, 2)} Рейтинг")
                        if data_from_json[f"{user_id}"]["randlist"] == "Монеты":
                            with open("C:/IT/RPGbot/database.json", "r") as f_o:
                                data_from_json = json.loads(f_o.read())

                                randommonet = random.randint(150, 250)
                                data_from_json[f"{user_id}"]["plusmoney"] = randommonet
                                data_from_json[f"{user_id}"]["money"] += data_from_json[f"{user_id}"]["plusmoney"]
                                

                            
                                await bot.send_message(message.from_user.id, f"💰 Вы получили + {randommonet} монет")
                elif(databoss_from_json[f"{user_id}"]["hpskelet"]) <= 0:
                    await bot.send_message(message.from_user.id, "🏹 Босс еще не отрегенерировался.")
                with open("C:/IT/RPGbot/database.json", "w") as f_o:
                    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
                with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                    json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            elif data_from_json[f"{user_id}"]["hp"]<= 0:
                await bot.send_message(message.from_user.id, "⚠️ У вас нет здоровья. Восстановите его.")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🏹 Восстановить здоровье боссов'))
async def regenboss(message: types.Message):
    chars = list('+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    random.shuffle(chars)
    global captcha
    captcha = ''.join([random.choice(chars) for x in range(6)])
    await bot.send_message(message.from_user.id, f"Введите капчу: {captcha}\nЧто бы ввести капчу напишите \"Капча \"капча которая сгенерировалась\"\"")

@dp.message_handler(lambda msg: msg.text.startswith('Капча'))
async def captc(message: types.Message):
    try:
        user_id = message.from_user.id
        if message.text[6:] == captcha:
            with open("C:/IT/RPGbot/databaseboss.json", "r") as f_o:
                databoss_from_json = json.loads(f_o.read())
            with open("C:/IT/RPGbot/megaboss.json", "r") as f_o:
                megaboss = json.loads(f_o.read())
                if megaboss["megabosshp"] <= 0:
                    megaboss["megabosshp"] = 100000
                    databoss_from_json[f"{user_id}"]["hples"] = 5
                    databoss_from_json[f"{user_id}"]["hpskelet"] = 10
                    databoss_from_json[f"{user_id}"]["hpbarya"] = 20
                    databoss_from_json[f"{user_id}"]["hpmag"] = 50
                    databoss_from_json[f"{user_id}"]["hpjin"] = 80
                    databoss_from_json[f"{user_id}"]["hpzombie"] = 140
                    databoss_from_json[f"{user_id}"]["hpspider"] = 200
                    databoss_from_json[f"{user_id}"]["hpfortuna"] = 1
                else:
                    databoss_from_json[f"{user_id}"]["hples"] = 5
                    databoss_from_json[f"{user_id}"]["hpskelet"] = 10
                    databoss_from_json[f"{user_id}"]["hpbarya"] = 20
                    databoss_from_json[f"{user_id}"]["hpmag"] = 50
                    databoss_from_json[f"{user_id}"]["hpjin"] = 80
                    databoss_from_json[f"{user_id}"]["hpzombie"] = 140
                    databoss_from_json[f"{user_id}"]["hpspider"] = 200
                    databoss_from_json[f"{user_id}"]["hpfortuna"] = 1
            
            with open("C:/IT/RPGbot/databaseboss.json", "w") as f_o:
                json.dump(databoss_from_json, f_o, indent=4, ensure_ascii=False)
            with open("C:/IT/RPGbot/megaboss.json", "w") as f_o:
                json.dump(megaboss, f_o, indent=4, ensure_ascii=False)
            await bot.send_message(message.from_user.id, "🏹 Все боссы отрегенерированы!")
        elif message.text[6:] != captcha:
            await bot.send_message(message.from_user.id, "❌ Вы не верно ввели капчу!")
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🔙 Назад'))
async def back(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["📋 Профиль", "🎁 Бонус","🛒 Магазин","🏹 Боссы", "🏆 Топ", "📢 Информация о боте"]])
    await bot.send_message(message.from_user.id, "🛠️ Команды:\n📋 Профиль\n🎁 Бонус\n🛒 Магазин\n💰 Передать\n💰 Продать рейтинг\n🏹 Боссы\n🏆 Топ\n📢 Информация о боте", reply_markup=markup)    

@dp.message_handler(lambda msg: msg.text.startswith('🐾 Питомцы'))
async def buypets(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["🐺 Волк", "🦝 Енот", "🤖 Дрон", "🔙 Назад"]])
    await bot.send_message(message.from_user.id, "🐾 Выберите питомца:\n    🐺 Волк - 1.000.000:\n        Добавляет +30 к силе\n    🦝 Енот - 10.000.000:\n        Добавляет +50 к силе\n    🤖 Дрон - 50.000.000:\n        Добавляет к +70 к силе", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('📢 Информация о боте'))
async def infobot(message: types.Message):
    await bot.send_message(message.from_user.id, "📢 Привествую, данный бот, это как мини RPG игра, где тебе нужно убивать боссов.\nУ каждого босса есть хп, например возьмем самого первого босса:\n\n\
Босс: 🌲 Лесник\n\
Здоровье: 5 ❤️\n\
Сила: 1-5, крит 9\n\
\n\
Награда за победу:\n\
1. Рейтинг\n\
2. Монеты\n\
")


@dp.message_handler(lambda msg: msg.text.startswith('⚔️ Увеличить силу'))
async def upgradepower(message: types.Message):
    try:
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
        if data_from_json[f"{user_id}"]["money"] > 500:
            await bot.send_message(message.from_user.id, "⚔️ Вы увеличили вашу силу на 1")

            data_from_json[f"{user_id}"]["power"] += 1
            data_from_json[f"{user_id}"]["money"] -= 500
        else:
            await bot.send_message(message.from_user.id, "❌ У вас нет 500 монет!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🏆 Топ'))
async def top(message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
        test_list = list(data_from_json.items())
        test_list.sort(reverse=True, key=lambda x: x[1]['money'])
        string = "🏆 Топ по количеству монет:\n"
        for num, item in enumerate(test_list[:5], 1):
            string += f'{num}. {item[1]["username"]}[<code>{item[1]["id"]}</code>] - {item[1]["money"]} монет\n'
        await bot.send_message(message.from_user.id, text=string, parse_mode="HTML")
        await bot.send_message(message.from_user.id, 'Что бы посмотреть профиль другого пользователя напишите "Чек [ID]" БЕЗ скобок и кавычек!')
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('✔️ Да'))
async def aptekada(message: types.Message):
    try:
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        back = KeyboardButton("🔙 Назад")
        markup.add(back)
        user_id = message.from_user.id
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())

            apt = data_from_json[f"{user_id}"]["apteka"]

            if data_from_json[f"{user_id}"]["money"] >= apt*10:
                data_from_json[f"{user_id}"]["hp"] += data_from_json[f"{user_id}"]["apteka"]
                data_from_json[f"{user_id}"]["money"] -= 10*data_from_json[f"{user_id}"]["apteka"]
                hp = data_from_json[f"{user_id}"]["apteka"]
                await bot.send_message(message.from_user.id, f"🩹 Ваше здоровье пополнено на {hp}!", reply_markup=markup)
            else:
                await bot.send_message(message.from_user.id, "❌ У вас нету столько денег!", reply_markup=markup)
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('❌ Нет'))
async def aptekano(message: types.Message):
    ReplyKeyboardRemove()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(text) for text in ["📋 Профиль", "🎁 Бонус","🛒 Магазин","🏹 Боссы", "🏆 Топ", "📢 Информация о боте"]])
    await bot.send_message(message.from_user.id, "🛠️ Команды:\n📋 Профиль\n🎁 Бонус\n🛒 Магазин\n💰 Передать\n💰 Продать рейтинг\n🏹 Боссы\n🏆 Топ\n📢 Информация о боте", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text.startswith('🐺 Волк'))
async def wolf(message: types.Message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
            if data_from_json[f"{user_id}"]["wolf"] == 0:
                if data_from_json[f"{user_id}"]["money"] > 1000000:

                    data_from_json[f"{user_id}"]["wolf"] = 1
                    data_from_json[f"{user_id}"]["money"] -= 1000000
                    data_from_json[f"{user_id}"]["pet"] = "🐺 Волк"
                    data_from_json[f"{user_id}"]["power"] += 30
                    await bot.send_message(message.from_user.id, "🐺 Вы купили волка!")
                else:
                    await bot.send_message(message.from_user.id, "❌ У вас нет столько денег!")
            else: 
                await bot.send_message(message.from_user.id, "🐺 У вас уже есть волк!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")

@dp.message_handler(lambda msg: msg.text.startswith('🤖 Дрон'))
async def drone(message: types.Message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
            if data_from_json[f"{user_id}"]["enot"] == 0:
                if data_from_json[f"{user_id}"]["money"] > 50000000:

                    data_from_json[f"{user_id}"]["drone"] = 1
                    data_from_json[f"{user_id}"]["money"] -= 50000000
                    data_from_json[f"{user_id}"]["pet"] = "🤖 Дрон"
                    data_from_json[f"{user_id}"]["power"] += 70
                    await bot.send_message(message.from_user.id, "🤖 Вы купили дрона!")
                else:
                    await bot.send_message(message.from_user.id, "❌ У вас нет столько денег!")
            else: 
                await bot.send_message(message.from_user.id, "🤖 У вас уже есть дрон!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")  

@dp.message_handler(lambda msg: msg.text.startswith('🦝 Енот'))
async def enot(message: types.Message):
    try:
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())
            user_id = message.from_user.id
            if data_from_json[f"{user_id}"]["enot"] == 0:
                if data_from_json[f"{user_id}"]["money"] > 10000000:

                    data_from_json[f"{user_id}"]["enot"] = 1
                    data_from_json[f"{user_id}"]["money"] -= 10000000
                    data_from_json[f"{user_id}"]["pet"] = "🦝 Енот"
                    data_from_json[f"{user_id}"]["power"] += 50
                    await bot.send_message(message.from_user.id, "🦝 Вы купили енота!")
                else:
                    await bot.send_message(message.from_user.id, "❌ У вас нет столько денег!")
            else: 
                await bot.send_message(message.from_user.id, "🦝 У вас уже есть енот!")
        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    except KeyError:
        await bot.send_message(message.from_user.id, "❌ Вас нет в базе данных. Напишите - /start")  

@dp.message_handler()
async def echo(message: types.Message):
    text = message.text
    user_id = message.from_user.id
    if text.isdigit():
        with open("C:/IT/RPGbot/database.json", "r") as f_o:
            data_from_json = json.loads(f_o.read())

            data_from_json[f"{user_id}"]["apteka"] = int(text)

        with open("C:/IT/RPGbot/database.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
        ReplyKeyboardRemove()
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        yes = KeyboardButton("✔️ Да")
        no = KeyboardButton("❌ Нет")
        markup.add(yes, no)
        await bot.send_message(message.from_user.id, f"🩹 Вы хотите пополнить здоровье на {text}?", reply_markup=markup)
    else: 
        await bot.send_message(message.from_user.id, "⚠️ Я не распознал ваших слов!")

async def main():
    await dp.start_polling(bot)

keep_alive()
if __name__ == "__main__":
    asyncio.run(main())# Проверяем запускается ли этот файл
