import time
import flet as ft
import model as md

class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view

    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language.lower())
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language.lower())
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language.lower())
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def handleLanguageChange(self, e):
        self._view._txtLanguage.value = f"Language {self._view._ddLanguage.value} selected corretly"
        self._view._txtLanguage.color = "green"
        self._view.update()

    def handleModalityChange(self, e):
        self._view._txtModality.value = f"Modality {self._view._ddModality.value} selected corretly"
        self._view._txtModality.color = "green"
        self._view.update()

    def handleSpellCheck(self, e):
        if not self.checkErrors():
            self._view._lv.controls.append(ft.Text(f"Errore! Uno o più campi non sono stati inseriti correttamente", color="red", size=20))
            self._view.update()
        else:
            self._view._lv.controls.clear()
            self._view.update()
            errate = self.handleSentence(self._view._txtIn.value, self._view._ddLanguage.value, self._view._ddModality.value)
            row1 = ft.Row(controls=[ft.Text(f"Frase da ricercare: ", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(self._view._txtIn.value, italic=True, size=18)], wrap=True)
            self._view._lv.controls.append(row1)
            row2 = ft.Row(controls=[ft.Text(f"Parole errate: ", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{errate[0]}", italic=True, size=18)], wrap=True)
            self._view._lv.controls.append(row2)
            row3 = ft.Row(controls=[ft.Text(f"Tempo di esecuzione: ", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{errate[1]} secondi", size=18)])
            self._view._lv.controls.append(row3)
            self._view.update()


    def checkErrors(self):
        if self._view._ddLanguage.value is None:
            return False
        elif self._view._ddModality.value is None:
            return False
        elif self._view._txtIn.value == "":
            return False
        return True

    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")


def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text