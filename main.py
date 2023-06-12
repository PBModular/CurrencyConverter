import requests
from pyrogram.types import Message
from pyrogram import Client
from base.module import BaseModule, command

class CurrencyModule(BaseModule):
    API_URL = "https://api.exchangerate-api.com/v4/latest/"

    @command("currency")
    def currency_command(self, client: Client, message: Message):
        command_parts = message.text.split(" ")

        if len(command_parts) < 3:
            message.reply(self.S["usage"])
            return

        number, source_currency = command_parts[1].upper(), command_parts[2].upper()
        target_currencies = ["USD", "EUR", "GBP", "JPY", "CAD"]

        if len(command_parts) > 3:
            target_currency = command_parts[3].upper()
            target_currencies = [target_currency]

        try:
            response = requests.get(f"{self.API_URL}/{source_currency}")
            data = response.json()

            if source_currency not in data["rates"]:
                message.reply(self.S["invalid_currency"])
                return

            result_message = ""

            for target_currency in target_currencies:
                if target_currency == source_currency:
                    message.reply(self.S["same_currency"])
                    return
                
                ratio = data["rates"][target_currency] / data["rates"][source_currency]
                rate = data["rates"][target_currency]
                result = round(float(number) * rate, 2)

                result_message += f"1 {source_currency} = {ratio} {target_currency}\n{number} {source_currency} = {result} {target_currency}\n\n"

            message.reply(result_message)

        except Exception as e:
            self.logger.error(e)
            message.reply(self.S["error"])
