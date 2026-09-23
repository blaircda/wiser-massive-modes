# baseline files to treat as read only
Do not modify: massive_SO10.py, massive_SO8_construct.py, massive_SO8_to_S010.py, massive_SO8_to_SO9.py
These are the baseline verification files established by the human.
They define the current known level-1–10 SO(10) result and must remain unchanged.
Create new scripts for experiments or extensions.

# Literature search skill
When doing literature searches or exploring arXiv papers, read and follow the procedure in:
.agents/skills/hepth-arxiv-inspire-literature-exploration/SKILL.md

# LaTeX formatting in .md files

Do not use \begin{aligned} ... \end{aligned}, instead just use individual equations.

# making claims
When producing reports to the human, be more guarded in interpreting results speculatively. If some expression appearing is reminiscent of a known interesting physical or mathematical phenomen it is fine to note that, but do not treat coincidence as established proof. 

# Scientific Integrity & Derivation Rules
1. **No Circular Seeding:**
   Scripts that claim to derive, uplift, or reconstruct representations from first principles or generating functions must NEVER import the baseline verification files (`massive_SO10.py`, etc.). Comparison against baseline must always happen in a separate verification step.
2. **Obstructions Over Artificial Success:**
   Do not patch failing algorithms with ground-truth lookups to make milestone checks pass. If an algorithm encounters an infinite loop, negative multiplicities, or algebraic non-divisibility, stop and document the mathematical obstruction. Discovering why an uplift fails algebraically is just as valuable as a successful proof.
3. **No Dead-Code Claims:**
   Never declare a milestone passed based on a function that is bypassed or commented out in the actual execution flow. Every claimed computation must be actively executed in the script.
