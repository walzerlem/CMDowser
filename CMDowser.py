import sys
import subprocess
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import gettext
import locale
import re

def get_system_language():
    try:
        sys_lang = locale.getdefaultlocale()[0]
        if sys_lang:
            return sys_lang[:2]
    except:
        pass
    return 'en'

temp_translations = {
    'en': {
        'install_deps': "Installing missing dependencies...",
        'deps_installed': "Dependencies installed successfully! Restarting...",
        'install_error': "Installation error: {}",
        'manual_install': "Please install manually: pip install {}",
        'setuptools_error': "Failed to install setuptools. Please install manually.",
        'restarting': "Restarting browser..."
    },
    'ru': {
        'install_deps': "Установка недостающих зависимостей...",
        'deps_installed': "Зависимости установлены! Перезапуск...",
        'install_error': "Ошибка установки: {}",
        'manual_install': "Установите вручную: pip install {}",
        'setuptools_error': "Ошибка установки setuptools. Установите вручную.",
        'restarting': "Перезапуск браузера..."
    },
    'uk': {
        'install_deps': "Встановлення відсутніх залежностей...",
        'deps_installed': "Залежності встановлено! Перезапуск...",
        'install_error': "Помилка встановлення: {}",
        'manual_install': "Встановіть вручну: pip install {}",
        'setuptools_error': "Помилка встановлення setuptools. Встановіть вручну.",
        'restarting': "Перезапуск браузера..."
    }
}

def install_dependencies():
    temp_lang = get_system_language()
    if temp_lang not in temp_translations:
        temp_lang = 'en'
    
    t = temp_translations[temp_lang]
    
    required = {'requests', 'beautifulsoup4'}
    missing = required
    
    try:
        import pkg_resources
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed
    except ImportError:
        try:
            print(t['install_deps'])
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'])
            import pkg_resources
            installed = {pkg.key for pkg in pkg_resources.working_set}
            missing = required - installed
        except:
            print(t['setuptools_error'])
            print(t['manual_install'].format(" ".join(required)))
            sys.exit(1)

    if missing:
        print(t['install_deps'])
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
            print(t['deps_installed'])
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(t['install_error'].format(e))
            print(t['manual_install'].format(" ".join(missing)))
            sys.exit(1)

install_dependencies()

class MultilingualBrowser:
    def __init__(self):
        self.history = []
        self.current_url = ""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TextBrowser/3.0 (MultiLang)'
        })
        self.language = "en"
        self.setup_translations()
        
    def setup_translations(self):
        if not os.path.exists('locales'):
            os.makedirs('locales')
            
        self.create_translation_files()
        
        self.translations = {
            "en": gettext.translation('browser', localedir='locales', languages=['en'], fallback=True),
            "ru": gettext.translation('browser', localedir='locales', languages=['ru'], fallback=True),
            "uk": gettext.translation('browser', localedir='locales', languages=['uk'], fallback=True)
        }
        self.translations["en"].install()
        
    def create_translation_files(self):
        en_path = 'locales/en/LC_MESSAGES'
        os.makedirs(en_path, exist_ok=True)
        with open(f'{en_path}/browser.po', 'w', encoding='utf-8') as f:
            f.write("""
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"

msgid "WELCOME_MSG"
msgstr "CMDowser (q-quit, h-history, lang-change language)"

msgid "ENTER_URL"
msgstr "Enter starting URL or command: "

msgid "ERROR"
msgstr "Error: "

msgid "LINKS_TITLE"
msgstr "LINKS:"

msgid "NO_LINKS"
msgstr "No links found"

msgid "PROMPT"
msgstr "\\nChoose link (№) or command (u-back, url, q-quit, lang-change language): "

msgid "INVALID_LINK"
msgstr "Invalid link number"

msgid "UNKNOWN_CMD"
msgstr "Unknown command"

msgid "CHANGE_LANG"
msgstr "Choose language (en, ru, uk): "

msgid "LANG_SET"
msgstr "Language set to: {}"

msgid "INVALID_LANG"
msgstr "Invalid language. Available: en, ru, uk"

msgid "PAGE_TEXT"
msgstr "Page content (first {} chars):"

msgid "INSTALLING_DEPS"
msgstr "Installing missing dependencies..."

msgid "DEPS_INSTALLED"
msgstr "Dependencies installed successfully! Restarting..."

msgid "INSTALL_ERROR"
msgstr "Installation error: {}"

msgid "MANUAL_INSTALL"
msgstr "Please install manually: pip install {}"

msgid "SETUPTOOLS_ERROR"
msgstr "Failed to install setuptools. Please install manually."

msgid "RESTARTING"
msgstr "Restarting browser..."

msgid "HELP_TITLE"
msgstr "COMMAND HELP"

msgid "HELP_COMMANDS"
msgstr "Available commands:"

msgid "HELP_LANG"
msgstr "Change interface language"

msgid "HELP_HELP"
msgstr "Show this help"

msgid "HELP_CLEAR"
msgstr "Clear the screen"

msgid "HELP_HISTORY"
msgstr "Show browsing history"

msgid "HELP_EXIT"
msgstr "Exit browser"

msgid "HELP_BACK"
msgstr "Go back to previous page"

msgid "HELP_LINK"
msgstr "Follow link by number"

msgid "HELP_URL"
msgstr "Go to specific URL"

msgid "HISTORY_TITLE"
msgstr "BROWSING HISTORY (last 10 sites)"

msgid "INVALID_URL"
msgstr "Invalid URL or command"
""")

        ru_path = 'locales/ru/LC_MESSAGES'
        os.makedirs(ru_path, exist_ok=True)
        with open(f'{ru_path}/browser.po', 'w', encoding='utf-8') as f:
            f.write("""
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"

msgid "WELCOME_MSG"
msgstr "CMDowser (q-выход, h-история, lang-сменить язык)"

msgid "ENTER_URL"
msgstr "Введите URL или команду: "

msgid "ERROR"
msgstr "Ошибка: "

msgid "LINKS_TITLE"
msgstr "ССЫЛКИ:"

msgid "NO_LINKS"
msgstr "Ссылок не найдено"

msgid "PROMPT"
msgstr "\\nВыберите ссылку (№) или команду (u-назад, url, q-выход, lang-сменить язык): "

msgid "INVALID_LINK"
msgstr "Неверный номер ссылки"

msgid "UNKNOWN_CMD"
msgstr "Неизвестная команда"

msgid "CHANGE_LANG"
msgstr "Выберите язык (en, ru, uk): "

msgid "LANG_SET"
msgstr "Язык изменен на: {}"

msgid "INVALID_LANG"
msgstr "Неверный язык. Доступны: en, ru, uk"

msgid "PAGE_TEXT"
msgstr "Содержимое страницы (первые {} символов):"

msgid "INSTALLING_DEPS"
msgstr "Установка недостающих зависимостей..."

msgid "DEPS_INSTALLED"
msgstr "Зависимости установлены! Перезапуск..."

msgid "INSTALL_ERROR"
msgstr "Ошибка установки: {}"

msgid "MANUAL_INSTALL"
msgstr "Установите вручную: pip install {}"

msgid "SETUPTOOLS_ERROR"
msgstr "Ошибка установки setuptools. Установите вручную."

msgid "RESTARTING"
msgstr "Перезапуск браузера..."

msgid "HELP_TITLE"
msgstr "СПРАВКА ПО КОМАНДАМ"

msgid "HELP_COMMANDS"
msgstr "Доступные команды:"

msgid "HELP_LANG"
msgstr "Сменить язык интерфейса"

msgid "HELP_HELP"
msgstr "Показать эту справку"

msgid "HELP_CLEAR"
msgstr "Очистить экран"

msgid "HELP_HISTORY"
msgstr "Показать историю посещений"

msgid "HELP_EXIT"
msgstr "Выйти из браузера"

msgid "HELP_BACK"
msgstr "Вернуться на предыдущую страницу"

msgid "HELP_LINK"
msgstr "Перейти по ссылке с номером"

msgid "HELP_URL"
msgstr "Перейти по указанному URL"

msgid "HISTORY_TITLE"
msgstr "ИСТОРИЯ ПОСЕЩЕНИЙ (последние 10 сайтов)"

msgid "INVALID_URL"
msgstr "Неверный URL или команда"
""")

        uk_path = 'locales/uk/LC_MESSAGES'
        os.makedirs(uk_path, exist_ok=True)
        with open(f'{uk_path}/browser.po', 'w', encoding='utf-8') as f:
            f.write("""
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"

msgid "WELCOME_MSG"
msgstr "CMDowser (q-вихід, h-історія, lang-змінити мову)"

msgid "ENTER_URL"
msgstr "Введіть URL або команду: "

msgid "ERROR"
msgstr "Помилка: "

msgid "LINKS_TITLE"
msgstr "ПОСИЛАННЯ:"

msgid "NO_LINKS"
msgstr "Посилань не знайдено"

msgid "PROMPT"
msgstr "\\nОберіть посилання (№) або команду (u-назад, url, q-вихід, lang-змінити мову): "

msgid "INVALID_LINK"
msgstr "Невірний номер посилання"

msgid "UNKNOWN_CMD"
msgstr "Невідома команда"

msgid "CHANGE_LANG"
msgstr "Оберіть мову (en, ru, uk): "

msgid "LANG_SET"
msgstr "Мову змінено на: {}"

msgid "INVALID_LANG"
msgstr "Невірна мова. Доступні: en, ru, uk"

msgid "PAGE_TEXT"
msgstr "Вміст сторінки (перші {} символів):"

msgid "INSTALLING_DEPS"
msgstr "Встановлення відсутніх залежностей..."

msgid "DEPS_INSTALLED"
msgstr "Залежності встановлено! Перезапуск..."

msgid "INSTALL_ERROR"
msgstr "Помилка встановлення: {}"

msgid "MANUAL_INSTALL"
msgstr "Встановіть вручну: pip install {}"

msgid "SETUPTOOLS_ERROR"
msgstr "Помилка встановлення setuptools. Встановіть вручну."

msgid "RESTARTING"
msgstr "Перезапуск браузера..."

msgid "HELP_TITLE"
msgstr "ДОВІДКА З КОМАНД"

msgid "HELP_COMMANDS"
msgstr "Доступні команди:"

msgid "HELP_LANG"
msgstr "Змінити мову інтерфейсу"

msgid "HELP_HELP"
msgstr "Показати цю довідку"

msgid "HELP_CLEAR"
msgstr "Очистити екран"

msgid "HELP_HISTORY"
msgstr "Показати історію відвідувань"

msgid "HELP_EXIT"
msgstr "Вийти з браузера"

msgid "HELP_BACK"
msgstr "Повернутись на попередню сторінку"

msgid "HELP_LINK"
msgstr "Перейти за посиланням за номером"

msgid "HELP_URL"
msgstr "Перейти за вказаним URL"

msgid "HISTORY_TITLE"
msgstr "ІСТОРІЯ ВІДВІДУВАНЬ (останні 10 сайтів)"

msgid "INVALID_URL"
msgstr "Невірний URL або команда"
""")
        
        for lang in ['en', 'ru', 'uk']:
            po_file = f'locales/{lang}/LC_MESSAGES/browser.po'
            mo_file = po_file.replace('.po', '.mo')
            if os.path.exists(po_file):
                try:
                    subprocess.check_call(['msgfmt', po_file, '-o', mo_file])
                except:
                    pass

    def set_language(self, lang_code):
        if lang_code in self.translations:
            self.language = lang_code
            self.translations[lang_code].install()
            return True
        return False

    def translate(self, key):
        return gettext.gettext(key)

    def fetch_page(self, url):
        try:
            response = self.session.get(url)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"{self.translate('ERROR')} {e}")
            return None

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 'form', 'iframe', 'aside', 'noscript']):
            element.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        links = [a for a in soup.find_all('a', href=True)]
        
        return text, links

    def display(self, text, links):
        print("\n" + "=" * 80)
        print(f"{self.translate('PAGE_TEXT').format(2000)}")
        print("=" * 40)
        print(text[:2000] + ("..." if len(text) > 2000 else ""))
        print("\n" + "=" * 80)
        
        if links:
            print(f"{self.translate('LINKS_TITLE')}")
            for i, link in enumerate(links[:20], 1):
                link_text = link.text.strip()[:50] + "..." if len(link.text.strip()) > 50 else link.text.strip()
                print(f"{i}. {link_text} [→ {link['href']}]")
        else:
            print(self.translate('NO_LINKS'))
    
    def process_command(self, command):
        command = command.strip().lower()
        
        if command.startswith('/lang'):
            parts = command.split()
            if len(parts) > 1:
                lang_code = parts[1].strip()
                return self.change_language(lang_code)
            else:
                return self.prompt_for_language()
        
        elif command == '/help':
            return self.show_help()
        
        elif command == '/clear':
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            return True
        
        elif command == '/history':
            self.show_history()
            return True
            
        elif command in ('/exit', '/quit'):
            return False
        
        elif command.startswith('/'):
            print(self.translate('UNKNOWN_CMD'))
            return True
            
        return None

    def change_language(self, lang_code):
        if self.set_language(lang_code):
            print(self.translate('LANG_SET').format(lang_code))
            return True
        else:
            print(self.translate('INVALID_LANG'))
            return self.prompt_for_language()

    def prompt_for_language(self):
        new_lang = input(self.translate('CHANGE_LANG')).strip().lower()
        if self.set_language(new_lang):
            print(self.translate('LANG_SET').format(new_lang))
            return True
        else:
            print(self.translate('INVALID_LANG'))
            return True

    def show_help(self):
        print("\n" + "=" * 80)
        print(self.translate('HELP_TITLE'))
        print("=" * 80)
        print(self.translate('HELP_COMMANDS'))
        print("  /lang <code> - " + self.translate('HELP_LANG'))
        print("  /help        - " + self.translate('HELP_HELP'))
        print("  /clear       - " + self.translate('HELP_CLEAR'))
        print("  /history     - " + self.translate('HELP_HISTORY'))
        print("  /exit        - " + self.translate('HELP_EXIT'))
        print("  u            - " + self.translate('HELP_BACK'))
        print("  <number>     - " + self.translate('HELP_LINK'))
        print("  <url>        - " + self.translate('HELP_URL'))
        print("\n" + "=" * 80)
        return True

    def show_history(self):
        print("\n" + "=" * 80)
        print(self.translate('HISTORY_TITLE'))
        print("=" * 80)
        for i, url in enumerate(self.history[-10:], 1):
            print(f"{i}. {url}")
        print("=" * 80)
        return True

    def run(self):
        sys_lang = get_system_language()
        if sys_lang not in ['en', 'ru', 'uk']:
            sys_lang = 'en'
        self.set_language(sys_lang)
        
        print(self.translate('WELCOME_MSG'))
        
        # Начальный ввод с поддержкой команд
        while True:
            user_input = input(self.translate('ENTER_URL')).strip()
            
            # Обработка команд
            if user_input.startswith('/'):
                result = self.process_command(user_input)
                if result is False:
                    return
                elif result is True:
                    continue
                else:
                    print(self.translate('INVALID_URL'))
                    continue
            
            # Обработка языковых команд без /
            command_lower = user_input.lower()
            if command_lower == 'lang':
                self.prompt_for_language()
                continue
            
            # Попытка загрузки URL
            self.current_url = user_input
            html = self.fetch_page(self.current_url)
            if html is not None:
                self.history.append(self.current_url)
                break
            else:
                print(self.translate('INVALID_URL'))
        
        # Основной цикл
        while True:
            html = self.fetch_page(self.current_url)
            if html is None:
                self.current_url = input(self.translate('ENTER_URL')).strip()
                continue
            
            self.history.append(self.current_url)
            text, links = self.parse_links(html)
            self.display(text, links)
            
            command = input(self.translate('PROMPT')).strip()
            
            if command.startswith('/'):
                result = self.process_command(command)
                if result is False:
                    break
                elif result is True:
                    continue
            
            command_lower = command.lower()
            
            if command_lower == 'q':
                break
            elif command_lower == 'u' and len(self.history) > 1:
                self.current_url = self.history[-2]
                self.history.pop()
            elif command_lower == 'lang':
                self.prompt_for_language()
            elif command_lower == 'help':
                self.show_help()
            elif command.isdigit():
                index = int(command) - 1
                if 0 <= index < len(links):
                    new_url = urljoin(self.current_url, links[index]['href'])
                    self.current_url = new_url
                else:
                    print(self.translate('INVALID_LINK'))
            elif re.match(r'^https?://', command_lower):
                self.current_url = command
            else:
                print(self.translate('UNKNOWN_CMD'))

if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass
    
    browser = MultilingualBrowser()
    browser.run()