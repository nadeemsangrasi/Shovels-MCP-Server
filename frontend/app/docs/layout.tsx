import { Navbar } from "@/components/navbar";
import { DocsSidebar } from "@/components/docs/docs-sidebar";

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="pt-20 flex">
        <DocsSidebar />
        <div className="flex-1 lg:ml-64">
          <div className="container py-6 px-4 sm:py-8 sm:px-6 lg:px-8 max-w-4xl">
            <div className="prose prose-invert prose-headings:text-foreground prose-p:text-muted-foreground prose-a:text-primary prose-code:text-foreground prose-pre:bg-secondary prose-strong:text-foreground prose-li:text-muted-foreground max-w-none prose-sm sm:prose-base">
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
