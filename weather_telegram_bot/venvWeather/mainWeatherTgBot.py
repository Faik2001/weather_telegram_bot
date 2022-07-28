import requests
import datetime
open_weather_token = "f85161682b46ce14a3f6b13b4abcb185"
tg_bot_token = "5526489200:AAEFmdh3_Ed7bLyxcWsPQOXa-W9pTrZDxV8"
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши ключевое слово 'прогноз', а затем название города и я пришлю сводку погоды!")



@dp.message_handler()
async def get_weather(message: types.Message):
    ans = message.text.upper();
    if "ПРОГНОЗ" in ans:
        ans = ans.replace("ПРОГНОЗ","");
        ans = ans.strip();
    else:
        ans = 0;
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={ans}&appid={open_weather_token}&units=metric"

        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd} \n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
            f"***Хорошего дня!***"
            )

    except:
        print(0)


if __name__=='__main__':
    executor.start_polling(dp)