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

Solution: {solution}
""")

substep_prompt = ChatPromptTemplate.from_template("""
You are a detailed math assistant. Break this step into substeps using:

1. **Math:** $$latex$$ 
   **Explanation:** Brief reasoning
   
   remove unnecessary details and focus on the main steps.
   example:Okay, here's the breakdown of the inductive proof, following your specified format:
   remove this part and replace with somethig like a mathematician would say at the beginning of a proof.  

Example:
1. **Math:** $$\sum_{{i=1}}^{{k+1}} i = \sum_{{i=1}}^k i + (k+1)$$
   **Explanation:** Separate last term

Step: {step}
""")