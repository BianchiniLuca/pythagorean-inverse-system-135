\# Pythagorean Inverse System 1–3–5



Research toolbox for enumerating abstract seeds and testing deterministic canon generation in the inverse 1–3–5 system.



This repository contains the computational core used to study cyclic seeds built from the alphabet {1,3,5} under contrapuntal constraints.



Reference preprint (Zenodo):

https://zenodo.org/records/18497758



The project explores:



\- enumeration of cyclic seeds with unique bigrams

\- structural limits of canon generation

\- computational verification of impossibility results



\## Example



The script:



examples/prove\_9\_voci.py



verifies that under the current constraints a canon with 9 voices is impossible.



Run:



&nbsp;   python examples/prove\_9\_voci.py



\## Project structure



&nbsp;   src/

&nbsp;       pythagorean\_inverse\_system\_135/

&nbsp;           canon.py

&nbsp;           counting.py

&nbsp;           validators.py



&nbsp;   examples/

&nbsp;   tests/



\## Status



Early research prototype.



The long-term goal is to provide composer-oriented functions for automatic canon generation.

