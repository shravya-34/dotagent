import os 
import re
import json
import sys 
sys.path.append(r'D:\DotagentDemo\dotagent')

from dotenv import load_dotenv
load_dotenv()

from dotagent import compiler
from dotagent.tools.basetool import Tool
from dotagent.helpers.math import PythonREPL
from dotagent.helpers.bash import BashProcess
from dotagent.helpers.serpapi import SerpAPIWrapper
from dotagent.helpers.ducksearch import DuckDuckGoSearchAPIWrapper

search = DuckDuckGoSearchAPIWrapper()
math = PythonREPL()
bash = BashProcess()
serp = SerpAPIWrapper(serpapi_api_key="3864588103371ef07ee835d1e5ff6bac6c885ade6fac564aceecd04702cfbd27")

serp = Tool(
    name = "Google Search tool",
    func = serp.run,
    description="useful when searching on internet"
)
math_tool = Tool(
    name="Math",
    func=math.run,
    description="Useful for doing mathematic calculations"
)
bash_tool = Tool(
    name="Bash",
    func=bash.run,
    description="Useful for executing Bash Commands"
)

tools = [math_tool,bash_tool,serp]

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
llm = compiler.llms.OpenAI(model="gpt-3.5-turbo-16k")

def tool_use(query, tools=tools):
    query = json.loads(query)
    return tools[int(query["index"])].func(query["query"])


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
experts = compiler(template='''
{{#system~}}
You are a helpful Web assistant. You are given a set of tools to use
{{~#each tools}}
{{this}}
{{/each}}
{{~/system}}

{{#user~}}
I want a response to the following question:
{{query}}
Think do you need to use the given tool to answer the question. Provide the answer in either <<Yes>> or <<No>>.
{{~/user}}

{{#assistant~}}
{{gen 'tools_use' temperature=0 max_tokens=300}}
{{~/assistant}}
                        
{{#user~}}
If the answer is Yes then call the tool using the following format '{"index":[index of the tool to be used in the tools list], "query":[query to be passed]'
If the answer is No, answer to the {{query}} itself.
{{~/user}}

{{#assistant~}}
{{gen 'action' temperature=0 max_tokens=500}}
{{#if (tools_use)=="Yes"}}
{{(tool_func action)}}
{{/if}}
{{~/assistant}}    
                        
{{#user~}}
Summarise the answer in one sentence
{{~/user}}
                        
{{#assistant~}}
{{gen 'final_answer' temperature=0 max_tokens=500}}
{{~/assistant}}
''', 
llm=llm, tools = tools, tool_func = tool_use, stream = False, OPENAI_API_KEY=OPENAI_API_KEY)


# execute the program for a specific goal
#Execute the bash command \'echo "hello world"\'
#2+2

out = experts(query='what is the age of current president of India as of today?')
print(out)