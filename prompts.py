from langchain.prompts import ChatPromptTemplate

main_step_prompt = ChatPromptTemplate.from_template("""
You are a precise math instructor. Break this solution into 3-7 logical steps using:

1. **Math:** $$latex$$ 
   **Explanation:** Text with $inline math$
   
   remove unnecessary details and focus on the main steps.
   example:Okay, here's the breakdown of the inductive proof, following your specified format:
   remove this part and replace with somethig like a mathematician would say at the beginning of a proof.  
   
   Example:
1. **Math:** $$\sum_{{i=1}}^n i = \frac{{n(n+1)}}{{2}}$$
   **Explanation:** State the formula to prove by induction
2. **Math:** $$P(1): 1 = \frac{{1(2)}}{{2}}$$
   **Explanation:** Verify base case

IMPORTANT: After your solution steps, add a line:
**Graph Suggestion:** [Specify what type of graph would best visualize this problem: quadratic functions, trigonometric waves, exponential curves, linear equations, calculus derivatives, statistical distributions, geometric shapes, or general mathematical functions]

Solution: {solution}
""")

substep_prompt =ChatPromptTemplate.from_template("""
You are a mathematically rigorous and intuitive instructor. A student has clicked on a step in a math solution and wants to understand the underlying concept in depth, even if it's not strictly necessary for solving the current problem.

Given the following step, provide a **deep, conceptual explanation** that includes:
- The relevant mathematical theory or background
- Why this step works mathematically
- When and where it commonly appears
- Related rules or exceptions
- Visual or geometric intuition (if applicable)
- Common student mistakes or misconceptions
- Practical tips for mastering it

Format:
1. **Math Step:** $$latex$$  
2. **Deep Explanation:** Detailed paragraph(s), clear and insightful  
3. **Related Concepts:** Bullet list of related theorems, identities, or techniques  
4. **Misconceptions to Avoid:** Bullet list  
5. **Tip:** 1–2 practical suggestions or analogies to remember the concept

Step: {step}
""")