# Implementation Examples

## Hero Typography Component
Text as the main visual element with scroll parallax.

```tsx
'use client';
import { motion, useScroll, useTransform } from 'framer-motion';

export const HeroSection = () => {
  const { scrollY } = useScroll();
  const y1 = useTransform(scrollY, [0, 500], [0, 200]);
  const y2 = useTransform(scrollY, [0, 500], [0, -150]);

  return (
    <section className="h-screen flex flex-col justify-center items-center overflow-hidden">
      <motion.h1 style={{ y: y1 }} className="text-[12vw] font-black uppercase leading-none opacity-20">
        Future
      </motion.h1>
      <h2 className="text-[15vw] font-black uppercase leading-none z-10 -mt-[5vw]">
        Vault
      </h2>
      <motion.p style={{ y: y2 }} className="max-w-md text-center mt-12 text-xl text-neutral-400">
        Manage your content ideas with the speed of thought.
      </motion.p>
    </section>
  );
};
```

## Scrollytelling Section
Simple implementation of a horizontal reveal or narrative step.

```tsx
import { motion } from 'framer-motion';

const Feature = ({ title, desc }: { title: string, desc: string }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-100px" }}
    className="h-screen flex items-center p-12"
  >
    <div className="max-w-2xl">
      <h3 className="text-6xl font-bold mb-6">{title}</h3>
      <p className="text-2xl text-neutral-400">{desc}</p>
    </div>
  </motion.div>
);
```

## Custom Cursor (Flashlight Effect)
```tsx
const CursorFollower = () => {
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e: MouseEvent) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return (
    <div
      className="pointer-events-none fixed inset-0 z-50 mix-blend-difference"
      style={{
        background: `radial-gradient(circle 100px at ${pos.x}px ${pos.y}px, white, transparent)`
      }}
    />
  );
}
```
