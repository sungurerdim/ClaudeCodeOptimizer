# Meta-Frameworks
*Full-stack framework rules*

## Next.js (Framework:Next)
**Trigger:** {nextjs_deps}, {nextjs_config}

- **App-Router**: Use App Router for new projects (Next.js 13+)
- **Server-Actions**: Server Actions for mutations, not API routes (Next.js 14+)
- **Streaming-SSR**: Use streaming with Suspense for faster TTFB
- **Route-Handlers**: Use Route Handlers (route.ts) instead of API routes for App Router
- **Metadata-API**: Use Metadata API for SEO, not manual head tags
- **Image-Component**: Use next/image for automatic optimization
- **Font-Optimization**: Use next/font for zero-layout-shift fonts
- **Parallel-Routes**: Use parallel routes for complex layouts
- **Intercepting-Routes**: Use intercepting routes for modals/sheets

## Nuxt (Framework:Nuxt)
**Trigger:** {nuxt_deps}, {nuxt_config}

- **Nitro-Server**: Use Nitro for server API routes
- **Auto-Imports**: Leverage auto-imports, don't manual import
- **Composables**: Use composables/ for shared logic
- **Server-Directory**: Use server/ for API endpoints
- **TypeScript-Native**: Full TypeScript support out of box
- **Layers**: Use Nuxt Layers for shared config
- **State-useState**: Use useState for SSR-safe state

## SvelteKit (Framework:SvelteKit)
**Trigger:** {sveltekit_deps}, {sveltekit_config}

- **Load-Functions**: Use +page.ts/+page.server.ts for data loading
- **Form-Actions**: Use form actions for mutations
- **Hooks**: Use hooks.server.ts for middleware
- **Adapter-Select**: Choose adapter based on deployment target
- **Prerender**: Prerender static pages where possible
- **SSR-First**: SSR by default, disable only when necessary

## Remix (Framework:Remix)
**Trigger:** {remix_deps}, {remix_patterns}

- **Loader-Action**: Use loader for GET, action for mutations
- **Nested-Routes**: Leverage nested routing for UI composition
- **ErrorBoundary**: Define error boundaries per route
- **Defer-Streaming**: Use defer for streaming large data
- **Form-Component**: Use Remix Form for progressive enhancement
- **Meta-Function**: Use meta function for route-specific SEO
