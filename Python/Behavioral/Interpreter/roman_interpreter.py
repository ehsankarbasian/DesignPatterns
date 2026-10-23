"""
TODO: Implement a natural language query processor for the Merchant's Guide galactic trading system.

Problem Statement:
Commodity trading across the galaxy requires converting intergalactic transaction statements into decimal credit values.
Alien transaction records use local alien numerals mapped to Roman numerals, commodities with inferred unit values, and queries requesting numeric or credit totals.
The system must parse assignments, compute commodity credit values, answer queries, and identify invalid inputs cleanly.

Domain Requirements:
- Map alien numeral words to Roman symbols (e.g., glob is I, prok is V, pish is X, tegj is L).
- Convert alien numeral sequences to decimal values by resolving them to Roman numerals and applying standard arithmetic rules.
- Enforce Roman numeral validation rules:
  - Symbols I, X, C, and M may be repeated at most three times consecutively.
  - Symbols D, L, and V can never be repeated.
  - Subtraction rules: I can subtract from V and X; X can subtract from L and C; C can subtract from D and M; V, L, and D can never subtract.
  - Only one smaller symbol may precede a larger symbol (e.g., IV is valid, IIV is invalid).
- Infer fractional or whole unit credit prices for commodities (e.g., Silver, Gold, Iron) from total transaction statements.
- Process input queries to calculate numeric values ("how much is ... ?") and credit values ("how many Credits is ... ?").
- Return "I have no idea what you are talking about" for any unparsable or malformed input line.
- Provide clean architectural separation between token parsing, Roman conversion, pricing calculations, and query dispatching.
"""
