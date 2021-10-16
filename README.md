


# Lexical Analyzer

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com)


Lexical Analyzer is the first phase of my compiler (Genepiler). It's planned to join my _'Oh My Compiler'_ project!

This phase converts the source code (based on the lexical file) into tokens, to be processed later in the second phase - [parser-generator](https://github.com/Hagar-Usama/parser-generator)

---

## [Memory] Plan (schedule) 
* Today: 23 May 2020
* Actual Deadline: 6 Jun 2020
* Phase Deadline: 29 May 2020
  
  ### Schedule:
* 23/5:  Getting to know what's going on
* (24-29)/5: Build the program (see todo)

---

## Tasks

* [x] input to RD
* [x] add concat to RD (needs improvement)[done]
* [x] RD to prefix
* [x] node
* [x] build AST tree
* [x] show tree
* [x] get nullable
* [x] get firstpos
* [x] get lastpos
* [x] get followpos
* [x] RD to DFA
* [x] Simulate DFA
* [x] make unique id for leaves only (expect for epsilon)
* [x] add + and ? to Regex
* [ ] Minimize DFA (algorithm already minimize it (lex algorithm))
* [x] add RE nodes to RD tree
* [x] append keywords and punctuation
* [x] format input code
* [x] make sub DFAs for each RD
* [x] subs REs in RDs
* [x] sep REs
* [x] sep keywords    (not really)
* [x] sep punctuation (not really)
* [x] tabulate DFA table
* [x] test the given test cases by diffmerge tool
* [x] consider module file to add your modules in
* [x] replace state names with smaller unique names
* [x] add arguments (argparse)
* [x] consider adding directory for input and directory for output
* [ ] add DFA table to Lexical (from lexical_aux)
* [ ] add Lexical to modules and run from main
* [x] report

### New Tasks:
* [ ] Enhance the lexical file format

---

## Notes (related to internal structure):
* rd to be entered without '#'
* add '#' . directly to post-fix expression to avoid confusion
* dfa_simulate_2 is recursive it returns output in reverse order
* as you replace 'e' with its symbol, replace '(' with LBRKT and ')' RBRKT
and mind that in postfix
