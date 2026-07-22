# Skill Template Reference

This document provides a complete template for creating Claude Code skills with all recommended sections and best practices.

## Complete SKILL.md Template

```markdown
---
name: skill-name
description: Brief description of what this skill does and when to use it. Include specific trigger keywords.
version: 1.0.0
allowed-tools: Bash, Read, Write
author: Your Name
tags: [category1, category2]
---

# Skill Title

## Overview

Brief explanation of what this skill accomplishes and its primary purpose.

## When to Use This Skill

- Specific trigger condition 1
- Specific trigger condition 2
- Specific trigger condition 3
- When the user mentions [specific keywords]

## Prerequisites

### Required Setup
- Required tool or dependency 1
- Required tool or dependency 2
- Required access or permissions

### Optional Dependencies
- Optional tool 1 (what it enables)
- Optional tool 2 (what it enables)

## Instructions

### Step 1: [Phase Name - Preparation]

1. **Action Name**: Clear action to take
   - Specific detail or command
   - Expected outcome

2. **Verification**: How to confirm step 1 worked
   - Success criteria
   - What to check

### Step 2: [Phase Name - Execution]

1. **Main Action**: Primary task to perform
   ```bash
   # Example command
   command --option value --flag
   ```

   Expected output:
   ```
   Success message or result
   ```

2. **Process Results**: What to do with output
   - How to interpret results
   - Next steps based on outcome

### Step 3: [Phase Name - Validation]

1. **Verify Success**: Check task completed correctly
   - Success indicator 1
   - Success indicator 2

2. **Handle Errors**: If something fails
   - Error pattern 1 and solution
   - Error pattern 2 and solution

### Step 4: [Phase Name - Completion]

1. **Finalize**: Complete the task
   - Cleanup steps if needed
   - Final actions

2. **Document**: Record results
   - What to report to user
   - Success message format

## Examples

### Example 1: [Basic Use Case Name]

**Scenario**: Describe the specific situation

**Input:**
```
Example input or starting state
```

**Process:**
1. Step one of execution
2. Step two of execution
3. Step three of execution

**Output:**
```
Expected result or final state
```

### Example 2: [Advanced Use Case Name]

**Scenario**: Describe more complex situation

**Input:**
```
Example input for advanced scenario
```

**Process:**
1. Advanced step one
2. Advanced step two with options
3. Conditional logic based on results

**Output:**
```
Expected result with additional details
```

### Example 3: [Edge Case Name]

**Scenario**: Describe edge case or special handling

**Input:**
```
Edge case input
```

**Handling:**
- How this differs from normal case
- Special steps required
- Additional validation

**Output:**
```
Expected result for edge case
```

## Error Handling

### Error: [Common Error 1 Name]

```
Error message or symptom
```

**Cause:** Why this error occurs

**Solution:**
1. Diagnostic step
2. Fix action
3. Verification step

**Prevention:** How to avoid in future

### Error: [Common Error 2 Name]

```
Another error message
```

**Cause:** Root cause explanation

**Solution:**
1. Identification step
2. Resolution steps
3. Confirmation

**Prevention:** Preventive measures

### Error: [Common Error 3 Name]

```
Third error pattern
```

**Cause:** What triggers this

**Solution:**
- Quick fix approach
- Alternative solution if first fails

## Limitations

### What This Skill Cannot Do

- Limitation 1: Explain scope boundary
- Limitation 2: Technical constraint
- Limitation 3: Environmental requirement
- Limitation 4: Known edge case not handled

### Known Constraints

- Constraint 1: Specific limitation detail
- Constraint 2: Dependency requirement
- Constraint 3: Performance or scale limit

### Future Enhancements

- Potential improvement 1
- Potential improvement 2

## Validation Checklist

Before completing the task, verify:

- [ ] Requirement 1 is met
- [ ] Requirement 2 is satisfied
- [ ] Output format is correct
- [ ] No errors are present
- [ ] Results are as expected
- [ ] Documentation is complete

## References

### Internal Files
- Detailed guide: `references/detailed-guide.md`
- API documentation: `references/api-reference.md`
- Extended examples: `references/examples.md`
- Configuration: `references/config-options.md`

### Scripts
- Main processor: `scripts/process.py`
- Validator: `scripts/validate.py`
- Helper utilities: `scripts/utils.py`

### External Resources
- Official documentation: [URL]
- Related tools: [URL]
- Community resources: [URL]

## Tips for Success

### Best Practice 1: [Practice Name]

Explain a key best practice for using this skill effectively. Include:
- Why it matters
- How to apply it
- Common pitfalls to avoid

### Best Practice 2: [Practice Name]

Another important tip for optimal results. Include:
- Specific guidance
- Examples of good vs bad approach
- Expected benefits

### Best Practice 3: [Practice Name]

Additional guidance for success. Include:
- Contextual advice
- When to apply this practice
- How to measure success

## Advanced Usage

### Pattern 1: [Advanced Pattern Name]

Description of advanced usage pattern

**When to use:**
- Situation 1
- Situation 2

**Implementation:**
```bash
# Advanced command example
complex-command --advanced-flag
```

**Considerations:**
- Trade-off 1
- Trade-off 2

### Pattern 2: [Integration Pattern]

How to combine this skill with other workflows

**Integration points:**
- Integration 1
- Integration 2

**Example workflow:**
1. Step from other skill
2. Use this skill
3. Continue to next skill

## Troubleshooting

### Issue: [Common Issue 1]

**Symptoms:**
- Symptom 1
- Symptom 2

**Diagnosis:**
1. Check condition 1
2. Verify setting 2
3. Inspect output 3

**Resolution:**
- Solution approach 1
- Alternative solution 2

### Issue: [Common Issue 2]

**Symptoms:**
- Observable behavior

**Quick Fix:**
```bash
# Command to resolve
fix-command --option
```

**Long-term Fix:**
- Configuration change
- Process improvement

## Version History

### v1.0.0 (YYYY-MM-DD)
- Initial release
- Core functionality
- Basic validation
- Example documentation

### v0.9.0 (YYYY-MM-DD)
- Beta release
- Testing phase features
- Known issues from testing
```

## Section Guidelines

### Overview Section
- 2-3 sentences
- State purpose clearly
- Mention primary benefit

### When to Use Section
- 3-5 bullet points
- Use specific trigger keywords
- Include user language (what they would say)

### Prerequisites Section
- List specific requirements
- Include version numbers if relevant
- Distinguish required from optional

### Instructions Section
- Use numbered steps for sequence
- Include code blocks with examples
- Show expected outputs
- Add verification steps

### Examples Section
- Minimum 2 examples (basic + advanced)
- Use real-world scenarios
- Show complete input → output
- Include explanatory process steps

### Error Handling Section
- Cover 3-5 common errors
- Include error messages
- Provide diagnostic steps
- Give clear solutions

### Limitations Section
- Be explicit about what's not supported
- Mention technical constraints
- List edge cases
- Set appropriate expectations

## Best Practices for Each Section

### Writing Clear Instructions

**DO:**
- Use imperative mood ("Run command" not "You should run")
- Number sequential steps
- Include concrete examples
- Show expected outputs
- Add validation checkpoints

**DON'T:**
- Use vague language ("might", "should", "try to")
- Skip error handling
- Assume prior knowledge
- Leave steps ambiguous

### Creating Helpful Examples

**DO:**
- Use realistic scenarios
- Show complete workflows
- Include explanations
- Cover different use cases
- Demonstrate best practices

**DON'T:**
- Use placeholder values without explanation
- Skip intermediate steps
- Show only success cases
- Make examples too abstract

### Documenting Errors

**DO:**
- Include actual error messages
- Explain root causes
- Provide step-by-step solutions
- Add prevention tips

**DON'T:**
- Just list error types
- Assume users can debug
- Skip verification steps
- Omit common errors

## Template Variations

### Minimal Template (Simple Skills)

For skills without scripts or complex logic:

```markdown
---
name: skill-name
description: Brief description with triggers
---

# Skill Name

## Overview
Brief explanation

## When to Use
- Trigger 1
- Trigger 2

## Instructions
1. Step one
2. Step two
3. Step three

## Examples
### Example 1
Input → Process → Output

## Error Handling
- Error 1 and solution
- Error 2 and solution
```

### Complete Template (Complex Skills)

Use the full template above for skills with:
- Multiple scripts
- Complex workflows
- Conditional logic
- External dependencies
- Advanced usage patterns

### Script-Heavy Template

For skills that primarily use automation:

```markdown
# Focus on:
- Clear script documentation
- Input/output specifications
- Error codes and meanings
- Script dependencies
- Configuration options
```

## Customization Guidelines

Adapt the template based on:

1. **Skill Complexity**
   - Simple: Use minimal template
   - Complex: Use complete template
   - Script-based: Emphasize script documentation

2. **Target Audience**
   - Beginners: More explanation, simpler examples
   - Advanced: Focus on patterns, trade-offs
   - Mixed: Separate basic and advanced sections

3. **Domain Specificity**
   - Technical: Include technical details, APIs
   - Business: Focus on workflows, decisions
   - Creative: Emphasize flexibility, variations

4. **Tool Requirements**
   - Read-only: Emphasize analysis patterns
   - Full access: Document safety measures
   - Script-heavy: Detail automation flows
