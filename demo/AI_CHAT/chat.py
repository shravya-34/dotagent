import os 
import pytesseract
from PIL import Image
from pathlib import Path
import sys
sys.path.append(r'D:/DotagentDemo/dotagent')

from dotenv import load_dotenv
load_dotenv()

from dotagent import compiler
from dotagent.memory import SimpleMemory
from dotagent.llms._openai import OpenAI
from dotagent.agent.base_agent import BaseAgent

path = Path(__file__).parent / 'chat.hbs'
interview_template = Path(path).read_text()
interview_memory = SimpleMemory()
config = '--psm 11 --oem 3'
image = Image.open('chat2.jpg')
chat = pytesseract.image_to_string(image, config=config)

words = chat.split()
index = 0
while index<len(words):
    word = words[index]
    if len(word)<1 or not word[0].isalnum():
        del words[index]
    elif len(word)==1:
        index += 1
    else:
        delete = False
        if word[0].isdigit():
            for i in range(1, len(word)):
                if not word[i].isdigit():
                    delete = True
                    del words[index]
                    break 
        if delete:
            continue
        index += 1
chat = ' '.join(words) 
print(chat, '\n')
    

class ApnaChat(BaseAgent):
    def __init__(self, 
                use_tools: bool = False,
                prompt_template: str = interview_template,
                memory = interview_memory,
                name = 'ApnaChat',
                **kwargs):
        super().__init__(**kwargs)

        self.prompt_template = prompt_template
        self.use_tools = use_tools
        self.memory = memory
        self.name = name
        self.llm = OpenAI(os.environ.get('OPENAI_MODEL'))
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        # self.function = function

        self.compiler = compiler(
            llm = self.llm,
            OPENAI_API_KEY = self.OPENAI_API_KEY,
            template = self.prompt_template,
            caching=kwargs.get('caching'),
            memory = self.memory,
            name = self.name ,
            # function = self.function
        )
        
agent = ApnaChat()
print(agent.run(user_text = chat))
