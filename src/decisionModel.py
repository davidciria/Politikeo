import pickle
import numpy as np
import tweepy
import emoji
import regex
import re
import nltk
from textblob import TextBlob
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

class DecisionModel:

    def __init__(self, screen_user, api):
        self.screen_user = screen_user
        self.api = api

    def loadPickleObject(self, file):
        with open(file, 'rb') as read_object:
            return pickle.load(read_object)
      
    # Funcio que retorna el ifidf de cada instancia (en el nostre cas seran words o emojis).
    def tfidf(self, ocurrenceList):
        # Obtenim un array amb les instancies diferents.
        flat_list = [item[0] for sublist in ocurrenceList for item in sublist]
        diffInstances = set(flat_list)
        instanceIdf = {}
        for instance in diffInstances:
            instanceIdf[instance] = 0
            for party in ocurrenceList:
                for partyInstance, _ in party:
                    if partyInstance == instance:
                        instanceIdf[instance] += 1
        return instanceIdf

    # Obtenir el nom d'usuari.
    def getUserName(self):
        u = self.api.get_user(self.screen_user)
        return u.name

    def getUserDescription(self):
        u = self.api.get_user(self.screen_user)
        return u.description

    def countEmojis(self, text,mainDict):
        #Retorna una llista amb els emojis d'un text.
        def Emojify(text):
            global emoji
            emoji_list = []
            data = regex.findall(r'\X', text)
            for word in data:
                if any(char in emoji.UNICODE_EMOJI for char in word):
                    emoji_list.append(word)

            return emoji_list

        #obtenim la llista de emojis per un text concret
        lt = list(Emojify(text)) # Set deleted
        #filtrem casos excepcionals
        if "🇪🇦" in lt:
            lt.remove("🇪🇦")
            lt.append("🇪🇸")
        if "❤" in lt:
            lt.remove("❤")
            lt.append("❤️")
        #afegim les ocurrencies a un diccionari 
        for emoji in lt:
            if emoji in mainDict:
                mainDict[emoji] += 1
            else:
                mainDict[emoji] = 1
        return mainDict

    def getPartiesScores(self, userNameAndDesc, instancesList, Tfidf):
        scores = {}
        PartiesSum = []
        for index, _ in enumerate(instancesList):
            PartiesSum.append(np.sum([value for i, value in instancesList[index]]))
            scores[index] = 0

        for i, value in userNameAndDesc:
                for index, party in enumerate(instancesList):
                    for instance, num in party:
                        if i == instance:
                            scores[index] += value *np.log(len(instancesList)/Tfidf[instance]) * num/PartiesSum[index]

        return scores.values()
    

    def emojisScores(self):
        # Vox, PP, CS, PSOE, UP.
        emojiList = self.loadPickleObject("./data/emojiList.pkl")

        emojiTfidf = self.tfidf(emojiList)

        # Obtenim el nom y descripcio del usuari.
        user_name = self.getUserName()
        user_description = self.getUserDescription()

        # Fem el primer diccionari de emojis al user_name
        user_name_emojis = self.countEmojis(user_name, {})
        # Partim del primer diccionari i afegim els emojis restants del user_description
        user_name_and_description_emojis = list(self.countEmojis(user_description, user_name_emojis).items())
        
        partiesScores = self.getPartiesScores(user_name_and_description_emojis, emojiList, emojiTfidf)

        return partiesScores

    def countKeywords(self, text, mainDict):

        sbEsp = SnowballStemmer('spanish') #Stemmer para obtener el lema de las palabras.

        def deEmojify(text):
            string = ""
            data = regex.findall(r'\X', text)
            for word in data:
                for char in word:
                    if not char in emoji.UNICODE_EMOJI:
                        string = string + char

            return string

        def removeStopwords(texto):
            texto = texto.lower()
            texto = re.sub('_', '', texto)
            texto = re.sub('@', '', texto)
            texto = re.sub(':', '', texto)
            texto = re.sub('/', '', texto)
            texto = re.sub('!', '', texto)
            texto = re.sub('_', '', texto)
            texto = re.sub('\.', '', texto)
            texto = deEmojify(texto)
            blob = TextBlob(texto).words
            
            outputlist = [sbEsp.stem(word) for word in blob if word not in stopwords.words('spanish')]
    
            return(outputlist)

        def countWords(lt, mainDict):
            for emoji in lt:
                if emoji in mainDict:
                    mainDict[emoji] += 1
                else:
                    mainDict[emoji] = 1
            return mainDict

        return countWords(removeStopwords(text), mainDict)

    def keywordsScores(self):
        # Vox, PP, CS, PSOE, UP.
        keywordsList = self.loadPickleObject("./data/keywordsList.pkl")

        keywordsTfidf = self.tfidf(keywordsList)

        # Obtenim el nom y descripcio del usuari.
        user_name = self.getUserName()
        user_description = self.getUserDescription()

        # Fem el primer diccionari de emojis al user_name
        user_name_keywords = self.countKeywords(user_name, {})
        # Partim del primer diccionari i afegim els emojis restants del user_description
        user_name_and_description_keywords = list(self.countKeywords(user_description, user_name_keywords).items())
        
        partiesScores = self.getPartiesScores(user_name_and_description_keywords, keywordsList, keywordsTfidf)

        return partiesScores