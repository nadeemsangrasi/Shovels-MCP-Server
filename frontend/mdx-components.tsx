import type { MDXComponents } from 'mdx/types'
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'
import { CodeBlock } from '@/components/docs/code-block'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h1: ({ children }) => (
      <h1 className="text-4xl font-bold mb-4 text-foreground">{children}</h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-3xl font-bold mb-3 mt-8 text-foreground">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-2xl font-bold mb-2 mt-6 text-foreground">{children}</h3>
    ),
    h4: ({ children }) => (
      <h4 className="text-xl font-bold mb-2 mt-4 text-foreground">{children}</h4>
    ),
    p: ({ children }) => (
      <p className="mb-4 text-muted-foreground leading-7">{children}</p>
    ),
    ul: ({ children }) => (
      <ul className="list-disc list-inside mb-4 space-y-2 text-muted-foreground">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-inside mb-4 space-y-2 text-muted-foreground">{children}</ol>
    ),
    li: ({ children }) => (
      <li className="text-muted-foreground">{children}</li>
    ),
    a: ({ href, children }) => (
      <a href={href} className="text-primary hover:underline">
        {children}
      </a>
    ),
    code: ({ children }) => (
      <code className="bg-secondary px-1 py-0.5 rounded text-sm font-mono">
        {children}
      </code>
    ),
    pre: ({ children }: any) => {
      const code = children?.props?.children || '';
      const language = children?.props?.className?.replace('language-', '') || 'bash';
      return <CodeBlock code={code} language={language} />;
    },
    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-primary pl-4 my-4 text-muted-foreground italic">
        {children}
      </blockquote>
    ),
    Accordion,
    AccordionItem,
    AccordionTrigger,
    AccordionContent,
    ...components,
  }
}
