# Tool Design Examples

## Example 1: Weather Tool - From Bad to Good

### ❌ Poor Design

```python
def get_weather(location):
    """Get weather data."""
    # This fails in multiple ways:
    # - Vague description ("weather data" - what data?)
    # - No parameter documentation (what format for location?)
    # - No return description (what does it return?)
    # - No error handling (what if location doesn't exist?)
    # - No usage context (when should agent use this?)
    pass
```

**Failure modes:**
- Agent doesn't know what data it returns
- Agent unsure if it needs city name, coordinates, or ZIP code
- Agent can't recover if location is invalid
- Agent might use wrong tool for the job

### ✅ Good Design

```python
def get_weather(location: str, units: str = "celsius") -> dict:
    """
    Get current weather conditions for a location.

    Use when:
    - User asks about current weather
    - Need weather for planning decisions
    - Checking if conditions suit an activity

    Args:
        location: City name or "city, country" (e.g., "London, UK")
        units: Temperature units - "celsius" or "fahrenheit"

    Returns:
        {
            "location": "London, UK",
            "temperature": 15,
            "units": "celsius",
            "condition": "rainy",
            "humidity": 80,
            "wind_speed": 12,
            "updated_at": "2025-01-11T14:30:00Z"
        }

    Errors:
        LOCATION_NOT_FOUND: Use format "city, country" (e.g., "Paris, France")
        INVALID_UNITS: Use "celsius" or "fahrenheit"
        SERVICE_UNAVAILABLE: Weather service down, try again in 30 seconds

    Examples:
        get_weather("London, UK")
        get_weather("New York, USA", "fahrenheit")
    """
    pass
```

**Improvements:**
- Clear, specific description
- Explicit "Use when" guidance
- Parameter formats documented with examples
- Return structure documented
- Error cases explained with recovery steps
- Usage examples provided

---

## Example 2: Database Tool - Consolidation

### ❌ Without Consolidation (4 tools)

```python
def get_user(user_id: str) -> dict:
    """Get user by ID."""
    pass

def list_users(limit: int = 50) -> list:
    """List all users."""
    pass

def create_user(email: str, name: str) -> dict:
    """Create new user."""
    pass

def delete_user(user_id: str) -> bool:
    """Delete user by ID."""
    pass
```

**Problems:**
- Agent must choose between 4 tools for user operations
- Ambiguity: Is "get user info" for existing users or could it create?
- Token overhead: 4 descriptions in context
- Inconsistent patterns: Some return dict, others list/bool

### ✅ With Consolidation (1 tool)

```python
def manage_users(
    action: str,  # "get", "list", "create", "delete"
    user_id: str = None,
    email: str = None,
    name: str = None,
    limit: int = 50,
) -> dict:
    """
    Manage user database.

    Use this single tool for all user operations:
    get, list, create, delete. Replaces need for
    separate user management tools.

    Args:
        action: Operation to perform
            - "get": Retrieve user by ID (requires: user_id)
            - "list": List users (optional: limit)
            - "create": Create new user (requires: email, name)
            - "delete": Delete user (requires: user_id)
        user_id: User ID (for get/delete)
        email: User email (for create)
        name: User name (for create)
        limit: Max results for list (default 50)

    Returns:
        {
            "action": "get|list|create|delete",
            "success": true/false,
            "data": user_dict_or_list,
            "error": "error message if failed"
        }

    Errors:
        INVALID_ACTION: Use one of: get, list, create, delete
        USER_NOT_FOUND: User ID not found, use list to see valid IDs
        DUPLICATE_EMAIL: Email already exists
        MISSING_PARAMS: Action requires specific parameters

    Examples:
        manage_users("get", user_id="USER-001")
        manage_users("list", limit=100)
        manage_users("create", email="jane@example.com", name="Jane Doe")
        manage_users("delete", user_id="USER-001")
    """
    pass
```

**Improvements:**
- Single tool eliminates ambiguity
- Clear action parameter with options
- All variations documented
- Examples for each action
- Consistent return format

---

## Example 3: API Tool with Response Formats

```python
def search_products(
    query: str,
    category: str = None,
    format: str = "concise",
    limit: int = 20,
) -> dict:
    """
    Search product catalog.

    Use when:
    - User searching for specific product
    - Need product availability
    - Checking prices or specifications

    Args:
        query: Product name or keyword (min 2 characters)
        category: Filter by category (optional)
        format: Response detail level
            - "concise": ID, name, price, availability (default, saves tokens)
            - "detailed": All fields including specs, reviews, images
        limit: Max results to return (1-100, default 20)

    Returns (concise):
        {
            "results": [
                {
                    "id": "PROD-12345",
                    "name": "Product Name",
                    "price": 99.99,
                    "in_stock": true,
                    "rating": 4.5
                }
            ],
            "total": 150,
            "query": "search term"
        }

    Returns (detailed):
        {
            "results": [
                {
                    "id": "PROD-12345",
                    "name": "Product Name",
                    "category": "Electronics",
                    "price": 99.99,
                    "original_price": 129.99,
                    "discount": 0.23,
                    "in_stock": true,
                    "quantity_available": 47,
                    "rating": 4.5,
                    "review_count": 324,
                    "specifications": {...},
                    "images": [...],
                    "related_products": [...]
                }
            ],
            "total": 150,
            "query": "search term"
        }

    Guidance:
        Use format="concise" for quick product confirmation.
        Use format="detailed" when agent needs full context
        to make decisions (comparisons, recommendations).

    Errors:
        QUERY_TOO_SHORT: Query must be at least 2 characters
        CATEGORY_NOT_FOUND: Valid categories are: electronics, books, etc.
        TOO_MANY_RESULTS: Add more specific query or use limit
        INVALID_FORMAT: Use "concise" or "detailed"

    Examples:
        search_products("laptop")
        search_products("laptop", category="electronics", format="detailed")
        search_products("gaming keyboard", limit=5)
    """
    pass
```

**Improvements:**
- Response format option reduces token usage
- Clear guidance on when to use each format
- Both concise and detailed structures documented
- Examples showing format usage
- Token efficiency built in

---

## Example 4: Error Handling Excellence

```python
def transfer_money(
    from_account: str,
    to_account: str,
    amount_cents: int,
    note: str = "",
) -> dict:
    """
    Transfer money between accounts.

    Use when:
    - User wants to move funds between their accounts
    - Paying another account holder
    - Splitting costs or reimbursements

    Args:
        from_account: Account number (format: ACC-#######)
        to_account: Recipient account number (ACC-#######)
        amount_cents: Amount in cents (e.g., 5000 = $50.00)
        note: Transfer note (optional, max 100 chars)

    Returns:
        {
            "success": true,
            "transaction_id": "TXN-20250111-12345",
            "from_account": "ACC-0123456",
            "to_account": "ACC-7654321",
            "amount": 5000,
            "timestamp": "2025-01-11T14:30:00Z"
        }

    Error cases and recovery:

        INSUFFICIENT_FUNDS:
            "Transfer failed: account has $30.00, need $50.00"
            Recovery: Reduce amount_cents or add funds to account

        INVALID_ACCOUNT_FORMAT:
            "Invalid from_account 'my_account'. Use format: ACC-0123456"
            Recovery: Use get_accounts() to list valid account numbers

        ACCOUNT_NOT_FOUND:
            "to_account ACC-9999999 not found. Valid accounts: ACC-123456, ACC-789012"
            Recovery: Use correct account number from list

        TRANSFER_LIMIT_EXCEEDED:
            "Daily transfer limit is $10,000. You've transferred $7,500 today."
            Recovery: Transfer remainder tomorrow or contact support

        ACCOUNT_LOCKED:
            "from_account is locked due to suspicious activity. Contact support."
            Recovery: No recovery - user must contact support team

        INVALID_AMOUNT:
            "amount_cents must be positive. Got: -5000. Use positive value."
            Recovery: Use positive amount_cents value

    Examples:
        transfer_money("ACC-0123456", "ACC-7654321", 5000)
        transfer_money("ACC-0123456", "ACC-7654321", 5000, "Lunch reimbursement")
    """
    pass
```

**Improvements:**
- Each error case explicitly documented
- Error messages are specific and actionable
- Recovery guidance for each error type
- Some errors have suggestions (get_accounts())
- Some guide to support team when needed

---

## Example 5: Complex Tool with Nested Parameters

```python
def create_meeting(
    title: str,
    attendees: list[str],
    duration_minutes: int = 60,
    time_zone: str = "UTC",
    options: dict = None,
) -> dict:
    """
    Schedule a meeting and send invitations.

    Use when:
    - User wants to schedule meeting with others
    - Need to book time with specific attendees
    - Organizing calendar events

    Args:
        title: Meeting title (max 100 chars)
        attendees: List of email addresses to invite
        duration_minutes: Meeting length (default: 60)
        time_zone: Timezone for scheduling (default: "UTC")
            Supported: UTC, US/Eastern, US/Pacific, Europe/London, etc.
        options: Optional configuration dict
            - "reminder_minutes": Send reminder before meeting
            - "recording": Enable recording (true/false)
            - "meeting_link": Include video conference link
            - "description": Meeting description/agenda

    Returns:
        {
            "meeting_id": "MTG-20250111-12345",
            "title": "Project Review",
            "attendees": ["alice@example.com", "bob@example.com"],
            "scheduled_for": "2025-01-15T10:00:00Z",
            "duration_minutes": 60,
            "meeting_link": "https://meet.example.com/mtg123",
            "invitations_sent": 2,
            "status": "pending_responses"
        }

    Options examples:
        create_meeting(
            "Team Standup",
            ["alice@example.com", "bob@example.com"],
            duration_minutes=30,
            options={
                "reminder_minutes": 15,
                "recording": true,
                "description": "Daily standup - updates on current projects"
            }
        )

    Errors:
        INVALID_EMAIL: "alice@example is not a valid email"
        INVALID_TIMEZONE: "PST not recognized. Use format like 'US/Pacific'"
        DURATION_OUT_OF_RANGE: "duration_minutes must be 15-240 minutes"
        NO_ATTENDEES: "Must invite at least 1 attendee"
        USER_NOT_FOUND: "Attendee bob@example.com is not a valid user"
        SCHEDULING_CONFLICT: "Organizer has conflict at proposed time"
    """
    pass
```

**Improvements:**
- Complex nested options clearly documented
- Each option field explained
- Example showing options usage
- Timezone guidance provided
- Validation errors documented

---

## Example 6: Consolidation Pattern - Order Management

### ❌ Without Consolidation (6 tools)

```python
def create_order(items, customer_id):
    """Create order."""
    pass

def get_order(order_id):
    """Get order details."""
    pass

def cancel_order(order_id):
    """Cancel order."""
    pass

def refund_order(order_id):
    """Refund order."""
    pass

def update_tracking(order_id, tracking_number):
    """Update tracking."""
    pass

def get_order_history(customer_id):
    """Get customer orders."""
    pass
```

### ✅ With Consolidation (1 tool)

```python
def manage_order(
    action: str,
    order_id: str = None,
    customer_id: str = None,
    items: list = None,
    reason: str = None,
    tracking_number: str = None,
) -> dict:
    """
    Manage orders end-to-end.

    Use this single tool for all order operations:
    create, retrieve, cancel, refund, track, history.

    Args:
        action: Operation to perform
            - "create": Create new order (requires: customer_id, items)
            - "get": Retrieve order details (requires: order_id)
            - "cancel": Cancel order (requires: order_id, reason)
            - "refund": Refund order (requires: order_id)
            - "track": Update tracking (requires: order_id, tracking_number)
            - "history": Get customer order history (requires: customer_id)
        order_id: Order ID (for get, cancel, refund, track)
        customer_id: Customer ID (for create, history)
        items: List of items for order (for create)
        reason: Cancellation reason (for cancel)
        tracking_number: Tracking number (for track)

    Returns:
        Varies by action:
        - "create": New order with ID and items
        - "get": Full order details with status
        - "cancel": Confirmation of cancellation
        - "refund": Refund details with reference
        - "track": Tracking update confirmation
        - "history": List of customer orders

    Examples:
        manage_order("create", customer_id="CUST-001", items=[...])
        manage_order("get", order_id="ORD-123456")
        manage_order("cancel", order_id="ORD-123456", reason="Changed mind")
        manage_order("refund", order_id="ORD-123456")
        manage_order("track", order_id="ORD-123456", tracking_number="1Z999AA1")
        manage_order("history", customer_id="CUST-001")
    """
    pass
```

---

## Example 7: MCP Tool Naming

```python
# MCP Server Definition (server.py)
from mcp_use.server import MCPServer
import json

server = MCPServer(
    name="DatabaseServer",
    version="1.0.0",
    description="Database operations via MCP"
)

@server.tool()
def query_users(user_id: str = None, limit: int = 50):
    """
    Query users from the database.

    Use the fully qualified tool name in descriptions:
    "Use the DatabaseServer:query_users tool to find users"

    Always reference as DatabaseServer:query_users, never just query_users.
    """
    pass

@server.tool()
def create_user(email: str, name: str):
    """
    Create new user.

    Reference: DatabaseServer:create_user
    """
    pass

# Tool references in agent prompts
SYSTEM_PROMPT = """
You have access to these tools for database operations:

1. DatabaseServer:query_users - Search for users
   Use: "DatabaseServer:query_users(email='user@example.com')"

2. DatabaseServer:create_user - Create new user
   Use: "DatabaseServer:create_user(email='new@example.com', name='Jane')"

Always use fully qualified names like DatabaseServer:tool_name.
"""

# Example of correct vs incorrect

# ✅ CORRECT: Fully qualified
tools = [
    "DatabaseServer:query_users",
    "DatabaseServer:create_user",
    "FileServer:read_file",
    "FileServer:write_file",
]

# ❌ INCORRECT: Unqualified (may fail with "tool not found")
tools = [
    "query_users",
    "create_user",
    "read_file",
    "write_file",
]
```

---

## Example 8: Tool Design Anti-Pattern Fixes

### ❌ Anti-Pattern: Cryptic Names and Vague Descriptions

```python
def do_thing(x, y):
    """Manipulate data."""
    pass
```

### ✅ Fixed

```python
def update_customer_preferences(
    customer_id: str,
    preferences: dict,
) -> dict:
    """
    Update customer's notification and communication preferences.

    Use when:
    - Customer changes notification settings
    - Need to update language or regional preferences
    - Disabling/enabling communications

    Args:
        customer_id: Customer ID (format: CUST-######)
        preferences: Dict with fields:
            - "notifications": true/false
            - "email_frequency": "daily", "weekly", "never"
            - "language": "en", "es", "fr", etc.

    Returns:
        {
            "customer_id": "CUST-000001",
            "preferences": {...},
            "updated_at": "2025-01-11T14:30:00Z"
        }

    Errors:
        CUSTOMER_NOT_FOUND: Use get_customers() to find valid IDs
        INVALID_FIELD: preferences contains unknown key
        INVALID_VALUE: preferences value not allowed
    """
    pass
```

---

## Example 9: Testing Tool Design

```python
# Test: Can different agents use this tool correctly?

def test_tool_unambiguity():
    """
    Would agents consistently interpret this tool?
    """
    tool_desc = """
    Get customer information by ID.

    Args:
        customer_id: Customer ID
    """

    # Problem: What data? What format for ID?
    # Different agents might:
    # 1. Interpret "customer_id" as numeric only
    # 2. Interpret as full customer record
    # 3. Interpret as customer name
    # Result: Inconsistent usage

    fixed_tool_desc = """
    Get customer profile by ID.

    Args:
        customer_id: Customer ID (format CUST-######, e.g., CUST-000001)

    Returns:
        {
            "id": "CUST-000001",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "status": "active",
            "created_at": "2024-01-01T00:00:00Z"
        }
    """
    # Fixed: Clear format, clear return structure


def test_tool_consolidation():
    """
    Is this a minimal set of tools with no ambiguity?
    """
    # Before: 5 tools, overlapping functionality
    tools = [
        "get_user",          # Get user by ID
        "find_user",         # Find by name
        "search_users",      # Search by criteria
        "list_users",        # List all users
        "filter_users",      # Filter by role
    ]
    # Problem: Agent unsure which to use for "find users with admin role"

    # After: 1 comprehensive tool
    tools = [
        "manage_users"  # All operations with clear parameters
    ]
    # Fixed: Unambiguous - only one choice


def test_tool_recoverability():
    """
    Can agents recover from errors?
    """
    # Bad error handling
    error = "Error: invalid parameter"
    # Result: Agent cannot recover

    # Good error handling
    error = (
        "Invalid customer_id format 'john'. "
        "Use format CUST-###### (e.g., CUST-000001). "
        "Call get_customers() to list valid IDs."
    )
    # Result: Agent knows exactly what to do
```

