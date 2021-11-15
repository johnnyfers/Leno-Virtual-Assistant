import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

class Leon:
    def __init__(self):
        self.keepListening = True
        self.LANGUAGE = 'portuguese'
        self.stopwords = set(corpus.stopwords.words(self.LANGUAGE))
        
        with open('config.json', "r") as config_file:
            config = json.load(config_file)

            self.assistant_name = config["name"]
            self.actions = config["actions"]

            config_file.close()
    
    def main(self):
        while self.keepListening:
            try:
                command = self.get_speech()
                
                if command:
                    action, object = self.get_token(self,command)
                    isValid = self.command_validation(self, action , object)

                    if isValid:
                        print('passed')

                        self.command_exec(self, action)
                    else:
                        print("I didn't understand'!")
            except KeyboardInterrupt:
                print('bye')
    
    @staticmethod
    def get_speech():
        command = None
        recognizer = sr.Recognizer()
            
        with sr.Microphone() as audio_src:
            recognizer.adjust_for_ambient_noise(audio_src)
            
            print('Say something... ')
            speech = recognizer.listen(audio_src)
            
            try:
                command = recognizer.recognize_google(speech, language='pt-BR')
                
                print('Got something... ', command)
            except sr.UnknownValueError:
                print('Something went wrong')
        
        return command

    @staticmethod
    def remove_stopwords(self, tokens):
        filtered_tokens = []

        for token in tokens:
            if token not in self.stopwords:
                filtered_tokens.append(token)

        return filtered_tokens
    
    @staticmethod
    def get_token(self, command):
        action = None
        object = None
        
        tokens = word_tokenize(command, self.LANGUAGE)
        if tokens:
            tokens = self.remove_stopwords(self,tokens)
            
        print("token >>> " + str(tokens))
                
        if len(tokens) >= 3:
            if self.assistant_name == tokens[0].lower():
                action = tokens[1].lower()
                object = tokens[len(tokens) - 1].lower()   
           
        return action, object

    @staticmethod
    def command_validation(self, action, object):        
        isValid = False
        
        if action and object:
            for registered_action in self.actions:
                if action == registered_action["name"]:
                    if object in registered_action["objects"]:
                        isValid = True
                    break
        
        return isValid
    
    @staticmethod
    def readFile():
        print("Reading the file ...")
            
        try:
            f = open("./file.txt", "r")
            contents = f.read()
            f.close()
            
            print("reading... : ", contents)
        except:
            f = open("./file.txt", "w+")
            f.close()
            
    @staticmethod
    def writeFile(self):
        print("writing on the file ...")
        command = self.get_speech()
            
        f = open("./file.txt", "w+")
        f.write(command)

        print("writing... : ", command)
    
    @staticmethod
    def command_exec(self, action):
        if action == 'leia':
            self.readFile()
                
        if action == 'escreva':
            self.writeFile(self)
            
        if action == 'pare':
            print('bye')
            
            self.keepListening = False
        
l = Leon()

l.main()