import { Building2, FileSearch, Globe } from "lucide-react"

const painPoints = [
  {
    icon: Globe,
    title: "Scattered across jurisdictions",
    description: "Every city and county has its own system. PDFs, legacy portals, scanned documents — there's no single source of truth for building data.",
  },
  {
    icon: FileSearch,
    title: "Inconsistent formats",
    description: "Permit data comes in every shape imaginable. Different schemas, missing fields, inconsistent naming. Comparing across jurisdictions is nearly impossible.",
  },
  {
    icon: Building2,
    title: "No unified API",
    description: "Each integration is custom. Need data from multiple cities? That's multiple contracts, multiple formats, multiple headaches. Every integration starts from scratch.",
  },
]

export function ProblemSection() {
  return (
    <section className="relative py-24 lg:py-32 border-t border-border">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mx-auto max-w-3xl mb-24">
          <h2 className="text-4xl font-bold text-foreground lg:text-5xl text-balance mb-8">
            The problem with building permit data today.
          </h2>
          <p className="text-lg text-muted-foreground leading-relaxed">
            Building permit data is trapped in municipal systems — PDFs, legacy portals, and
            inconsistent databases. Every jurisdiction speaks its own data language. AI agents
            need a universal translator.
          </p>
        </div>

        <div className="grid gap-12 md:grid-cols-3 pb-12 border-b border-border">
          {painPoints.map((point) => (
            <div
              key={point.title}
              className="flex flex-col gap-6"
            >
              <div className="flex h-14 w-14 items-center justify-center border border-border rounded-lg">
                <point.icon className="h-6 w-6 text-foreground" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-3">{point.title}</h3>
                <p className="text-base leading-relaxed text-muted-foreground">{point.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
