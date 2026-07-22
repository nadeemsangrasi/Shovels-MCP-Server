"use client";

import {
  ClaudeCode,
  Claude,
  Cursor,
  Cline,
  Windsurf,
  Codex,
  Qwen,
  RooCode,
  Trae,
  Zencoder,
  Qoder,
  Replit,
  Copilot,
  Antigravity,
  Amp,
  Anthropic,
  OpenClaw,
  OpenCode,
  GeminiCLI,
  Kimi,
  Junie,
  KiloCode,
  Mistral,
  ZenMux,
  OpenHands,
} from "@lobehub/icons";
import Link from "next/link";

const AGENTS_ROW1 = [
  { name: "Claude Code", slug: "claude-code", Icon: ClaudeCode },
  { name: "Claude", slug: "claude", Icon: Claude },
  { name: "Cursor", slug: "cursor", Icon: Cursor },
  { name: "Cline", slug: "cline", Icon: Cline },
  { name: "Windsurf", slug: "windsurf", Icon: Windsurf },
  { name: "Codex", slug: "codex", Icon: Codex },
  { name: "Qwen Code", slug: "qwen", Icon: Qwen },
  { name: "Roo Code", slug: "roo-code", Icon: RooCode },
  { name: "Trae", slug: "trae", Icon: Trae },
  { name: "OpenClaw", slug: "openclaw", Icon: OpenClaw },
  { name: "OpenCode", slug: "opencode", Icon: OpenCode },
  { name: "Gemini CLI", slug: "gemini-cli", Icon: GeminiCLI },
  { name: "Kimi CLI", slug: "kimi-cli", Icon: Kimi },
];

const AGENTS_ROW2 = [
  { name: "Zencoder", slug: "zencoder", Icon: Zencoder },
  { name: "Qoder", slug: "qoder", Icon: Qoder },
  { name: "Replit", slug: "replit", Icon: Replit },
  { name: "GitHub Copilot", slug: "copilot", Icon: Copilot },
  { name: "Antigravity", slug: "antigravity", Icon: Antigravity },
  { name: "Amp", slug: "amp", Icon: Amp },
  { name: "Anthropic", slug: "anthropic", Icon: Anthropic },
  { name: "Junie", slug: "junie", Icon: Junie },
  { name: "KiloCode", slug: "kilocode", Icon: KiloCode },
  { name: "Mistral Vibe", slug: "mistral-vibe", Icon: Mistral },
  { name: "Mux", slug: "mux", Icon: ZenMux },
  { name: "OpenHands", slug: "openhands", Icon: OpenHands },
];

interface AgentIconProps {
  name: string;
  slug: string;
  Icon: any;
}

function AgentIcon({ name, slug, Icon }: AgentIconProps) {
  return (
    <div className="relative w-10 h-10 rounded-lg overflow-hidden flex items-center justify-center">
      <Icon.Avatar size={40} />
    </div>
  );
}

export function AgentCompatibilitySection() {
  return (
    <section id="agents" className="py-20 lg:py-32 border-t border-border">
      <div className="mx-auto max-w-7xl px-6">
        <div className="text-center mb-16">
          <p className="text-sm font-medium text-primary mb-2">
            AGENT COMPATIBILITY
          </p>
          <h2 className="text-4xl lg:text-5xl font-bold text-foreground text-balance mb-4">
            MCP-compatible. Works everywhere.
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            If it supports MCP, it supports Shovels. No custom SDKs, no vendor lock-in.
            One config entry and your agent has permit data superpowers.
          </p>
        </div>

        {/* Row 1 - Scrolls left */}
        <div className="mb-8 overflow-hidden">
          <div className="flex gap-6 animate-scroll-left-slow">
            {[...AGENTS_ROW1, ...AGENTS_ROW1].map((agent, idx) => (
              <div
                key={`row1-${idx}`}
                className="flex flex-col items-center gap-2 flex-shrink-0"
              >
                <AgentIcon
                  name={agent.name}
                  slug={agent.slug}
                  Icon={agent.Icon}
                />
                <p className="text-xs text-muted-foreground whitespace-nowrap">
                  {agent.name}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Row 2 - Scrolls right */}
        <div className="overflow-hidden mb-12">
          <div className="flex gap-6 animate-scroll-right-slow">
            {[...AGENTS_ROW2, ...AGENTS_ROW2].map((agent, idx) => (
              <div
                key={`row2-${idx}`}
                className="flex flex-col items-center gap-2 flex-shrink-0"
              >
                <AgentIcon
                  name={agent.name}
                  slug={agent.slug}
                  Icon={agent.Icon}
                />
                <p className="text-xs text-muted-foreground whitespace-nowrap">
                  {agent.name}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="text-center">
          <p className="text-sm text-muted-foreground mb-2">
            MCP-compatible · Works out of the box · Zero configuration
          </p>
          <Link
            href="/docs/clients"
            className="text-primary hover:text-primary/80 text-sm font-medium transition-colors"
          >
            View supported agents →
          </Link>
        </div>
      </div>

      <style jsx>{`
        @keyframes scroll-left-slow {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        @keyframes scroll-right-slow {
          0% { transform: translateX(-50%); }
          100% { transform: translateX(0); }
        }
        .animate-scroll-left-slow {
          animation: scroll-left-slow 40s linear infinite;
        }
        .animate-scroll-right-slow {
          animation: scroll-right-slow 35s linear infinite;
        }
        div:hover .animate-scroll-left-slow,
        div:hover .animate-scroll-right-slow {
          animation-play-state: paused;
        }
      `}</style>
    </section>
  );
}
