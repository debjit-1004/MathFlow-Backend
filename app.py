from fastapi import FastAPI
from pydantic import BaseModel
from chain import break_into_main_steps, break_into_substeps  # Remove the dot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolutionRequest(BaseModel):
    solution: str

class StepRequest(BaseModel):
    step: str

@app.post("/split-solution")
async def split_solution(req: SolutionRequest):
    result = await break_into_main_steps(req.solution)
    return result  # Now returns both steps and graph data

@app.post("/split-step")
async def split_step(req: StepRequest):
    substeps = await break_into_substeps(req.step)
    return {"substeps": substeps}
