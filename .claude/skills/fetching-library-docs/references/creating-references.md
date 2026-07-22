# Creating Reference Files

## Purpose

Reference files store documentation patterns for future use, creating a knowledge base that improves over time.

## Structure

```
.claude/skills/library-name/
├── SKILL.md                    # Main skill (optional)
├── README.md                   # Overview
└── references/
    ├── installation.md         # Setup
    ├── usage.md                # Basic usage
    ├── examples.md             # Code examples
    ├── patterns.md             # Common patterns
    └── troubleshooting.md       # Known issues
```

## Creating a Reference File

### Template

```markdown
# Library Feature Reference

## Source Information
- **Context7 ID:** /org/project
- **Query:** Your original query
- **Date Retrieved:** YYYY-MM-DD
- **Version:** Optional version info

## Overview
Brief description of what this reference covers.

## Key Concepts
- Concept 1: Description
- Concept 2: Description

## Code Examples

### Basic Example
```language
// Code from documentation
code here
```

### Advanced Example
```language
// More complex example
code here
```

## Usage Notes
- Note 1
- Note 2

## Related
- Link to related references
- Link to official docs
```

## Example: React useEffect Reference

```markdown
# React useEffect Reference

## Source
- Context7 ID: /facebook/react
- Query: "React useEffect cleanup function examples"
- Date: 2024-01-15

## Overview
Using useEffect with cleanup to prevent memory leaks and race conditions.

## Key Concepts
- Cleanup function runs before component unmounts
- Cleanup runs before effect re-runs
- Return undefined vs return function

## Code Examples

### Basic with Cleanup
```tsx
useEffect(() => {
  const subscription = subscribe(data);

  // Cleanup function
  return () => {
    subscription.unsubscribe();
  };
}, [data]);
```

### Fetch with AbortController
```tsx
useEffect(() => {
  const controller = new AbortController();
  const { signal } = controller;

  fetch(url, { signal })
    .then(response => response.json())
    .then(data => setData(data))
    .catch(err => {
      if (err.name !== 'AbortError') {
        console.error(err);
      }
    });

  return () => controller.abort();
}, [url]);
```

## Usage Notes
- Always return cleanup function for subscriptions
- Use AbortController for fetch requests
- Dependencies array controls re-run frequency
```

## Updating References

When new documentation is fetched:

1. **Review** new information
2. **Compare** with existing reference
3. **Update** if new patterns are better
4. **Version** if significant changes

```markdown
## Version History
- v1.0 (2024-01-15): Initial reference
- v1.1 (2024-02-01): Added AbortController pattern
```

## Organizing References

### By Feature
```
references/
├── hooks/
│   ├── useState.md
│   ├── useEffect.md
│   └── useContext.md
├── components/
│   ├── forwardRef.md
│   └── memo.md
└── patterns/
    ├── state-management.md
    └── performance.md
```

### By Use Case
```
references/
├── authentication.md
├── data-fetching.md
├── forms.md
└── routing.md
```

## Best Practices

1. **Include source** - Always link to Context7
2. **Add dates** - Track when information was retrieved
3. **Use code blocks** - Copy-paste ready examples
4. **Document variations** - Different approaches
5. **Add troubleshooting** - Common issues
6. **Version references** - Track updates
