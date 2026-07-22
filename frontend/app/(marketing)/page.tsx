import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { ProblemSection } from "@/components/problem-section"
import { HowItWorksSection } from "@/components/how-it-works-section"
import { AgentCompatibilitySection } from "@/components/agent-compatibility-section"
import { FaqSection } from "@/components/faq-section"
import { FinalCtaSection } from "@/components/final-cta-section"
import { Footer } from "@/components/footer"

export default function Page() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <HeroSection />
      <ProblemSection />
      <HowItWorksSection />
      <AgentCompatibilitySection />
      <FaqSection />
      <FinalCtaSection />
      <Footer />
    </main>
  )
}
