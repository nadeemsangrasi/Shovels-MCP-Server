---
name: tool-design
description: Design tools that agents can use effectively. Use when creating new tools for agents, debugging tool-related failures, or optimizing existing tool sets. Covers tool naming, descriptions, parameters, error handling, and agent-specific API design.
version: 1.0.0
allowed-tools: Read, Write, Edit
author: Claude Code
tags: [agents, tools, api-design, mcp, tool-optimization]
---

# Tool Design for Agents

## Overview

Design tools that agents (LLMs) can reliably use. Unlike APIs for developers, agent tools require unambiguous descriptions, clear examples, and recovery guidance. Poor tool design creates failure modes no prompt engineering can fix.

**Key insight:** If humans can't definitively choose which tool to use in a situation, agents can't either (consolidation principle).

**See:** `references/best_practices.md` for detailed guidelines

## When to Use

**Activate when:**
- "Create new tool for agent"
- "Design tool API"
- "Debug tool failures"
- "Optimize tool set"
- "Fix tool description"
- "Improve tool usability"
- "Evaluate third-party tools"

**NOT for:** Using existing tools (use directly); general API design (use API-design skill)

## Prerequisites

**Required:**
- Understanding of LLM reasoning
- Familiarity with agent frameworks (OpenAI SDK, Claude API, etc.)
- Knowledge of your target domain

**Optional:**
- MCP (Model Context Protocol) experience
- Production agent observability data

**See:** `references/setup.md` for prerequisites

## Instructions

### Phase 1: Define Tool Purpose

**Identify the workflow:**
```
What single workflow should this tool accomplish?
(Not: multiple steps agents must chain)
```

**Use consolidation principle:**
```python
# Poor: 3 separate tools
get_user()           # Retrieves user
get_permissions()    # Gets permissions
check_access()       # Checks access

# Better: 1 comprehensive tool
authorize_user(user_id, action)  # Determines access in one call
```

**Validation:**
- Can you explain the workflow in 1 sentence?
- Would a human ask for 1 or multiple tools?

**See:** `references/examples.md#consolidation`

### Phase 2: Design Parameters

**Clear parameter names:**
```python
# Good: Verb-noun pattern
create_issue(title, description, labels)
update_user(user_id, fields_to_update)
get_customer(customer_id, format)

# Poor: Cryptic names
do_thing(x, y, z)
process(val, param1, param2)
```

**Add constraints & defaults:**
```python
def schedule_meeting(
    title: str,              # Meeting title (max 100 chars)
    attendees: list[str],    # Email addresses
    duration_minutes: int = 60,  # Default 1 hour
    time_zone: str = "UTC",     # Default UTC
):
    """Schedule a meeting."""
```

**Validation:**
- Can agent understand each parameter without documentation?
- Are constraints explicit?
- Do defaults match common cases?

**See:** `references/parameter-design.md`

### Phase 3: Write Effective Descriptions

**Answer 4 questions:**

**What:** Clear, specific functionality
```python
def get_customer(customer_id: str) -> dict:
    """
    Retrieve full customer profile including contact info,
    purchase history, and account status.
    """
```

**When:** Usage triggers and context
```python
    """
    Retrieve full customer profile...

    Use when:
    - User asks about specific customer
    - Need customer context for decision
    - Verifying customer identity
    """
```

**Inputs:** Parameter guidance
```python
    """
    ...
    Args:
        customer_id: Format "CUST-######" (e.g., "CUST-000001")
    """
```

**Returns:** Output structure
```python
    """
    ...
    Returns:
        dict with: id, name, email, phone, created_at, status,
        purchase_count, last_purchase
    """
```

**Validation:**
- Does description answer all 4 questions?
- Is it under 200 words?
- Does it include an example?

**See:** `references/descriptions.md`

### Phase 4: Handle Errors

**Error messages guide recovery:**
```python
def transfer_funds(account_id: str, amount: float):
    """Transfer funds from account."""

    if not account_exists(account_id):
        raise ValueError(
            f"Account {account_id} not found. "
            f"Use get_accounts() to list valid accounts."
        )

    if amount <= 0:
        raise ValueError(
            f"Amount must be positive. Got: {amount}. "
            f"Use format: transfer_funds(id, 100.50)"
        )
```

**Include:**
- What went wrong (specific, not generic)
- How to fix it (actionable suggestion)
- Valid alternatives (if applicable)

**Validation:**
- Can agent recover from error message?
- Is suggestion clear?

**See:** `references/error-handling.md`

### Phase 5: Optimize Response Format

**Control token usage:**
```python
def get_user(user_id: str, format: str = "concise") -> dict:
    """
    Get user information.

    Args:
        format: "concise" (key fields only) or "detailed" (all fields)
    """
    if format == "concise":
        return {"id": user.id, "name": user.name, "email": user.email}
    else:
        return user.to_dict()
```

**Guidance in description:**
```
Use format="concise" for quick confirmation.
Use format="detailed" when making complex decisions.
```

**Validation:**
- Does concise format omit unnecessary fields?
- Does detailed format include everything agent might need?

**See:** `references/response-formats.md`

### Phase 6: Test Tool Design

**Evaluate against criteria:**

**Unambiguity:** Would different agents interpret tool the same way?
```python
# Test: What would agent do?
# Tool: "Get customer data"
# Agent: Unsure - get all fields? Just profile? Purchase history?
```

**Completeness:** Does tool handle realistic workflows?
```python
# Test: Complete workflow?
# get_customer() -> check_limits() -> approve_discount()
# Better: approve_discount(customer_id) -> handles limits internally
```

**Recoverability:** Can agent recover from errors?
```python
# Test: If tool fails, what does agent do?
# Bad error: "Error: invalid input"
# Good error: "Amount exceeds limit of $5000. Use smaller amount."
```

**Efficiency:** Does tool minimize token usage?
```python
# Test: Tokens needed?
# 10 separate tools = 10 descriptions
# 1 comprehensive tool = 1 description (consolidation)
```

**Consistency:** Do tool names/patterns match others?
```python
# Consistent:
create_issue(), create_user(), create_comment()
get_issue(), get_user(), get_comment()

# Inconsistent:
create_issue(), fetch_user(), retrieve_comment()
```

**See:** `references/testing.md`

### Phase 7: Document Tool Behavior

**Create tool reference:**
```python
"""
get_customer(customer_id, format="concise") -> dict

Retrieve customer profile by ID.

Args:
    customer_id: CUST-###### format
    format: "concise" or "detailed"

Returns:
    {"id", "name", "email", "status", "created_at", ...}

Errors:
    NOT_FOUND: Use get_accounts() to list valid IDs
    INVALID_FORMAT: Use format "CUST-000001"
    RATE_LIMIT: Try again in 60 seconds

Examples:
    get_customer("CUST-000001", "concise")
    # Returns: {"id": "CUST-000001", "name": "Jane Doe", ...}
"""
```

**See:** `references/tool-reference-template.md`

### Phase 8: Implement MCP Naming (Optional)

**If using MCP servers, use fully qualified names:**
```python
# Tool definition in MCP server
# Correct: Include server prefix
"tools": [
    {"name": "BigQuery:execute_query", ...},
    {"name": "GitHub:create_issue", ...},
    {"name": "Slack:send_message", ...},
]

# In descriptions and examples
"""
Use the BigQuery:execute_query tool to run SQL queries.
Use the GitHub:create_issue tool to create issues.
"""

# Incorrect: Unqualified names (may cause "tool not found")
"tools": [
    {"name": "execute_query", ...},
    {"name": "create_issue", ...},
]
```

**Validation:**
- All tool references include server prefix
- Format: `ServerName:tool_name`
- Names match exactly (case-sensitive)

**See:** `references/mcp-naming.md`

## Common Patterns

### Pattern 1: Parameter Defaults
```python
def search_customers(
    query: str,
    limit: int = 20,
    offset: int = 0,
    sort: str = "relevance",
):
    """Search customers. Defaults to 20 results, relevance sort."""
```

**See:** `references/examples.md#defaults`

### Pattern 2: Enum Choices
```python
def update_order_status(order_id: str, status: str):
    """
    Update order status.

    Args:
        status: One of: "pending", "processing", "shipped", "delivered"
    """
```

**See:** `references/examples.md#enums`

### Pattern 3: Optional Parameters
```python
def create_user(
    email: str,
    name: str,
    role: str = "user",
    department: str = None,  # Optional
):
    """Create user. Department is optional."""
```

**See:** `references/examples.md#optional`

### Pattern 4: Nested Objects
```python
def transfer_funds(
    from_account: str,
    to_account: str,
    amount: float,
    metadata: dict = None,  # Optional metadata
):
    """
    Transfer funds between accounts.

    Args:
        metadata: Optional dict with keys: reference, notes, category
    """
```

**See:** `references/examples.md#nested`

### Pattern 5: Consolidation
```python
# Instead of separate tools
list_users()
filter_users(role="admin")
count_active_users()
get_user_permissions(user_id)

# Create comprehensive tool
def find_users(
    role: str = None,
    status: str = "active",
    include_permissions: bool = False,
) -> dict:
    """
    Find users with filters.

    Args:
        role: Filter by role (admin, user, guest)
        status: active or inactive
        include_permissions: Add permission data
    """
```

**See:** `references/examples.md#consolidation`

## Error Handling

| Error | Solution |
|-------|----------|
| Tool not found | Check MCP naming: `ServerName:tool_name` |
| Wrong parameters | Provide usage example in description |
| Ambiguous purpose | Split into multiple tools or clarify context |
| Agent misuses tool | Improve error messages with recovery steps |
| Inconsistent naming | Adopt consistent naming convention |
| Too many tools | Apply consolidation principle |
| Token overflow | Implement response format options |
| Missing defaults | Add sensible defaults for common cases |

**See:** `references/troubleshooting.md`

## Decision Trees

### Single vs. Multiple Tools?
```
Does every agent request map to one tool? → Yes → Single tool
                                          → No → Multiple tools

If multiple: Can agents confuse which to use? → Yes → Consolidate
                                               → No → Keep separate
```

### Parameter Required or Optional?
```
Always needed for tool to work? → Yes → Required
                                → No → Optional with default

Can you choose sensible default? → Yes → Add default
                                 → No → Keep required
```

### Response: Concise or Detailed?
```
Will agent always need all fields? → Yes → Detailed only
                                   → No → Offer both

Can context budget spare fields? → Yes → Include detailed
                                 → No → Concise only
```

## Anti-Patterns to Avoid

```python
# ❌ Anti-Pattern 1: Vague descriptions
def search(query):
    """Search the database."""

# ✅ Better
def search_customers(query: str, limit: int = 20):
    """
    Search customers by name or email.

    Args:
        query: Name or email fragment (min 2 chars)
        limit: Max results (1-100, default 20)
    """

# ❌ Anti-Pattern 2: Cryptic parameter names
def process(x, y, z):
    pass

# ✅ Better
def transfer_funds(source_account_id: str, destination_account_id: str, amount_cents: int):
    pass

# ❌ Anti-Pattern 3: No error handling
def get_user(user_id):
    return database.get(user_id)

# ✅ Better
def get_user(user_id: str):
    """Get user by ID."""
    user = database.get(user_id)
    if not user:
        raise ValueError(
            f"User {user_id} not found. "
            f"Call list_users() to see available IDs."
        )
    return user

# ❌ Anti-Pattern 4: Too many similar tools
list_users()
get_user(id)
search_users(query)
filter_users(role)
count_users()

# ✅ Better
def find_users(
    query: str = None,
    role: str = None,
    include_count: bool = False,
):
    """
    Find users with optional filters.

    Args:
        query: Search by name/email
        role: Filter by role
        include_count: Add total count to response
    """
```

**See:** `references/anti-patterns.md`

## References

**Local Documentation:**
- Best practices: `references/best_practices.md`
- Parameter design: `references/parameter-design.md`
- Descriptions: `references/descriptions.md`
- Error handling: `references/error-handling.md`
- Response formats: `references/response-formats.md`
- Testing: `references/testing.md`
- Examples: `references/examples.md`
- Troubleshooting: `references/troubleshooting.md`
- MCP naming: `references/mcp-naming.md`

**External Resources:**
- MCP specification: https://modelcontextprotocol.io
- Claude API tools: https://docs.anthropic.com
- OpenAI function calling: https://platform.openai.com

## Tips for Success

1. **Apply consolidation principle** - Reduce tool count, eliminate ambiguity
2. **Write descriptions for agents, not developers** - Include context and examples
3. **Design error messages for recovery** - Tell agents what's wrong and how to fix it
4. **Test with actual agent interactions** - Observe real failure modes
5. **Use consistent naming patterns** - Reduce cognitive load
6. **Provide sensible defaults** - Minimize parameter burden
7. **Implement response formats** - Give agents control over token usage
8. **Document error cases** - Help agents understand boundaries
9. **Use MCP fully qualified names** - Avoid "tool not found" errors
10. **Iterate based on failures** - Use observability data to improve

**See:** `references/best_practices.md#checklist`
