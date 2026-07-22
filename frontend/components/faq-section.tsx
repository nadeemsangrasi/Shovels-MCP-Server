import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "What is Shovels?",
    answer:
      "Shovels is an MCP (Model Context Protocol) server that gives AI agents access to U.S. building permits, contractor records, and zoning decisions. Instead of scraping municipal websites or parsing PDFs, your agent queries Shovels for structured, consistent data.",
  },
  {
    question: "What data sources does Shovels support?",
    answer:
      "Shovels aggregates data from municipal building departments, county assessor offices, and public records databases across the United States. This includes building permits, contractor licenses and histories, and zoning/land-use decisions.",
  },
  {
    question: "Do I need an API key?",
    answer:
      "Yes. You need a Shovels API key from app.shovels.ai. The free trial includes 250 requests — enough to evaluate the service. Paid plans are credit-per-record based.",
  },
  {
    question: "What AI agents work with Shovels?",
    answer:
      "Any MCP-compatible agent works out of the box: Claude Code, Claude Desktop, Cursor, Windsurf, GitHub Copilot, Cline, Roo Code, and 30+ more. If it supports MCP, it supports Shovels.",
  },
  {
    question: "Is there a usage limit?",
    answer:
      "The Shovels API free trial provides 250 requests total (not time-limited). Each search result counts as one credit. Paid plans are available for higher volume needs.",
  },
  {
    question: "How do I get started?",
    answer:
      "Sign up at app.shovels.ai for an API key. Then add the Shovels MCP server to your agent's config with a single JSON entry. Your agent can immediately search permits, contractors, and decisions.",
  },
  {
    question: "What jurisdictions are covered?",
    answer:
      "Shovels covers all 50 U.S. states at the state level, plus thousands of cities, counties, and jurisdictions. Coverage depth varies by location — start with shovels_geo() to check what's available for your area.",
  },
];

export function FaqSection() {
  return (
    <section id="faq" className="py-20 lg:py-32 border-t border-border">
      <div className="mx-auto max-w-3xl px-6">
        <div className="text-center mb-12">
          <p className="text-sm font-medium text-primary mb-2">FAQ</p>
          <h2 className="text-4xl lg:text-5xl font-bold text-foreground text-balance">
            Frequently Asked Questions.
          </h2>
        </div>

        <div className="mt-12">
          <Accordion type="single" collapsible className="flex flex-col gap-3">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={faq.question}
                value={`item-${index}`}
                className="rounded-xl border border-border bg-card px-6 data-[state=open]:border-primary/20"
              >
                <AccordionTrigger className="text-left text-base font-medium text-foreground hover:no-underline py-5">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-relaxed text-muted-foreground pb-5">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}
