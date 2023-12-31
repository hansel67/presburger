# Theorem-Prover for Presburger Arithmetic (In Progress)

## Takes as input a sentence in Presburger arithmetic and decides whether it is true or false.

References:
 * On the Completeness of a Certain System of Arithmetic of Whole Numbers in Which Addition Occurs as the Only Operation. Mojżesz Presburger. 1928
 
Working components:
 * Axioms
 * Concequences
 * Parser
 * AST Evaluator

Plan:
 * Transform input into disjunctive normal form
 * Six pairs of four types: = ≠ ≡ ≢
 * Existential quantifier elimination
 
 Possible Further Directions:
 * Depth-first search for formulas with minimum Kolmogorov complexity
 * Data analysis
 * Cooper's quantifier elimination algorithm
 * Super-exponential complexity algorithm from Fischer, Rabin 1972
 * Accompanying LaTeX file with concise proof
 * Skolem arithmetic
 * Fragments of Peano arithmetic
 * Dan Willard's self-verifying theories
 
