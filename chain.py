import re
import numpy as np
import sympy as sp
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
    graph_suggestion = ""
    
    # Extract graph suggestion if present
    if '**Graph Suggestion:**' in content:
        parts = content.split('**Graph Suggestion:**')
        content = parts[0]
        if len(parts) > 1:
            graph_suggestion = parts[1].strip()
    
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
    
    return steps, graph_suggestion

def generate_graph_data(solution_text: str, graph_suggestion: str = "") -> dict:
    """Generate Plotly.js graph data based on the mathematical content and Gemini's suggestion"""
    
    # Use Gemini's suggestion if available
    suggestion_lower = graph_suggestion.lower()
    solution_lower = solution_text.lower()
    
    # Priority 1: Use Gemini's explicit suggestion
    if suggestion_lower:
        if 'quadratic' in suggestion_lower:
            return create_quadratic_graph()
        elif 'trigonometric' in suggestion_lower or 'trig' in suggestion_lower:
            return create_trig_graph()
        elif 'exponential' in suggestion_lower or 'exp' in suggestion_lower:
            return create_exponential_graph()
        elif 'linear' in suggestion_lower:
            return create_linear_graph()
        elif 'calculus' in suggestion_lower or 'derivative' in suggestion_lower:
            return create_calculus_graph()
        elif 'statistic' in suggestion_lower or 'distribution' in suggestion_lower:
            return create_statistics_graph()
    
    # Priority 2: Fallback to content detection
    # Pattern 1: Quadratic functions
    if any(keyword in solution_lower for keyword in ['quadratic', 'parabola', 'x^2', 'x²', 'ax^2', 'vertex']):
        return create_quadratic_graph()
    
    # Pattern 2: Trigonometric functions
    elif any(keyword in solution_lower for keyword in ['sin', 'cos', 'tan', 'trigonometric', 'sine', 'cosine']):
        return create_trig_graph()
    
    # Pattern 3: Exponential/logarithmic
    elif any(keyword in solution_lower for keyword in ['exponential', 'logarithm', 'log', 'ln', 'e^', 'exp']):
        return create_exponential_graph()
    
    # Pattern 4: Linear functions or systems
    elif any(keyword in solution_lower for keyword in ['linear', 'slope', 'y = mx', 'equation of line']):
        return create_linear_graph()
    
    # Pattern 5: Calculus (derivatives, integrals)
    elif any(keyword in solution_lower for keyword in ['derivative', 'integral', 'limit', 'tangent line', 'area under']):
        return create_calculus_graph()
    
    # Pattern 6: Statistics/Probability
    elif any(keyword in solution_lower for keyword in ['mean', 'median', 'standard deviation', 'probability', 'distribution']):
        return create_statistics_graph()
    
    # Default: Mathematical function visualization
    else:
        return create_default_function_graph()

def create_quadratic_graph() -> dict:
    """Create a quadratic function graph"""
    x = np.linspace(-5, 5, 100)
    y1 = x**2
    y2 = -0.5 * x**2 + 2*x + 1
    y3 = 0.3 * x**2 - x - 2
    
    return {
        "data": [
            {
                "x": x.tolist(),
                "y": y1.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "y = x²",
                "line": {"color": "blue"}
            },
            {
                "x": x.tolist(),
                "y": y2.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "y = -0.5x² + 2x + 1",
                "line": {"color": "red"}
            },
            {
                "x": x.tolist(),
                "y": y3.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "y = 0.3x² - x - 2",
                "line": {"color": "green"}
            }
        ],
        "layout": {
            "title": "Quadratic Functions",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "y"},
            "showlegend": True,
            "grid": True
        }
    }

def create_trig_graph() -> dict:
    """Create trigonometric functions graph"""
    x = np.linspace(-2*np.pi, 2*np.pi, 200)
    sin_y = np.sin(x)
    cos_y = np.cos(x)
    tan_y = np.tan(x)
    # Limit tan values to avoid infinity issues
    tan_y = np.where(np.abs(tan_y) > 10, np.nan, tan_y)
    
    return {
        "data": [
            {
                "x": x.tolist(),
                "y": sin_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "sin(x)",
                "line": {"color": "blue"}
            },
            {
                "x": x.tolist(),
                "y": cos_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "cos(x)",
                "line": {"color": "red"}
            },
            {
                "x": x.tolist(),
                "y": tan_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "tan(x)",
                "line": {"color": "green"}
            }
        ],
        "layout": {
            "title": "Trigonometric Functions",
            "xaxis": {"title": "x (radians)"},
            "yaxis": {"title": "y", "range": [-3, 3]},
            "showlegend": True
        }
    }

def create_exponential_graph() -> dict:
    """Create exponential and logarithmic functions graph"""
    x_exp = np.linspace(-3, 3, 100)
    x_log = np.linspace(0.1, 10, 100)
    
    exp_y = np.exp(x_exp)
    exp2_y = 2**x_exp
    log_y = np.log(x_log)
    log10_y = np.log10(x_log)
    
    return {
        "data": [
            {
                "x": x_exp.tolist(),
                "y": exp_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "e^x",
                "line": {"color": "blue"}
            },
            {
                "x": x_exp.tolist(),
                "y": exp2_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "2^x",
                "line": {"color": "red"}
            },
            {
                "x": x_log.tolist(),
                "y": log_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "ln(x)",
                "line": {"color": "green"}
            },
            {
                "x": x_log.tolist(),
                "y": log10_y.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "log₁₀(x)",
                "line": {"color": "orange"}
            }
        ],
        "layout": {
            "title": "Exponential and Logarithmic Functions",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "y"},
            "showlegend": True
        }
    }

def create_linear_graph() -> dict:
    """Create linear functions graph"""
    x = np.linspace(-5, 5, 100)
    y1 = 2*x + 1
    y2 = -0.5*x + 3
    y3 = x - 2
    
    return {
        "data": [
            {
                "x": x.tolist(),
                "y": y1.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "y = 2x + 1",
                "line": {"color": "blue"}
            },
            {
                "x": x.tolist(),
                "y": y2.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "y = -0.5x + 3",
                "line": {"color": "red"}
            },
            {
                "x": x.tolist(),
                "y": y3.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "y = x - 2",
                "line": {"color": "green"}
            }
        ],
        "layout": {
            "title": "Linear Functions",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "y"},
            "showlegend": True,
            "grid": True
        }
    }

def create_calculus_graph() -> dict:
    """Create a graph showing a function and its derivative"""
    x = np.linspace(-3, 3, 100)
    f_x = x**3 - 3*x**2 + 2*x + 1
    f_prime_x = 3*x**2 - 6*x + 2
    
    return {
        "data": [
            {
                "x": x.tolist(),
                "y": f_x.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "f(x) = x³ - 3x² + 2x + 1",
                "line": {"color": "blue", "width": 3}
            },
            {
                "x": x.tolist(),
                "y": f_prime_x.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "f'(x) = 3x² - 6x + 2",
                "line": {"color": "red", "width": 2, "dash": "dash"}
            }
        ],
        "layout": {
            "title": "Function and Its Derivative",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "y"},
            "showlegend": True,
            "annotations": [
                {
                    "text": "Blue: Original function<br>Red: Derivative",
                    "x": 0.02,
                    "y": 0.98,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "bgcolor": "rgba(255,255,255,0.8)"
                }
            ]
        }
    }

def create_statistics_graph() -> dict:
    """Create a statistical distribution graph"""
    x = np.linspace(-4, 4, 100)
    normal_dist = (1/np.sqrt(2*np.pi)) * np.exp(-0.5 * x**2)
    
    # Sample data for histogram
    np.random.seed(42)
    sample_data = np.random.normal(0, 1, 1000)
    
    return {
        "data": [
            {
                "x": x.tolist(),
                "y": normal_dist.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "Standard Normal Distribution",
                "line": {"color": "blue", "width": 3}
            },
            {
                "x": sample_data.tolist(),
                "type": "histogram",
                "name": "Sample Data",
                "opacity": 0.7,
                "nbinsx": 30,
                "marker": {"color": "lightblue"},
                "yaxis": "y2"
            }
        ],
        "layout": {
            "title": "Normal Distribution and Sample Data",
            "xaxis": {"title": "Value"},
            "yaxis": {"title": "Probability Density", "side": "left"},
            "yaxis2": {"title": "Frequency", "side": "right", "overlaying": "y"},
            "showlegend": True,
            "barmode": "overlay"
        }
    }

def create_default_function_graph() -> dict:
    """Create a default mathematical function graph"""
    x = np.linspace(-5, 5, 100)
    y1 = x**2
    y2 = np.sin(x)
    y3 = np.exp(-x**2/4)  # Gaussian
    
    return {
        "data": [
            {
                "x": x.tolist(),
                "y": y1.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "Quadratic: y = x²",
                "line": {"color": "blue"}
            },
            {
                "x": x.tolist(),
                "y": y2.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "Trigonometric: y = sin(x)",
                "line": {"color": "red"}
            },
            {
                "x": x.tolist(),
                "y": y3.tolist(),
                "type": "scatter",
                "mode": "lines",
                "name": "Gaussian: y = e^(-x²/4)",
                "line": {"color": "green"}
            }
        ],
        "layout": {
            "title": "Common Mathematical Functions",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "y"},
            "showlegend": True,
            "grid": True
        }
    }



async def break_into_main_steps(solution_text: str) -> dict:
    # Escape curly braces in user input
    escaped_solution = solution_text.replace("{", "{{").replace("}", "}}")
    chain = main_step_prompt | llm
    result = await chain.ainvoke({"solution": escaped_solution})
    
    # Parse steps and graph suggestion
    steps, graph_suggestion = await parse_steps(result.content)
    
    # Generate graph data using both solution content and Gemini's suggestion
    graph_data = generate_graph_data(solution_text, graph_suggestion)
    
    return {
        "steps": steps,
        "graph": graph_data
    }

async def break_into_substeps(step_text: str) -> list:
    escaped_step = step_text.replace("{", "{{").replace("}", "}}")
    chain = substep_prompt | llm
    result = await chain.ainvoke({"step": escaped_step})
    steps, _ = await parse_steps(result.content)  # Ignore graph suggestion for substeps
    return steps