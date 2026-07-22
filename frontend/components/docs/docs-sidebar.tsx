"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { Menu, X } from "lucide-react";

const docsNav = [
  {
    title: "Getting Started",
    items: [
      { title: "Quickstart", href: "/docs" },
      { title: "Introduction", href: "/docs/intro" },
    ],
  },
  {
    title: "Clients",
    items: [
      { title: "Claude Code", href: "/docs/agents/claude-code" },
      { title: "Cursor", href: "/docs/agents/cursor" },
      { title: "Codex", href: "/docs/agents/codex" },
      { title: "VS Code", href: "/docs/agents/vscode" },
      { title: "Windsurf", href: "/docs/agents/windsurf" },
      { title: "OpenCode", href: "/docs/agents/opencode" },
      { title: "All MCP Clients", href: "/docs/clients" },
    ],
  },
  {
    title: "API",
    items: [{ title: "API Reference", href: "/docs/api-reference" }],
  },
];

export function DocsSidebar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setMobileOpen(!mobileOpen)}
        className="fixed top-[84px] left-4 z-50 lg:hidden p-1.5 rounded-lg bg-card border border-border"
        aria-label="Toggle menu"
      >
        {mobileOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
      </button>

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed top-20 left-0 z-40 h-[calc(100vh-5rem)] w-64 border-r border-border bg-card/50 backdrop-blur-sm overflow-y-auto transition-transform duration-300",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        <nav className="p-6 space-y-6">
          {docsNav.map((section) => (
            <div key={section.title}>
              <h4 className="mb-3 text-sm font-semibold text-foreground uppercase tracking-wider">
                {section.title}
              </h4>
              <ul className="space-y-1">
                {section.items.map((item) => (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      onClick={() => setMobileOpen(false)}
                      className={cn(
                        "block px-3 py-2 text-sm rounded-lg transition-all duration-200",
                        pathname === item.href
                          ? "bg-primary text-primary-foreground font-medium shadow-md shadow-primary/20"
                          : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                      )}
                    >
                      {item.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </aside>

      {/* Overlay for mobile */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-30 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}
    </>
  );
}
