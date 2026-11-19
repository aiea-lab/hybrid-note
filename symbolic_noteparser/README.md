# AIEA Symbolic Note Parser

This is a research prototype for converting symbolic structures in handwritten notes into machine-readable representations. 

This project explores whether LLM models can accurately identify note-taking structures such as bullets, arrows, equations, circles, boxes, sketches, and other elemets and represent them using structured JSON. 

## Current Prototype

The current pipeline is: 

Handwritten Note --> LLM --> Structured JSON --> Python Schema Validator

To extract the symbolic structures from the handwritten notes, I have used Claude. The generated JSON is then validated using a Python script to check if it follows the defined schema. 

## Symbol Types 

The parser is currently based on the following symbol types: 
- Bullet
- Numbered List
- Checkbox
- Arrow
- Date
- Highlight
- Underline
- Box
- Sketch
- Equation
- Circle
- Table
- Graph/Chart
- Star/Exclamation 

## Run the sample validator

From the root of the `hybrid-note` repository, run:

```bash
cd symbolic_noteparser
python3 parser.py
```

The script needs only Python 3. It reads five saved JSON files in
`outputs/raw/`, one for each sample page from 10 to 14. Claude generated
these files from handwritten note images in a separate step.

The script writes one report per page to `outputs/validation/`. All five
samples should report `No errors found.` Page 14 also reports a warning
about a duplicate arrow whose connections are already recorded.