import aiohttp
import asyncio
import json

class TempMail:
    BASE_URL = "https://api.mail.tm"

    async def create_email(self) -> dict:
        async with aiohttp.ClientSession() as session:
            # Создание домена
            async with session.get(f"{self.BASE_URL}/domains") as resp:
                domains = await resp.json()
                domain = domains[0]["domain"]

            # Генерация email
            username = f"user_{random.randint(1000, 9999)}"
            email = f"{username}@{domain}"
            password = f"pass_{random.randint(1000, 9999)}"

            # Регистрация email
            payload = {"address": email, "password": password}
            async with session.post(f"{self.BASE_URL}/accounts", json=payload) as resp:
                if resp.status != 201:
                    raise Exception("Failed to create email")
                account = await resp.json()

            return {"email": email, "password": password, "account_id": account["id"]}

    async def get_messages(self, account_id: str) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/messages?accountId={account_id}") as resp:
                if resp.status != 200:
                    raise Exception("Failed to fetch messages")
                return await resp.json()

    async def get_verification_link(self, account_id: str) -> str:
        for _ in range(5):  # Проверяем 5 раз с интервалом
            messages = await self.get_messages(account_id)
            for message in messages:
                if "Steam" in message.get("from", ""):
                    # Здесь должна быть логика извлечения ссылки из тела письма
                    return "https://store.steampowered.com/verification_link"  # Заглушка
            await asyncio.sleep(5)
        raise Exception("Verification link not found")