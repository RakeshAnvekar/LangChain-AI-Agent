from langchain_openai import ChatOpenAI

from langchain_core.tools import Tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# Create a search tool using DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Create a language model instance
llm= ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# I havr tool and llm ready, now I will create an agent that can use the tool to answer questions
from langchain.agents import AgentExecutor, create_react_agent #It allows the AI to think (reason) and take actions (use tools) step by step to solve a problem.
from langchain import hub
                            # Question
                            #    ↓
                            # Thought (reason about what to do)
                            #    ↓
                            # Action (choose a tool)
                            #    ↓
                            # Observation (tool result)
                            #    ↓
                            # Thought
                            #    ↓
                            # Final Answer
#---------------------------------------------------------------------
                            # What is the capital of France?
                            # Thought: I should search for the capital of France
                            # Action: DuckDuckGoSearch
                            # Action Input: capital of France
                            # Observation: Paris is the capital of France
                            # Thought: I now know the answer
                            # Final Answer: Paris


#     | Component              | Responsibility                                |
# | ---------------------- | --------------------------------------------- |
# | **create_react_agent** | Decides **which tool to use** (reasoning)     |
# | **AgentExecutor**      | **Runs the agent loop and executes the tool** |

                        
prompt= hub.pull("hwchase17/react")
# This downloads a prompt template from LangChain Hub.

# Think of it like downloading a ready-made instruction guide for the agent.
# | Part        | Meaning                                                  |
# | ----------- | -------------------------------------------------------- |
# | `hwchase17` | Creator of the prompt (LangChain founder Harrison Chase) |
# | `react`     | ReAct agent prompt template                              |


agent=create_react_agent(llm=llm, tools=[search_tool], prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)
#verbose=True is used to show detailed logs of what the agent is doing internally, including the thoughts, actions, and observations. This is helpful for debugging and understanding the agent's reasoning process.
# Now I can use the agent to answer questions
question = "3 ways to reac goa from delhi?"
answer = agent_executor.invoke({"input": question})
print(answer["output"])








