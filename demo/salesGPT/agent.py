import sys
sys.path.append(r'D:\DotagentDemo\dotagent')

import os
from dotagent import compiler
from dotagent.agent.base_agent import BaseAgent
from dotagent.llms._openai import OpenAI
from dotagent.memory import SimpleMemory
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

path = Path(__file__).parent / 'prompt.hbs'
salesagent_prompt_template = Path(path).read_text()

sales_coversation_memory = SimpleMemory()

class SalesAgent(BaseAgent):
    def __init__(self,
                use_tools: bool = False,
                prompt_template :str = salesagent_prompt_template,
                salesperson_name: str = "Ted Lasso",
                salesperson_role: str = "Business Development Representative",
                company_name: str = "Sleep Haven",
                company_business: str = "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers.",
                company_values: str = "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service.",
                conversation_purpose: str = "find out whether they are looking to achieve better sleep via buying a premier mattress.",
                conversation_type: str = "call",
                memory = sales_coversation_memory,
                **kwargs):
        super().__init__(**kwargs)

        self.prompt_template = prompt_template
        self.use_tools = use_tools
        self.salesperson_name = salesperson_name
        self.salesperson_role = salesperson_role
        self.company_name = company_name
        self.company_business = company_business
        self.company_values = company_values
        self.conversation_purpose = conversation_purpose
        self.conversation_type = conversation_type
        self.memory = memory
        self.llm = OpenAI('gpt-3.5-turbo')

        self.compiler = compiler(
            llm = self.llm,
            OPENAI_API_KEY = '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',
            template = self.prompt_template,
            salesperson_name = salesperson_name,
            salesperson_role = salesperson_role,
            company_name = company_name,
            company_business = company_business,
            company_values = company_values,
            conversation_purpose = conversation_purpose,
            conversation_type = conversation_type,
            caching=kwargs.get('caching'),
            memory = self.memory
        )

    def agent_type(self):
        return "chat"

agent = SalesAgent()
print(agent.run(user_text = "hello!?"))
print(agent.run(user_text = "I am doing good."))
print(agent.run(user_text = "Not much satisfied.he"))