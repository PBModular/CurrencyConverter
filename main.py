import requests
from pyrogram.types import Message
from base.module import BaseModule
from base.module import command
from pyrogram import Client

class CurrencyModule(BaseModule):
    @command("currency")
    def currency_command(self, client: Client, message: Message):
        command_parts = message.text.split(" ")
        if len(command_parts) != 4:
            message.reply("Использование: /currency <number> <source_currency> <target_currency>")
            return

        number = command_parts[1]
        source_currency = command_parts[2].upper()
        target_currency = command_parts[3].upper()

        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{source_currency}")
            data = response.json()

            if source_currency not in data["rates"] or target_currency not in data["rates"]:
                message.reply("Неверно указаны валюты.")
                return

            rate = data["rates"][target_currency]
            result = float(number) * rate

            message.reply(f"{number} {source_currency} = {result} {target_currency}")

        except Exception as e:
            message.reply("Произошла ошибка при выполнении команды.")