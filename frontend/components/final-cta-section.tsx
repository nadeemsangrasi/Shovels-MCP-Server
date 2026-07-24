"use client";

import { Button } from "@/components/ui/button";
import { Github, ArrowRight, Shovel } from "lucide-react";
import Link from "next/link";

export function FinalCtaSection() {
  return (
    <section className="py-20 lg:py-32 border-t border-border">
      <div className="mx-auto max-w-7xl px-6">
        <div className="text-center">
          <div className="mb-8 flex justify-center">
            <div className="rounded-full bg-primary/10 p-4">
              <Shovel className="h-10 w-10 text-primary" />
            </div>
          </div>

          <h2 className="text-4xl lg:text-5xl font-bold text-foreground text-balance mb-4">
            Start building with permit data.
          </h2>

          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-12">
            Give your AI agents direct access to building permits, contractor records,
            and zoning decisions across U.S. jurisdictions. No scraping. No PDFs.
            Just structured data.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              className="bg-primary text-primary-foreground hover:bg-primary/90 gap-2"
              asChild
            >
              <Link href="/docs">
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-border text-foreground hover:bg-secondary bg-transparent gap-2"
              asChild
            >
              <a href="https://github.com/nadeemsangrasi/Shovels-MCP-Server.git">
                <Github className="h-4 w-4" />
                View on GitHub
              </a>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
