import { Shovel } from "lucide-react";

const footerLinks = [
  {
    title: "PRODUCT",
    links: [
      { label: "How It Works", href: "/#how-it-works" },
      { label: "FAQ", href: "/#faq" },
    ],
  },
  {
    title: "RESOURCES",
    links: [
      { label: "Documentation", href: "/docs" },
      { label: "API Reference", href: "/docs/api-reference" },
      { label: "GitHub", href: "https://github.com/daniyalnagori/agentskill-mcp" },
    ],
  },
];

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid gap-12 md:grid-cols-2 lg:grid-cols-5 mb-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <a href="/" className="flex items-center gap-2 mb-6">
              <Shovel className="h-6 w-6 text-primary" />
              <span className="text-lg font-bold text-foreground">
                Shovels
              </span>
            </a>
            <p className="text-sm leading-relaxed text-muted-foreground max-w-sm">
              The MCP server for construction permit intelligence.
              Access building permits, contractor records, and zoning
              decisions through AI agents.
            </p>
          </div>

          {/* Links */}
          {footerLinks.map((group) => (
            <div key={group.title}>
              <h4 className="text-sm font-semibold text-foreground mb-4">
                {group.title}
              </h4>
              <ul className="flex flex-col gap-2">
                {group.links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="flex flex-col items-start gap-4 border-t border-border pt-8 md:flex-row md:items-center md:justify-between">
          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()} Shovels. Open source under the
            MIT License.
          </p>
          <div className="flex items-center gap-6">
            <a
              href="#privacy"
              className="text-xs text-muted-foreground transition-colors hover:text-foreground"
            >
              Privacy
            </a>
            <a
              href="#terms"
              className="text-xs text-muted-foreground transition-colors hover:text-foreground"
            >
              Terms
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
