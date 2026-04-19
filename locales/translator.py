import subprocess
import polib
import gettext


class Translator:

    def __init__(self):
        self.lang = None

    def change_language(self, lang):
        self.lang = lang

    def scan_script(self):
        """
        Scan all .py files in project and create messages.pot
        """
        subprocess.run([
            "bash",
            "-c",
            "find . -name '*.py' | xargs xgettext "
            "-d messages "
            "-o locales/messages.pot "
            "--from-code=UTF-8"
        ], check=True)

    def create_translation(self, lang: str, locale: str):
        """
        Create a .po file for translation from the .pot file
        """
        subprocess.run([
            "msginit",
            "-l", locale,
            "-o", f"locales/{lang}/LC_MESSAGES/messages.po",
            "-i", "locales/messages.pot",
            "--no-translator"
        ], check=True)

    def write_translation(self, lang, word, translation):
        po_path = f"locales/{lang}/LC_MESSAGES/messages.po"
        po = polib.pofile(po_path)
        po.metadata["Content-Type"] = "text/plain; charset=UTF-8"
        po.metadata["Content-Transfer-Encoding"] = "8bit"
        entry = po.find(word)

        if entry:
            entry.msgstr = translation
        else:
            po.append(
                polib.POEntry(
                    msgid=word,
                    msgstr=translation
                )
            )

        po.save()
        po.save_as_mofile(po_path.replace(".po", ".mo"))

    def mark_translation(self):
        """
        Activate selected language
        """
        if not self.lang:
            raise ValueError("Language not set")

        gettext.bindtextdomain("messages", "locales")
        gettext.textdomain("messages")

        lang = gettext.translation(
            "messages",
            "locales",
            languages=[self.lang]
        )

        lang.install()
        return lang.gettext

    @staticmethod
    def get_locale():
        result = subprocess.run(
            ["locale", "-a"],
            capture_output=True,
            text=True
        )
        return result.stdout
