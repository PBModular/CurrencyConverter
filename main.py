import json
import aiohttp
from pyrogram.types import Message
from pyrogram import Client
from base.module import BaseModule, command

class CurrencyModule(BaseModule):
    API_URL = "https://api.exchangerate-api.com/v4/latest/"
    FLAG_CODES = {}
    
    def on_init(self):
        try:
            with open("flags.json", "r") as file:
                data = json.load(file)
                self.FLAG_CODES = data.get("flag_codes", {})
        except Exception as e:
            self.logger.error(e)

    async def fetch_data(self, session, url):
        async with session.get(url) as response:
            return await response.json()
    
    @command("currency")
    async def currency_command(self, client: Client, message: Message):
        command_parts = message.text.split(" ")

        if len(command_parts) < 3 and not command_parts[1].isnumeric():
            await message.reply_text(self.S["usage"])
            return

        number, source_currency = command_parts[1].upper(), command_parts[2].upper()
        target_currency = command_parts[3].upper() if len(command_parts) > 3 else None

        try:
            async with aiohttp.ClientSession() as session:
                response = await self.fetch_data(session, f"{self.API_URL}/{source_currency}")
                data = response
                
            if source_currency not in data["rates"]:
                await message.reply_text(self.S["invalid_currency"])
                return

            result_message = ""

            target_currencies = [target_currency] if target_currency else ["USD", "EUR", "GBP", "JPY", "CAD"]

            for target in target_currencies:
                if target == source_currency:
                    if not target_currency:
                        continue
                    
                    await message.reply_text(self.S["same_currency"])
                    return

                ratio = data["rates"][target] / data["rates"][source_currency]
                rate = data["rates"][target]
                result = round(float(number) * rate, 2)

                source_flag = self.FLAG_CODES.get(source_currency, "")
                target_flag = self.FLAG_CODES.get(target, "")

                result_message += (
                    f"{source_flag} ⇆ {target_flag}\n"
                    f"1 {source_currency} = {ratio} {target}\n"
                    f"{number} {source_currency} = {result} {target}\n\n"
                )

            await message.reply_text(result_message)

        except Exception as e:
            self.logger.error(e)
            await message.reply_text(self.S["error"])
