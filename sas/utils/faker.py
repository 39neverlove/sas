from faker import Faker

def generate_user_data(region: str) -> dict:
    locale_map = {
        "Turkey": "tr_TR",
        "Kazakhstan": "kk_KZ",
        "Ukraine": "uk_UA",
        "Russia": "ru_RU"
    }
    locale = locale_map.get(region, "ru_RU")
    fake = Faker(locale)
    return {
        "username": fake.user_name(),
        "password": fake.password(length=12),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }