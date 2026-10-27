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