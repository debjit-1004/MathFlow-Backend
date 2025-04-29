import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain

import os
from dotenv import load_dotenv
from prompts import main_step_prompt, substep_prompt

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

async def parse_steps(content: str) -> list:
    steps = []
    # Split by numbered items using lookahead for next number
    raw_steps = re.split(r'\n(?=\d+\. )', content)
    
    for step in raw_steps:
        # Clean numbering and whitespace
        clean_step = re.sub(r'^\d+\.\s*', '', step).strip()
        
        # Split math and explanation
        math, explanation = "", ""
        if '**Explanation:**' in clean_step:
            math_part, expl_part = clean_step.split('**Explanation:**', 1)
            math = math_part.replace('**Math:**', '').strip()
            explanation = expl_part.strip()
        else:
            math = clean_step.replace('**Math:**', '').strip()
        
        steps.append({
            "math": math,
            "explanation": explanation
        })
    
    return steps



async def break_into_main_steps(solution_text: str) -> list:
    # Escape curly braces in user input
    escaped_solution = solution_text.replace("{", "{{").replace("}", "}}")
    chain = main_step_prompt | llm
    result = await chain.ainvoke({"solution": escaped_solution})
    return await parse_steps(result.content)

async def break_into_substeps(step_text: str) -> list:
    escaped_step = step_text.replace("{", "{{").replace("}", "}}")
    chain = substep_prompt | llm
    result = await chain.ainvoke({"step": escaped_step})
    return await parse_steps(result.content)