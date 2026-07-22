"use client";

import Image from "next/image";
import Link from "next/link";

const partners = [
  // AI & LLMs
  { name: "OpenAI", avatar: "https://avatars.githubusercontent.com/u/14957082?s=64&v=4" },
  { name: "Anthropic", avatar: "https://avatars.githubusercontent.com/u/143567668?s=64&v=4" },
  { name: "Google", avatar: "https://avatars.githubusercontent.com/u/2810941?s=64&v=4" },
  { name: "Google Gemini", avatar: "https://avatars.githubusercontent.com/u/174465178?s=64&v=4" },
  { name: "Hugging Face", avatar: "https://avatars.githubusercontent.com/u/25720743?s=64&v=4" },
  { name: "Replicate", avatar: "https://avatars.githubusercontent.com/u/142758687?s=64&v=4" },
  { name: "MiniMax", avatar: "https://avatars.githubusercontent.com/u/155615448?s=64&v=4" },
  { name: "NVIDIA", avatar: "https://avatars.githubusercontent.com/u/1728152?s=64&v=4" },
  { name: "Fal AI", avatar: "https://avatars.githubusercontent.com/u/150994415?s=64&v=4" },
  { name: "Venice AI", avatar: "https://avatars.githubusercontent.com/u/173646455?s=64&v=4" },
  // Cloud & Infrastructure
  { name: "Vercel", avatar: "https://avatars.githubusercontent.com/u/14985020?s=64&v=4" },
  { name: "Cloudflare", avatar: "https://avatars.githubusercontent.com/u/314135?s=64&v=4" },
  { name: "Netlify", avatar: "https://avatars.githubusercontent.com/u/7892489?s=64&v=4" },
  { name: "Hashicorp", avatar: "https://avatars.githubusercontent.com/u/761456?s=64&v=4" },
  { name: "Cypress", avatar: "https://avatars.githubusercontent.com/u/8908513?s=64&v=4" },
  { name: "Expo", avatar: "https://avatars.githubusercontent.com/u/12504344?s=64&v=4" },
  { name: "Angular", avatar: "https://avatars.githubusercontent.com/u/139426?s=64&v=4" },
  { name: "Flutter", avatar: "https://avatars.githubusercontent.com/u/14101776?s=64&v=4" },
  // Database & Storage
  { name: "MongoDB", avatar: "https://avatars.githubusercontent.com/u/45120?s=64&v=4" },
  { name: "Supabase", avatar: "https://avatars.githubusercontent.com/u/54469796?s=64&v=4" },
  { name: "Firebase", avatar: "https://avatars.githubusercontent.com/u/1335026?s=64&v=4" },
  { name: "Neon", avatar: "https://avatars.githubusercontent.com/u/109699203?s=64&v=4" },
  { name: "ClickHouse", avatar: "https://avatars.githubusercontent.com/u/54801242?s=64&v=4" },
  { name: "Redis", avatar: "https://avatars.githubusercontent.com/u/1529926?s=64&v=4" },
  { name: "DuckDB", avatar: "https://avatars.githubusercontent.com/u/90930955?s=64&v=4" },
  { name: "Qdrant", avatar: "https://avatars.githubusercontent.com/u/95043391?s=64&v=4" },
  // Payments & Fintech
  { name: "Stripe", avatar: "https://avatars.githubusercontent.com/u/856813?s=64&v=4" },
  { name: "Coinbase", avatar: "https://avatars.githubusercontent.com/u/1885080?s=64&v=4" },
  { name: "Binance", avatar: "https://avatars.githubusercontent.com/u/23902424?s=64&v=4" },
  // Developer Tools
  { name: "Auth0", avatar: "https://avatars.githubusercontent.com/u/2824157?s=64&v=4" },
  { name: "Better Auth", avatar: "https://avatars.githubusercontent.com/u/177674041?s=64&v=4" },
  { name: "Firecrawl", avatar: "https://avatars.githubusercontent.com/u/137631688?s=64&v=4" },
  { name: "Browserbase", avatar: "https://avatars.githubusercontent.com/u/138443293?s=64&v=4" },
  { name: "Remotion", avatar: "https://avatars.githubusercontent.com/u/65511402?s=64&v=4" },
  { name: "Sanity", avatar: "https://avatars.githubusercontent.com/u/17177659?s=64&v=4" },
  { name: "Tinybird", avatar: "https://avatars.githubusercontent.com/u/69145799?s=64&v=4" },
  { name: "Typefully", avatar: "https://avatars.githubusercontent.com/u/111137213?s=64&v=4" },
  { name: "Resend", avatar: "https://avatars.githubusercontent.com/u/127139101?s=64&v=4" },
  // Security & Monitoring
  { name: "Sentry", avatar: "https://avatars.githubusercontent.com/u/1396951?s=64&v=4" },
  { name: "Trail of Bits", avatar: "https://avatars.githubusercontent.com/u/2443621?s=64&v=4" },
  { name: "Brave", avatar: "https://avatars.githubusercontent.com/u/11573432?s=64&v=4" },
  { name: "Datadog", avatar: "https://avatars.githubusercontent.com/u/365230?s=64&v=4" },
  // Media & Content
  { name: "WordPress", avatar: "https://avatars.githubusercontent.com/u/276006?s=64&v=4" },
  { name: "Figma", avatar: "https://avatars.githubusercontent.com/u/5155369?s=64&v=4" },
  { name: "GSAP", avatar: "https://avatars.githubusercontent.com/u/7824801?s=64&v=4" },
  { name: "Courier", avatar: "https://avatars.githubusercontent.com/u/61319840?s=64&v=4" },
  { name: "Callstack", avatar: "https://avatars.githubusercontent.com/u/10681383?s=64&v=4" },
  { name: "Composio", avatar: "https://avatars.githubusercontent.com/u/139064527?s=64&v=4" },
  // Other
  { name: "Apollo GraphQL", avatar: "https://avatars.githubusercontent.com/u/17189275?s=64&v=4" },
  { name: "Notion", avatar: "https://avatars.githubusercontent.com/u/16750161?s=64&v=4" },
  { name: "Google Workspace", avatar: "https://avatars.githubusercontent.com/u/16779465?s=64&v=4" },
  { name: "Google Labs", avatar: "https://avatars.githubusercontent.com/u/166967263?s=64&v=4" },
  { name: "VoltAgent", avatar: "https://avatars.githubusercontent.com/u/151584882?s=64&v=4" },
];

// Deduplicate
const uniquePartners = Array.from(
  new Map(partners.map((p) => [p.name, p])).values()
);

// Split into two rows
const mid = Math.ceil(uniquePartners.length / 2);
const ROW1 = uniquePartners.slice(0, mid);
const ROW2 = uniquePartners.slice(mid);

export function OfficialPartnersSection() {
  return (
    <section id="partners" className="py-20 lg:py-32 border-t border-border">
      <div className="mx-auto max-w-7xl px-6">
        <div className="text-center mb-16">
          <p className="text-sm font-medium text-primary mb-2">
            OFFICIAL REPOSITORIES
          </p>
          <h2 className="font-heading text-4xl lg:text-5xl font-bold text-foreground text-balance mb-4">
            Skills from the companies you trust.
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Every repository is verified and maintained by its respective
            organization. No community submissions — 100% official sources.
          </p>
        </div>

        {/* Row 1 - Scrolls left */}
        <div className="mb-8 overflow-hidden">
          <div className="flex gap-10 animate-scroll-left-slow">
            {[...ROW1, ...ROW1].map((partner, idx) => (
              <div
                key={`row1-${idx}`}
                className="flex flex-col items-center gap-2 flex-shrink-0"
              >
                <div className="w-12 h-12 rounded-xl overflow-hidden border border-border/50 flex items-center justify-center bg-card">
                  <Image
                    src={partner.avatar}
                    alt={partner.name}
                    width={40}
                    height={40}
                    className="rounded-lg"
                  />
                </div>
                <p className="text-xs text-muted-foreground whitespace-nowrap">
                  {partner.name}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Row 2 - Scrolls right */}
        <div className="overflow-hidden mb-12">
          <div className="flex gap-10 animate-scroll-right-slow">
            {[...ROW2, ...ROW2].map((partner, idx) => (
              <div
                key={`row2-${idx}`}
                className="flex flex-col items-center gap-2 flex-shrink-0"
              >
                <div className="w-12 h-12 rounded-xl overflow-hidden border border-border/50 flex items-center justify-center bg-card">
                  <Image
                    src={partner.avatar}
                    alt={partner.name}
                    width={40}
                    height={40}
                    className="rounded-lg"
                  />
                </div>
                <p className="text-xs text-muted-foreground whitespace-nowrap">
                  {partner.name}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="text-center">
          <p className="text-sm text-muted-foreground mb-2">
            60+ official repositories · 1,000+ verified skills · 100% verified sources
          </p>
          <Link
            href="#repos"
            className="text-primary hover:text-primary/80 text-sm font-medium transition-colors"
          >
            View all repositories →
          </Link>
        </div>
      </div>

      <style jsx>{`
        @keyframes scroll-left-slow {
          0% {
            transform: translateX(0);
          }
          100% {
            transform: translateX(-50%);
          }
        }
        @keyframes scroll-right-slow {
          0% {
            transform: translateX(-50%);
          }
          100% {
            transform: translateX(0);
          }
        }
        .animate-scroll-left-slow {
          animation: scroll-left-slow 50s linear infinite;
        }
        .animate-scroll-right-slow {
          animation: scroll-right-slow 45s linear infinite;
        }
        div:hover .animate-scroll-left-slow,
        div:hover .animate-scroll-right-slow {
          animation-play-state: paused;
        }
      `}</style>
    </section>
  );
}
