import requests
from pyrogram.types import Message
from pyrogram import Client
from base.module import BaseModule, command

class CurrencyModule(BaseModule):
    API_URL = "https://api.exchangerate-api.com/v4/latest/"

    @command("currency")
    def currency_command(self, client: Client, message: Message):
        command_parts = message.text.split(" ")

        if len(command_parts) != 4:
            message.reply(self.S["usage"])
            return

        number, source_currency, target_currency = command_parts[1].upper(), command_parts[2].upper(), command_parts[3].upper()
        try:
            response = requests.get(f"{self.API_URL}/{source_currency}")
            data = response.json()

            if source_currency not in data["rates"] or target_currency not in data["rates"]:
                message.reply(self.S["invalid_currency"])
                return

            ratio = data["rates"][target_currency] / data["rates"][source_currency]
            rate = data["rates"][target_currency]
            result = round(float(number) * rate, 2)

            message.reply(f"1 {source_currency} = {ratio} {target_currency}\n{number} {source_currency} = {result} {target_currency}")

        except Exception as e:
            self.logger.error(e)
            message.reply(self.S["error"])
