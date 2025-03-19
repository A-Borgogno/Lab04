import time
import flet as ft
import model as md

class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view

    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split(" ")
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None


    def handleLanguageChange(self, e):
        self._view._txtLanguage.value = f"Lingua {self._view._ddLanguage.value} selezionata correttamente"
        self._view._txtLanguage.color = "green"
        self._view.page.update()

    def handleModalityChange(self, e):
        self._view._txtModality.value = f"Modalità {self._view._ddModality.value} selezionata correttamente"
        self._view._txtModality.color = "green"
        self._view.page.update()

    def handleSpellCheck(self, e):
        if not self.checkErrors():
            self._view._lv.controls.append(ft.Text(f"Errore! Uno o più campi non sono stati inseriti correttamente", color="red", size=20))
            self._view.page.update()
        else:
            self._view._lv.controls.clear()
            self._view.page.update()
            errate = self.handleSentence(self._view._txtIn.value, self._view._ddLanguage.value, self._view._ddModality.value)
            self._view._lv.controls.append(ft.Text(f"Frase da ricercare: {self._view._txtIn.value}", size=18))
            self._view._lv.controls.append(ft.Text(f"Parole errate: {errate[0]}", size=18))
            self._view._lv.controls.append(ft.Text(f"Tempo di esecuzione: {errate[1]}", size=18))
            self._view.page.update()

    def checkErrors(self):
        if self._view._ddLanguage.value == "Language not selected":
            return False
        elif self._view._ddModality == "Modality not selected":
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