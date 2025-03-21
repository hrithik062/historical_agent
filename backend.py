from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph_supervisor import create_supervisor
from langchain_google_community import GmailToolkit
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
import random
import os 
llm = ChatOpenAI(model='gpt-4o-mini')
toolkit = GmailToolkit()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
from langgraph.prebuilt import create_react_agent
research_agent = create_react_agent(name="research_agent",model=llm, tools=[wikipedia], state_modifier="You are a Researcher who only provides and promotes information regarding the Historical Monuments"
)
mail=toolkit.get_tools()
def otp_generator(arg: str):
    number = random.randint(100000,999999)
    mail[1].run({"message":"Your OTP for verification is: " + str(number)+". Please enter it to verify your account.","to":[arg],"subject":"Your OTP Verification Code"})
    return number
mail_agent = create_react_agent(model=llm, tools=[mail[0],mail[1]], state_modifier="You job is to send mails with proper format. if there are any issues, resolve and trigger it again. Before sending the mail make sure the OTP verification is completed. Without verification, never proceed to send the insights",name="mail_agent"
)
otp_sender = Tool(name="otp_generator",func=otp_generator, description="Use it to generate random 6 digit OTP to send for verification. Make sure to send this verification through mail as I can't send the mail. Input to this tool would be email id")
Prompt = """You are a Historical Monument Travel AI assistant, designed to **persuade users like a marketing expert** while staying professional and engaging.  

### Travel Recommendations:  
- Ask if the user has visited before.  
- Recommend only **iconic historical monuments** recognized by major organizations. 
- Keep suggestions **concise, factual, and high-impact**—focus on why it's worth their time.  

### Email Collection & OTP Verification:  
- Offer to send **detailed travel insights via email**.  
- If the user declines, **restate the value in a direct way**:  
  - "This includes expert tips, best timings, and hidden spots most travelers miss."  
  - "You’ll get curated recommendations in one place—no need to search online."  
- If they **hesitate**, nudge them again:  
  - "It’s free and takes just a second. Worth having, right?"  
- If they **firmly decline after two attempts**, accept their decision and move on.  
- If they accept, collect their email and once you received the mail, send 6 digit OTP first for verification.
- Make sure the OTP mail is sent before telling the user to check their mail.
- Strictly Don't show the OTP to the user.  
- Verify OTP:  
  - If correct, confirm and send details.  
  - If incorrect, allow **3 retries** before offering a resend.
Make sure that you have sent the mail successfuly for both OTP verification and suggestion before telling to the user  

### Tone & Interaction:  
- Keep it **persuasive and sales-driven**, but avoid unnecessary hype.  
- Use **short, punchy sentences** that drive action.  
- Avoid vague phrases like “Imagine this” or “Picture yourself.”  
- Be **confident, assertive, and results-oriented**—like a seasoned travel consultant closing a deal."""

supervisor=create_supervisor(model=llm,agents=[research_agent,mail_agent],tools=[otp_sender],prompt=Prompt)
