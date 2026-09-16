# Debug Lab Solution: Obfuscation Blindness Bug

### The Defect
`BrokenScanner` checks only a literal string, completely failing against Base64 encoding or regex variations.

### The Fix
Implement Base64 extraction, normalization, and regex rule matching as shown in `project_solution/adversarial_detector.py`.
