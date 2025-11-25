---
name: cco-skill-frontend
description: Reduce bundle size under 200KB gzipped, ensure WCAG 2.1 AA compliance, achieve Core Web Vitals targets (LCP under 2.5s, FID under 100ms, CLS under 0.1), and enable SPA SEO
keywords: [bundle size, accessibility, WCAG, Core Web Vitals, LCP, FID, CLS, code splitting, tree shaking, lazy loading, a11y]
category: performance
related_commands:
  action_types: [audit, fix, optimize]
  categories: [performance, quality]
pain_points: [1, 6, 11]
---

# Frontend: Bundle Size, Accessibility & Performance

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


**Skill ID:** `frontend-bundle-a11y-performance`

**Domain:** Frontend optimization (React/Vue/Angular SPAs)

**Purpose:** Reduce bundle size (<200KB gzipped), ensure WCAG 2.1 AA compliance, achieve Core Web Vitals targets (LCP <2.5s, FID <100ms, CLS <0.1), enable SPA SEO

**Related Guidance:** Lazy Loading, Profile Before Optimize
---

---

## Core Techniques

### 1. Bundle Optimization

**Code Splitting:**
```javascript
// ❌ BAD: Single bundle
import Dashboard from './Dashboard';

// ✅ GOOD: Route-based lazy loading
const Dashboard = lazy(() => import('./Dashboard'));
<Suspense fallback={<Loading />}>
  <Route path="/dashboard" component={Dashboard} />
</Suspense>
```

**Tree Shaking:**
```javascript
// ❌ BAD: ~70KB
import _ from 'lodash';

// ✅ GOOD: ~5KB
import debounce from 'lodash/debounce';
```

**Dynamic Imports:**
```javascript
async function exportPDF() {
  const jsPDF = await import('jspdf');
  return new jsPDF.default();
}
```

---

### 2. Accessibility (WCAG 2.1 AA)

**Semantic + ARIA:**
```jsx
<form aria-label="Registration">
  <label htmlFor="email">Email</label>
  <input id="email" type="email" aria-required="true" />
</form>
```

**Keyboard Navigation:**
```javascript
function Modal({ isOpen, onClose }) {
  const modalRef = useRef();
  useEffect(() => { if (isOpen) modalRef.current.focus(); }, [isOpen]);

  return (
    <div role="dialog" aria-modal="true" ref={modalRef} tabIndex={-1}
         onKeyDown={e => e.key === 'Escape' && onClose()}>
      {children}
    </div>
  );
}
```

**Testing:**
```javascript
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('a11y', async () => {
  const { container } = render(<App />);
  expect(await axe(container)).toHaveNoViolations();
});
```

---

### 3. Performance

**Images:**
```html
<img src="hero.jpg" srcset="hero-400w.jpg 400w, hero-800w.jpg 800w"
     sizes="(max-width: 600px) 400px, 800px" loading="lazy" />

<picture>
  <source srcset="img.avif" type="image/avif" />
  <source srcset="img.webp" type="image/webp" />
  <img src="img.jpg" alt="Fallback" />
</picture>
```

**Virtual Scrolling:**
```javascript
import { FixedSizeList } from 'react-window';

<FixedSizeList height={600} itemCount={items.length} itemSize={50}>
  {({ index, style }) => <div style={style}>{items[index]}</div>}
</FixedSizeList>
```

**Memoization:**
```javascript
const Component = memo(({ data }) => {
  const result = useMemo(() => expensiveCalc(data), [data]);
  return <div>{result}</div>;
});
```

---

### 4. SEO for SPAs

**SSR (Next.js):**
```javascript
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}
```

**Meta + Structured Data:**
```html
<head>
  <title>Page Title - Site</title>
  <meta name="description" content="Description" />
  <meta property="og:title" content="Title" />
  <link rel="canonical" href="https://example.com/page" />
</head>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Title",
  "datePublished": "2025-01-17"
}
</script>
```

---

### 5. Responsive Design

**Mobile-First:**
```css
.container { padding: 1rem; }
@media (min-width: 768px) { .container { padding: 2rem; } }
@media (min-width: 1024px) { .container { padding: 3rem; } }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

---

## Patterns

### Bundle Analysis
```bash
npm install --save-dev webpack-bundle-analyzer
# webpack.config.js
plugins: [new BundleAnalyzerPlugin()]
```

### Web Vitals Monitoring
```javascript
import { getCLS, getFID, getLCP } from 'web-vitals';
getCLS(console.log); getFID(console.log); getLCP(console.log);
```

---

## Checklist

**Bundle (<200KB gzipped):**
- [ ] Route-based code splitting
- [ ] Tree shaking (import specific functions)
- [ ] Dynamic imports for heavy libraries
- [ ] Bundle analyzer reviewed

**Accessibility (Lighthouse ≥90):**
- [ ] Semantic HTML (<button>, <nav>, <header>)
- [ ] ARIA labels + roles
- [ ] Keyboard navigation (Tab, Escape)
- [ ] Color contrast ≥4.5:1
- [ ] Automated tests (jest-axe)

**Performance (Core Web Vitals):**
- [ ] Images lazy loaded (loading="lazy")
- [ ] WebP/AVIF formats
- [ ] Virtual scrolling (>1000 items)
- [ ] Memoization (useMemo, memo)
- [ ] LCP <2.5s, FID <100ms, CLS <0.1

**SEO (Score ≥80):**
- [ ] SSR or pre-rendering
- [ ] Meta tags (title, description, OG)
- [ ] Structured data (JSON-LD)
- [ ] Sitemap.xml

**Responsive:**
- [ ] Mobile-first CSS
- [ ] Touch targets ≥44x44px
- [ ] Tested mobile/tablet/desktop

---

## Anti-Patterns

```javascript
// ❌ Import entire library
import _ from 'lodash'; // 70KB

// ❌ Synchronous heavy imports
import Chart from 'chart.js'; // Blocks render

// ❌ Non-semantic HTML
<div class="button">Submit</div>

// ❌ No keyboard support
<div onClick={submit}>Submit</div> // Not keyboard accessible

// ✅ Correct patterns shown above
```

---

## Success Criteria

- Bundle size <200KB gzipped
- Lighthouse: Accessibility ≥90, SEO ≥80
- Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
- Keyboard navigation functional
- Mobile/tablet/desktop tested

---

