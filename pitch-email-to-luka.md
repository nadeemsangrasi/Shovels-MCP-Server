# Pitch Email to Luka

---

**To:** Anurag "Luka" Goyal — Shovels
**Subject:** The MCP server you said wasn't worth building — we built it, and it fixes the exact problems you flagged

---

Hey Luka,

I read your CLI launch post — specifically the part where you explained _why_ you chose CLI over MCP. The two objections were:

1. **Schema bloat** — tool definitions alone burn tens of thousands of tokens before real work starts
2. **Payload bloat** — MCP tool calls don't compose the way shell pipes do, and full records on every row compound the cost

Both real. Both fixable. So instead of debating it, I built the fix.

**What exists now:** a working MCP server against `api.shovels.ai/v2` that answers both concerns directly.

**Schema bloat fix — 4 tools instead of 11 subcommands**

We didn't write 11 separate MCP tools (addresses, cities, counties, jurisdictions, states, permits search, permits get, contractors search, contractors get, contractors permits, contractors employees, contractors metrics, tags, usage). Instead, we grouped them into 4 consolidated tools routed by `action` or `id` params:

- `shovels_permits` — `id` present → get; absent → search (compact)
- `shovels_contractors` — `action`: search | get | permits | employees | metrics
- `shovels_geo` — single query + optional `level` routes address/city/county/jurisdiction/state
- `shovels_meta` — `action`: tags | usage

That's ~75% less schema loaded per session. Every flag, default, and output field from your CLI is preserved inside that routing.

**Payload bloat fix — progressive disclosure**

Search responses return compact rows (~7 fields) plus a `resource` URI (`shovels://permits/<id>`). The agent fetches the full record as a separate call only when it needs the detail. This means:

- A 50-result search that used to carry ~40 fields × 50 rows = ~2,000 fields now carries ~7 × 50 = ~350
- Token cost tracks what the agent actually reads, not what's theoretically available
- Same `get`-by-ID endpoint returns the full record when the agent explicitly asks for it

**Same output contract as your CLI**

The `{data, meta}` envelope, `credits_used`/`credits_remaining`, `error_type` vocabulary, `limit`/`max_records` pagination, and retry-with-jitter on 429 are all identical. An agent that already understands your CLI needs to learn almost nothing new.

**Plus one thing you don't have in the CLI — bring-your-own-key**

We validate each client's `X-API-Key` against your `/usage` endpoint before forwarding the request. The tools then use that same key to call your API. No shared credential, no server-side key management — each user authenticates with their own Shovels API key.

**The pitch:** This is a reference implementation of the MCP server you'll eventually want to ship — yours to take, fork, or productize. It's tested end-to-end against live responses, and it directly answers the two concerns you publicly raised about MCP.

Want to see a Claude Desktop demo this week?

— [Your name]

Yes, you should absolutely send all three links. Since timezone overlap was his primary concern, presenting a self-contained, working product via a Loom video directly addresses that bottleneck by proving you can deliver high-quality async work.

## The Winning Email Structure

Subject: Fixed CLI limitations + built Shovels MCP server (Asynchronous Demo)
The Pitch:
"Hi [CTO Name],
I know timezone overlap was a concern for us earlier. To show you how I work independently and asynchronously, I took the initiative to solve the Shovels CLI limitations we discussed and built a fully functional Model Context Protocol (MCP) server for you.
By wrapping your CLI into an MCP server, Shovels gets native agent discoverability (e.g., in Claude Desktop) and secure enterprise access without security risks.
Here is everything you need to review this at your convenience:

- Demo Video (3 Mins): [Loom Link] — Watch the MCP server query permit data live.
- Live App/Endpoint: [Deployed URL] — Test the integration yourself.
- Source Code: [GitHub Link] — Clean, documented code showing the fixes.

I would love to jump on a quick sync—at any hour that works for your timezone—to discuss joining the team.
Best,
[Your Name]"

## How to Structure Your 3-Minute Loom Video

- Minute 0–1: State the problem. Show the original CLI limitations and explain how your fixes resolved them.
- Minute 1–2: Show the magic. Open Claude Desktop, ask an agent to query Shovels data, and show the MCP server delivering the JSON payload flawlessly.
- Minute 2–3: Show the code. Quickly highlight your repository structure, security protocols, and clean documentation to prove engineering quality.

If you'd like, share:

- The exact fixes you implemented for their CLI.
- Your target timezone versus the CTO's timezone.

I can help you customize the security and architectural talking points for your email.

## 0:00 - 0:30 | The Hook & Timezone Address

- Action: Show your face on camera with a clean desktop background.
- Script: "Hi [CTO Name], since we have a timezone difference, I wanted to respect your time and show you exactly how I work asynchronously. I took your feedback on the Shovels CLI limitations, fixed them, and built an official MCP server on top of it. Here is how it works."

## 0:30 - 1:15 | The "Before & After" CLI Fixes

- Action: Open your terminal or IDE. Show the specific files or commands you changed.
- Visual: Highlight 2-3 specific code snippets where you optimized their existing codebase.
- Talking Point: Explain why you fixed it this way (e.g., "I optimized this query loop to reduce latency by 40%" or "I fixed this parsing bug to prevent agent crashes").

## 1:15 - 2:15 | The Live MCP Magic (The Climax)

- Action: Open Claude Desktop or an AI agent interface side-by-side with your terminal logs.
- Visual: Type a natural language prompt like, "Find recent building permits in Miami using Shovels."
- Talking Point: Watch the agent call your MCP server in real-time. Say: "Notice how the agent instantly discovers the Shovels tool natively. It pulls structured JSON safely without needing raw command-line execution or risking ambient security vulnerabilities."

## 2:15 - 2:45 | Code Quality & Architecture Walkthrough

- Action: Flip over to your GitHub repository.
- Visual: Scroll through your README.md, showing clear setup instructions, environment variables, and architecture diagrams.
- Talking Point: "The code is fully modular, typed, and ready to deploy. I built this completely autonomously to show that timezone gaps don't impact my speed or engineering standards."

## 2:45 - 3:00 | The Call to Action

- Action: Switch back to your camera view.
- Script: "All the links to this repo and the live endpoint are in my email. I am ready to work on your schedule to get onboarded. Let me know what you think!"

---

If you want to refine this further, tell me:

- What exact fixes did you make to their CLI?
- What agent client (Claude Desktop, Cursor, etc.) are you using for the demo?

I can give you the exact script phrases to say for those specific tools.
