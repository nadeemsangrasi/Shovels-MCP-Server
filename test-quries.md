Here are test queries for the Shovels AI MCP (Model Context Protocol), which connects LLMs to deep building permit, construction, and contractor databases.
To thoroughly test real-time agents, these queries are split by specific use cases, ranging from simple data lookups to complex, multi-step analytical reasoning. [1] 
## 🏢 Contractor & Installer Sourcing
Find specific professionals based on localized, historical permit data.

* "Find the top 3 solar installers in Austin, Texas, based on the number of residential permits issued in the last 12 months."
* "Identify contractors in Seattle who have successfully completed structural foundation repairs on historical homes since 2024."
* "Who is the most active commercial HVAC contractor in Miami, Florida right now?"

## 📊 Market Intelligence & Construction Trends
Analyze macroeconomic patterns, regional growth, and construction volumes.

* "Compare the volume of accessory dwelling unit (ADU) permits issued in Los Angeles versus San Diego over the last two years."
* "Which zip codes in Denver are seeing the fastest growth in new commercial construction starts?"
* "Show me the monthly trend of swimming pool permit approvals in Phoenix for the past year."

## 🔍 Property History & Due Diligence
Investigate specific addresses to find hidden building data or verify renovations.

* "Pull the complete building permit history for 100 Main Street, San Francisco, CA. Are there any open or unpermitted major renovations listed?"
* "Check if a permit was ever filed and approved for the deck addition at [Insert Your Address Here] between 2018 and 2022."
* "Identify the exact contractor and total estimated job cost for the kitchen remodel done at [Insert Your Address Here]."

## 🛠️ Advanced Agent Reasoning (Stress Tests)
Test how well the AI agent chains data, filters noise, and computes answers. [2, 3] 

* "Find me a general contractor in Boston who has done at least 5 commercial restaurant build-outs, has zero open/expired violations, and tends to finish projects in under 90 days based on permit timelines."
* "Cross-reference recent roofing permits in Dallas with a list of major hailstorms this year to identify which neighborhoods are updating their roofs the fastest."

------------------------------
If you want to narrow down your testing, let me know:

* What specific geographic region (city/state) you want to pull data for?
* Are you focusing on residential or commercial properties?
* Do you want to test individual property data or macro market trends?


[1] [https://dev.to](https://dev.to/kuldeep_paul/how-to-build-robust-evaluation-datasets-for-ai-agents-tips-and-tricks-3kp0)
[2] [https://www.networkworld.com](https://www.networkworld.com/article/4057121/network-and-cloud-implications-of-agentic-ai.html)
[3] [https://docs.camunda.io](https://docs.camunda.io/docs/guides/getting-started-agentic-orchestration/)
