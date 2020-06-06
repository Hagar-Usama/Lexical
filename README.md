


# Lexical Analyzer

This is my third time to implement this phase. Hopefully, it is the last time ISA.
I have explored different references so far. Thus, I would say I have a complete perspective for this project.

---

## Plan (schedule)
* Today: 23 May
* Actual Deadline: 6 Jun
* Phase Deadline: 29 May

---

### Schedule:
* 23/5:  Getting to know what's going on
* (24-29)/5: * build the program (see todo)

---
### Message
It is the third time I implement this phase. I failed two times and finally
managed to implement it successfully.

I am proud of my original work. It is not the best. Yet, it is mine. And that is enough for me 😌
### Tasks

 ####  you can do it 💪 👐 ( yup I did it)
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
* [x] test the case by diffmerge tool
* [x] consider module file to add your modules in
* [x] replace state names with smaller unique names
* [x] add arguments (argparse)
* [x] consider add directory for input and directory for output
* [ ] add DFA table to Lexical (from lexical_aux)
* [ ] add Lexical to modules and run from main
* [x] report

---

### Notes:
* rd to be entered without '#'
* add '#' . directly to post-fix expression to avoid confusion
* dfa_simulate_2 is recursive it returns output in reverse order
* as you replace 'e' with its symbol, replace '(' with LBRKT and ')' RBRKT
and mind that in postfix
