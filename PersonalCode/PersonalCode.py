#Discord and asyncio docs: https://github.com/Rapptz/discord.py/blob/async/examples/basic_bot.py #https://discordpy.readthedocs.io/en/rewrite/index.html
#Googletrans docs: https://pypi.org/project/googletrans/, https://py-googletrans.readthedocs.io/en/latest/
#Fixed googletrans error through : https://github.com/ssut/py-googletrans/issues/93
import discord, asyncio, random, requests
from discord.ext import commands
from discord.ext.commands import Bot, Context
from googletrans import Translator, LANGUAGES
from chatterbot import ChatBot

#Defining constants
bot = commands.Bot(command_prefix="!")
translator = Translator()
chatterbot = ChatBot("Koneko",
input_adapter = 'chatterbot.input.VariableInputTypeAdapter',
output_adapter ='chatterbot.output.OutputAdapter',
output_format="text",
database ='./ChatterbotDatabase.sqlite3')
TOKEN = "Add your token here."
cat_api_ulr = "https://api.thecatapi.com/v1/images/search?size=full&mime_types=jpg,png,gif&format=json&order=RANDOM&page=0&limit=1"
catfact_api_url = "https://cat-fact.herokuapp.com/facts"
translator_input = ["translate", "translator", "say"]
cat_input = ["cat", "cats", "neko", "kitten"]
removal_list = ["," , "?", "!", ".", "to", "please", "in"]
function_list = []

@bot.event
async def on_ready():
    """Prints a message in the console once the Bot has come online"""
    print("Online!")

async def translating(message):
    """Translates a specific part of the user input, indicated by a quotation. """
    #Prevents the calling of other functions in case two keywords have been used.
    if len(function_list) != 0:
        return
    user_input = message.content.lower()
    separate = user_input.split("'")
    #Splitting the user input into 3 parts. [0]Keyword - useless at this point, [1]Sentence to be translated, [2]Language you want it translated to.
    if len(separate) == 3:
        sentence = separate[1]
        language = separate[2]
        #Removing excess characters and words. The goal is to have language == for example "portuguese"
        for character in removal_list:
            language = language.replace(character, "")
            language = language.strip()
        #A dictionary included in the module with all the languages it supports (en:english, fr:french...)
        for key in LANGUAGES:
            if LANGUAGES[key] == language:
                language = key 
        #Using the google translator API through the module, we receive a translation.
        result = translator.translate(sentence, dest=language, src="auto")
        await bot.send_message(message.channel, result.text)
        function_list.append("called")
    else:
        #If the keyword is met, but the formatting is wrong, it returns an explanation along with an example.
        await bot.send_message(message.channel, "Specify what you want me to translate with a quotation :).")
        await bot.send_message(message.channel, "Ex.: Can you translate 'how are you?' to french?")
        #Appending an element into a list to keep track of whether a function has been called.
        function_list.append("called")

async def cat(message):
    """Generates a cute cat fact + image"""
    if len(function_list) != 0:
        return
    #Reading and assigning the data in json format to a variable.
    data_list = requests.get(cat_api_ulr).json()
    data_dict = data_list[0]
    #The data I'm interested in is in the "url" key of the dictionary.
    image = data_dict["url"]
    data_list = requests.get(catfact_api_url).json()["all"]
    data_dict = data_list[random.randint(0, len(data_list))]
    fact = data_dict["text"]
    await bot.send_message(message.channel, (fact + "\n" + image))
    function_list.append("called")

async def chat(message):
    """Chatterbot module function"""
    response = chatterbot.get_response(message.content)
    await bot.send_message(message.channel, response)
    #Chatterbot training was done with the code below.

"""
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

chatterbot = ChatBot("Koneko",
input_adapter = 'chatterbot.input.VariableInputTypeAdapter',
output_adapter ='chatterbot.output.OutputAdapter',
output_format="text",
database ='./ChatterbotDatabase.sqlite3')

#chatterbot.set_trainer(ChatterBotCorpusTrainer)
chatterbot.set_trainer(ListTrainer)
List1 = open("./TrainingData/MovieCorpus.txt", encoding='utf-8').read().splitlines()
List2 = open("./TrainingData/TwitterLowerAsciiCorpus.txt", encoding='utf-8').read().splitlines()

chatterbot.train(
        List2
)
"""



@bot.event
async def on_message(message):
    """Main function - No Prefix"""
    #Prevents the chatbot from taking its own messages as input.
    if message.author.bot is True:
        return
    #Calling specific functions based on keywords in the user input. Only one can be called with each input.
    for word in translator_input:
        if word in message.content:
            await translating(message)
    for word in cat_input:
        if word in message.content:
            await cat(message)
    #If none of the above functions were called, call the chatbot function.
    if len(function_list) == 0:
        await chat(message)
    else:
        function_list.remove("called") #Clearing the list awaiting new user input.


bot.run(TOKEN)

"""
async def functionCall(message):
    call_function = {key:translating(message) for key in translator_input}
    for key in cat_input:
       call_function[key] = cat(message)
    for word in call_function:
        if word in message.content:
            await call_function[word]
        else:
            pass
"""

"""
async def inputCheck(list, function, user_input):
    for word in list:
        if word in user_input:
            await function
        else:
            return
"""
"""
    await inputCheck(translator_input, translating(message), user_input)
    await inputCheck(cat_input, cat(message), user_input)
"""
