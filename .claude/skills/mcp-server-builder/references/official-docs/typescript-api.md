# MCP Server API Reference (TypeScript)

## MCPServer Class

### Constructor

```typescript
import { MCPServer } from "mcp-use/server";

const server = new MCPServer({
  name: string,                    // Required - Server name
  version: string,                 // Required - Server version (semver)
  description?: string,              // Optional - Server description
  host?: string,                   // Optional - Hostname (default: 'localhost')
  baseUrl?: string,                 // Optional - Full base URL
  allowedOrigins?: string[],         // Optional - Allowed origins for CSP
  sessionIdleTimeoutMs?: number,     // Optional - Session timeout (default: 300000)
  autoCreateSessionOnInvalidId?: boolean, // Optional - Auto-create session (default: true)
});
```

**Examples:**

```typescript
// Basic
const server = new MCPServer({
  name: 'my-server',
  version: '1.0.0',
  description: 'My MCP server',
});

// With custom host
const server = new MCPServer({
  name: 'my-server',
  version: '1.0.0',
  host: '0.0.0.0',  // or 'myserver.com'
});

// With base URL (production)
const server = new MCPServer({
  name: 'my-server',
  version: '1.0.0',
  baseUrl: process.env.MCP_URL || 'http://localhost:3000',
});

// With allowed origins
const server = new MCPServer({
  name: 'my-server',
  version: '1.0.0',
  allowedOrigins: [
    'https://myapp.com',
    'https://app.myapp.com',
  ],
});
```

---

## MCP Protocol Methods

### tool()

Register a tool with the server.

```typescript
server.tool(
  definition: ToolDefinition,
  handler: ToolHandler,
): this;
```

**ToolDefinition:**
```typescript
interface ToolDefinition {
  name: string;
  description?: string;
  schema: z.ZodSchema;
}
```

**ToolHandler:**
```typescript
type ToolHandler = (args: z.infer<ZodSchema>) => Promise<ToolResponse>;
```

**ToolResponse:**
```typescript
import { text, object, mix } from "mcp-use/server";

text("string response")
object({ key: "value" })
mix(text("message"), object({ data: "value" }))
```

**Example:**
```typescript
import { z } from "zod";
import { text, object } from "mcp-use/server";

server.tool({
  name: "greet",
  description: "Greet someone by name",
  schema: z.object({
    name: z.string().describe("Person's name"),
  }),
}, async ({ name }) =>
  text(`Hello, ${name}!`)
);

server.tool({
  name: "get-user",
  description: "Get user by ID",
  schema: z.object({
    id: z.string().uuid(),
  }),
}, async ({ id }) =>
  object({ id, name: "John", email: "john@example.com" })
);
```

---

### resource()

Register a resource with the server.

```typescript
server.resource(
  definition: ResourceDefinition,
  handler: ResourceHandler,
): this;
```

**ResourceDefinition:**
```typescript
interface ResourceDefinition {
  name: string;
  uri?: string;
  description?: string;
}
```

**ResourceHandler:**
```typescript
type ResourceHandler = () => Promise<ResourceResponse>;
```

**ResourceResponse:**
```typescript
import { object } from "mcp-use/server";

object({ key: "value" })
```

**Example:**
```typescript
import { object } from "mcp-use/server";

server.resource({
  name: "config",
  uri: "config://settings",
  description: "Server configuration",
}, async () =>
  object({
    version: "1.0.0",
    environment: "production",
  })
);

server.resource({
  name: "user-info",
  description: "Current user information",
}, async () => {
  const user = await getCurrentUser();
  return object({
    id: user.id,
    name: user.name,
    email: user.email,
  });
});
```

---

### resourceTemplate()

Register a resource template with parameters.

```typescript
server.resourceTemplate(
  definition: ResourceTemplateDefinition,
  handler: ResourceTemplateHandler,
): this;
```

**ResourceTemplateDefinition:**
```typescript
interface ResourceTemplateDefinition {
  uriTemplate: string;  // e.g., "file://{path}"
  name: string;
  description?: string;
  mimeType?: string;
}
```

**ResourceTemplateHandler:**
```typescript
type ResourceTemplateHandler = (params: Record<string, string>) =>
  Promise<ResourceResponse>;
```

**Example:**
```typescript
server.resourceTemplate({
  uriTemplate: "file://{path}",
  name: "file",
  description: "Read a file from the filesystem",
  mimeType: "text/plain",
}, async ({ path }) => {
  const content = await fs.readFile(path, "utf-8");
  return object({ path, content });
});
```

---

### prompt()

Register a prompt with the server.

```typescript
server.prompt(
  definition: PromptDefinition,
  handler: PromptHandler,
): this;
```

**PromptDefinition:**
```typescript
interface PromptDefinition {
  name: string;
  description?: string;
  arguments?: PromptArgument[];
}

interface PromptArgument {
  name: string;
  description?: string;
  required?: boolean;
}
```

**PromptHandler:**
```typescript
type PromptHandler = (args: Record<string, string>) =>
  Promise<PromptResponse>;
```

**Example:**
```typescript
server.prompt({
  name: "code-review",
  description: "Generate a code review prompt",
  arguments: [
    {
      name: "language",
      description: "Programming language",
      required: true,
    },
  ],
}, async ({ language }) =>
  text(`Review the following ${language} code for issues:\n\n{{code}}`)
);
```

---

### uiResource()

Register a UI resource (widget) for the server.

```typescript
server.uiResource(
  definition: UIResourceDefinition,
  handler: UIResourceHandler,
): this;
```

**Example:**
```typescript
server.uiResource({
  name: "display-weather",
  uri: "widget://weather",
  description: "Display weather widget",
}, async () => ({
  type: "widget",
  widget: "weather-display",
  props: { city: "San Francisco" },
}));
```

---

## Server Methods

### listen()

Start the server and listen for connections.

```typescript
server.listen(port?: number): Promise<void>;
```

**Example:**
```typescript
// Default port
await server.listen();

// Custom port
await server.listen(3000);

console.log("Server running on port 3000");
```

---

## HTTP Proxy Methods

MCPServer acts as a proxy to Hono/Express, providing access to HTTP methods.

### get()

```typescript
server.get(path: string, handler: Handler): this;
```

**Example:**
```typescript
server.get("/health", (c) => {
  return c.json({ status: "ok" });
});
```

### post()

```typescript
server.post(path: string, handler: Handler): this;
```

**Example:**
```typescript
server.post("/webhook", async (c) => {
  const body = await c.req.json();
  // Process webhook
  return c.json({ received: true });
});
```

### use()

```typescript
server.use(middleware: Middleware): this;
```

**Example:**
```typescript
server.use(async (c, next) => {
  console.log(`${c.req.method} ${c.req.url}`);
  await next();
});
```

### static()

```typescript
server.static(path: string, root: string): this;
```

**Example:**
```typescript
server.static("/assets", "./public");
```

---

## Return Types

### text()

Return plain text response.

```typescript
import { text } from "mcp-use/server";

text("Hello, world!")
```

### object()

Return JSON object response.

```typescript
import { object } from "mcp-use/server";

object({
  name: "John",
  age: 30,
  active: true,
})
```

### mix()

Return mixed response with text and object.

```typescript
import { mix, text, object } from "mcp-use/server";

mix(
  text("Here's the data:"),
  object({ result: "success", value: 42 })
)
```

---

## Zod Schemas

### Common Types

```typescript
import { z } from "zod";

// String
z.string().describe("A string value")

// Number
z.number().min(0).max(100).describe("A number between 0-100")

// Boolean
z.boolean().describe("A boolean flag")

// Enum
z.enum(["option1", "option2", "option3"])

// Array
z.array(z.string())

// Object
z.object({
  name: z.string(),
  age: z.number(),
  email: z.string().email().optional(),
})

// Union
z.union([z.string(), z.number()])

// Literal
z.literal("value")

// Date
z.coerce.date()
```

### Validation

```typescript
// Email validation
z.string().email("Invalid email address")

// URL validation
z.string().url("Invalid URL")

// Regex validation
z.string().regex(/^[a-z]+$/, "Only lowercase letters allowed")

// Length validation
z.string().min(5).max(100)

// Transform
z.string().transform(val => val.toLowerCase())

// Refine
z.number().refine(
  val => val % 2 === 0,
  "Must be even number"
)
```

---

## Configuration Options

### ServerConfig

```typescript
interface ServerConfig {
  name: string;                    // Required - Server name
  version: string;                 // Required - Version (semver)
  description?: string;             // Optional - Description
  host?: string;                   // Optional - Hostname (default: 'localhost')
  baseUrl?: string;                 // Optional - Full base URL
  allowedOrigins?: string[];         // Optional - CSP allowed origins
  sessionIdleTimeoutMs?: number;     // Optional - Session timeout (default: 300000)
  autoCreateSessionOnInvalidId?: boolean; // Optional - Auto-create session (default: true)
}
```

---

## Examples

### Complete Server with Tools and Resources

```typescript
import { MCPServer, text, object } from "mcp-use/server";
import { z } from "zod";

const server = new MCPServer({
  name: "example-server",
  version: "1.0.0",
  description: "Example MCP server",
  baseUrl: process.env.MCP_URL || "http://localhost:3000",
});

// Tool: Greet user
server.tool({
  name: "greet",
  description: "Greet someone by name",
  schema: z.object({
    name: z.string().describe("Person's name"),
  }),
}, async ({ name }) =>
  text(`Hello, ${name}! Welcome to the MCP server.`)
);

// Tool: Calculate
server.tool({
  name: "calculate",
  description: "Perform mathematical operations",
  schema: z.object({
    a: z.number(),
    b: z.number(),
    operation: z.enum(["add", "subtract", "multiply", "divide"]),
  }),
}, async ({ a, b, operation }) => {
  let result: number;
  switch (operation) {
    case "add":
      result = a + b;
      break;
    case "subtract":
      result = a - b;
      break;
    case "multiply":
      result = a * b;
      break;
    case "divide":
      if (b === 0) throw new Error("Cannot divide by zero");
      result = a / b;
      break;
  }
  return object({ a, b, operation, result });
});

// Resource: Config
server.resource({
  name: "config",
  uri: "config://settings",
  description: "Server configuration",
}, async () =>
  object({
    name: "example-server",
    version: "1.0.0",
    tools: ["greet", "calculate"],
  })
);

// HTTP endpoint: Health check
server.get("/health", (c) => {
  return c.json({ status: "ok", timestamp: Date.now() });
});

// Start server
await server.listen(3000);
console.log("Example server running on port 3000");
```

---

## Best Practices

### 1. Type Safety

Use Zod schemas for all parameters.

```typescript
server.tool({
  name: "validate-input",
  schema: z.object({
    email: z.string().email(),
    age: z.number().int().min(18).max(120),
    consent: z.boolean(),
  }),
}, async ({ email, age, consent }) => {
  // TypeScript knows types: email: string, age: number, consent: boolean
  return object({ email, age, consent });
});
```

### 2. Error Handling

Handle errors gracefully and return user-friendly messages.

```typescript
server.tool({
  name: "safe-operation",
  schema: z.object({ input: z.string() }),
}, async ({ input }) => {
  try {
    const result = await riskyOperation(input);
    return object({ success: true, result });
  } catch (error) {
    return object({
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    });
  }
});
```

### 3. Async Operations

Always use async for I/O operations.

```typescript
server.tool({
  name: "fetch-data",
  schema: z.object({ url: z.string().url() }),
}, async ({ url }) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return object(await response.json());
});
```

### 4. Documentation

Provide clear descriptions for tools and parameters.

```typescript
server.tool({
  name: "search-users",
  description: "Search for users with filters",
  schema: z.object({
    query: z.string().describe("Search query (name, email, or ID)"),
    limit: z.number().min(1).max(100).default(20).describe("Maximum results"),
    activeOnly: z.boolean().default(true).describe("Only return active users"),
  }),
}, async ({ query, limit, activeOnly }) => {
  // Implementation
});
```

### 5. Environment Variables

Use environment variables for configuration.

```typescript
const server = new MCPServer({
  name: process.env.SERVER_NAME || "mcp-server",
  version: "1.0.0",
  baseUrl: process.env.BASE_URL || "http://localhost:3000",
  allowedOrigins: process.env.ALLOWED_ORIGINS?.split(",") || [],
});
```
