#Discord and asyncio docs: https://github.com/Rapptz/discord.py/blob/async/examples/basic_bot.py
#Googletrans docs: https://pypi.org/project/googletrans/
#Developed a second version where the chatbot uses a prefix and command "!chatbot", instead of reading every message in the channel.
import discord, asyncio, random, requests
from discord.ext import commands
from discord.ext.commands import Bot
from googletrans import Translator, LANGUAGES
from chatterbot import ChatBot


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
    print("Online!")

async def translating(message):
    if len(function_list) != 0:
        return                  
    separate = message.split("'")
    if len(separate) == 3:
        sentence = separate[1]
        language = separate[2]
        for character in removal_list:
            language = language.replace(character, "")
            language = language.strip()
        for key in LANGUAGES:
            if LANGUAGES[key] == language:
                language = key 
        result = translator.translate(sentence, dest=language, src="auto")
        await bot.say(result.text)                                                                       
        function_list.append("called")
    else:
        await bot.say("Ex.: Can you translate 'how are you?' to french?")                             
        await bot.say("Specify what you want me to translate with a quotation :).")                          
        function_list.append("called")

async def cat(message):
    if len(function_list) != 0:
        return
    data_list = requests.get(cat_api_ulr).json()
    data_dict = data_list[0]
    image = data_dict["url"]
    data_list = requests.get(catfact_api_url).json()["all"]
    data_dict = data_list[random.randint(0, len(data_list))]
    fact = data_dict["text"]
    await bot.say(fact + "\n" + image)
    function_list.append("called")

async def chat(message):
    response = chatterbot.get_response(message)
    await bot.say(response)

@bot.command(pass_context=True)
async def chatbot(ctx, *message):
    """Main Function - Prefix""" 
    message = " ".join(message)
    for word in translator_input:
        if word in message:
            await translating(message)
    for word in cat_input:
        if word in message:
            await cat(message)
    if len(function_list) == 0:
        await chat(message)
    else:
        function_list.remove("called")

bot.run(TOKEN)