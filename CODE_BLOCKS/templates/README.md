# Flask Template Code Blocks

This folder contains example template blocks using Jinja2 templating in Flask. Each example demonstrates different templating patterns and best practices.

## Quick Start
1. Copy the HTML blocks you need
2. Replace variable names and content to match your needs
3. Make sure to extend base templates properly
4. Keep template logic simple - complex logic belongs in your Python code

## Files in this Directory

- `inheritance_examples.html`: Template inheritance patterns
- `form_examples.html`: Common form patterns and validation
- `loop_examples.html`: Working with loops and conditionals
- `macro_examples.html`: Reusable template components

## Important Jinja2 Syntax
- Variables: `{{ variable }}`
- Control structures: `{% if condition %}` `{% endif %}`
- Comments: `{# comment #}`
- Template inheritance: `{% extends 'base.html' %}`
- Blocks: `{% block content %}` `{% endblock %}`

## Best Practices
1. Keep logic in your Python code, not templates
2. Use template inheritance to avoid code duplication
3. Name your blocks consistently
4. Use meaningful variable names
5. Comment complex template logic

## Common Issues
1. Forgetting to pass required variables to templates
2. Incorrect block names in child templates
3. Missing endblock statements
4. Forgetting to escape user input (use |escape)