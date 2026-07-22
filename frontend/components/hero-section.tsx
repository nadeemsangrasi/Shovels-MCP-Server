import { Button } from "@/components/ui/button";
import { ArrowRight, Search, Database, FileCheck } from "lucide-react";
import Link from "next/link";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-40 pb-24 lg:pt-40 lg:pb-40">
      <div className="relative mx-auto max-w-7xl px-6">
        <div className="grid items-center gap-16 lg:grid-cols-2 lg:gap-24">
          {/* Left: Copy */}
          <div className="flex flex-col gap-12">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 px-3 py-1 rounded-full">
                <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                <p className="text-xs font-medium text-primary uppercase tracking-wider">
                  MCP Server for Construction Data
                </p>
              </div>

              <h1 className="text-5xl font-bold leading-tight tracking-tight text-foreground lg:text-6xl text-balance">
                Building permit data, native to your AI agents.
              </h1>

              <p className="text-lg leading-relaxed text-muted-foreground max-w-lg">
                Shovels gives your AI agents direct access to building permits,
                contractor records, zoning decisions, and construction data
                across U.S. jurisdictions — no web scraping, no PDF parsing,
                no manual lookups.
              </p>
            </div>

            <div className="flex flex-col gap-6">
              <div className="flex flex-wrap items-center gap-3">
                <Button
                  size="lg"
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                  asChild
                >
                  <Link
                    href="/docs"
                    className="inline-flex items-center gap-2"
                  >
                    Get Started
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-border text-foreground hover:bg-secondary bg-transparent"
                  asChild
                >
                  <a href="#how-it-works">How It Works</a>
                </Button>
              </div>

              <p className="text-sm text-muted-foreground">
                Free API key. 250 requests to start. Works with every major AI agent.
              </p>
            </div>
          </div>

          {/* Right: Feature cards */}
          <div className="lg:pl-8 grid gap-4">
            <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="rounded-md bg-primary/10 p-2">
                  <Search className="h-5 w-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Search Permits</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Query building permits by location, date, type, and status.
                Structured data returned in real-time.
              </p>
            </div>
            <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="rounded-md bg-primary/10 p-2">
                  <Database className="h-5 w-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Contractor Records</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Find contractors, view their permit history, and track
                performance metrics across projects.
              </p>
            </div>
            <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="rounded-md bg-primary/10 p-2">
                  <FileCheck className="h-5 w-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Zoning Decisions</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Access rezoning applications, variances, and land-use
                decisions from local planning departments.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
