import { MapPin, Search, Database } from "lucide-react";

const steps = [
  {
    step: "01",
    icon: MapPin,
    title: "Resolve Location",
    description:
      "Your agent describes the location — a city, county, address, or jurisdiction. Shovels resolves it to a geo_id in milliseconds.",
    visual: (
      <div className="rounded-lg border border-border bg-secondary p-4 font-mono text-sm">
        <div className="text-muted-foreground">{"> shovels_geo("}</div>
        <div className="text-primary ml-4">{'"Austin, TX"'}</div>
        <div className="text-muted-foreground">{")"}</div>
        <div className="mt-3 text-foreground">{"→ geo_id: 'q8fdm_HmVcc'"}</div>
      </div>
    ),
  },
  {
    step: "02",
    icon: Search,
    title: "Search Records",
    description:
      "With the geo_id, your agent searches permits, contractors, or decisions — filtered by date, type, status, or value. Results in structured JSON.",
    visual: (
      <div className="rounded-lg border border-border bg-secondary p-4 font-mono text-sm space-y-2">
        {[
          { field: "Permit #", value: "RE2303928" },
          { field: "Type", value: "Electrical - Residential" },
          { field: "Status", value: "Final" },
          { field: "Job Value", value: "$5,000 (cents: 500000)" },
        ].map(({ field, value }) => (
          <div
            key={field}
            className="flex items-center justify-between text-muted-foreground"
          >
            <span>{field}</span>
            <span className="text-primary">{value}</span>
          </div>
        ))}
      </div>
    ),
  },
  {
    step: "03",
    icon: Database,
    title: "Get Structured Data",
    description:
      "Full permit records, contractor profiles, and decision details — all in clean, consistent JSON. Your agent uses it directly. No parsing needed.",
    visual: (
      <div className="rounded-lg border border-border bg-secondary p-4 font-mono text-sm text-muted-foreground space-y-1">
        <div className="text-foreground font-semibold mb-2">response.json</div>
        <div>{"{"}</div>
        <div className="ml-4 text-primary">"job_value_cents"</div>
        <div className="ml-4">: 500000,</div>
        <div className="ml-4 text-primary">"status"</div>
        <div className="ml-4">: "final",</div>
        <div className="ml-4 text-primary">"property_type"</div>
        <div className="ml-4">: "commercial",</div>
        <div className="ml-4">...</div>
        <div>{"}"}</div>
      </div>
    ),
  },
];

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-20 lg:py-32 border-t border-border">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mx-auto max-w-2xl text-center mb-16">
          <p className="text-sm font-medium text-primary mb-2">HOW IT WORKS</p>
          <h2 className="text-4xl lg:text-5xl font-bold text-foreground text-balance mb-4">
            Three steps to permit intelligence.
          </h2>
          <p className="text-lg text-muted-foreground">
            From natural language to structured building data — in a single MCP call.
          </p>
        </div>

        <div className="mt-20 flex flex-col gap-16 lg:gap-24">
          {steps.map((step, index) => (
            <div
              key={step.step}
              className={`grid items-center gap-10 lg:grid-cols-2 lg:gap-16 ${
                index % 2 !== 0 ? "lg:direction-rtl" : ""
              }`}
            >
              <div
                className={`flex flex-col gap-5 ${
                  index % 2 !== 0 ? "lg:order-2" : ""
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs font-bold text-primary">
                    {step.step}
                  </span>
                  <div className="h-px flex-1 bg-border" />
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                    <step.icon className="h-5 w-5" />
                  </div>
                  <h3 className="text-2xl font-bold text-foreground">
                    {step.title}
                  </h3>
                </div>
                <p className="text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </div>
              <div className={index % 2 !== 0 ? "lg:order-1" : ""}>
                {step.visual}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
