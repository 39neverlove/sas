translations = {
    "ru": {
        "welcome": "Добро пожаловать! Выберите действие:",
        "create_account": "Создать аккаунты 🛠",
        "referral": "Реферальная система 💎",
        "support": "Поддержка 🆘",
        "stats": "Статистика 📊",
        "lang_select": "Выберите язык:",
        "no_accounts_left": "У вас нет доступных аккаунтов!",
        "rate_limit_exceeded": "Слишком много запросов! Попробуйте позже.",
        "account_created": "Аккаунт создан",
        "referral_link": "Ваша реферальная ссылка: {link}",
        "admin_menu": "Админ-панель:\n1. Статистика\n2. Управление пользователями\n3. Рассылка",
        "support_msg": "Свяжитесь с поддержкой: @drug0nly",
        "use_proxy": "Использовать прокси?",
        "yes": "Да",
        "no": "Нет"
    },
    "en": {
        "welcome": "Welcome! Choose an action:",
        "create_account": "Create accounts 🛠",
        "referral": "Referral system 💎",
        "support": "Support 🆘",
        "stats": "Statistics 📊",
        "lang_select": "Select language:",
        "no_accounts_left": "You have no available accounts!",
        "rate_limit_exceeded": "Too many requests! Try again later.",
        "account_created": "Account created",
        "referral_link": "Your referral link: {link}",
        "admin_menu": "Admin panel:\n1. Statistics\n2. User management\n3. Broadcast",
        "support_msg": "Contact support: @drug0nly",
        "use_proxy": "Use proxy?",
        "yes": "Yes",
        "no": "No"
    },
    "tr": {
        "welcome": "Hoş geldiniz! Bir işlem seçin:",
        "create_account": "Hesap oluştur 🛠",
        "referral": "Referans sistemi 💎",
        "support": "Destek 🆘",
        "stats": "İstatistikler 📊",
        "lang_select": "Dil seçin:",
        "no_accounts_left": "Kullanılabilir hesabınız yok!",
        "rate_limit_exceeded": "Çok fazla istek! Daha sonra tekrar deneyin.",
        "account_created": "Hesap oluşturuldu",
        "referral_link": "Referans bağlantınız: {link}",
        "admin_menu": "Yönetici paneli:\n1. İstatistikler\n2. Kullanıcı yönetimi\n3. Toplu mesaj",
        "support_msg": "Destek ile iletişime geçin: @drug0nly",
        "use_proxy": "Proxy kullan?",
        "yes": "Evet",
        "no": "Hayır"
    }
}

def get_translation(lang, key, **kwargs):
    text = translations.get(lang, translations["ru"]).get(key, key)
    return text.format(**kwargs)