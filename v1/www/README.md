# 11brands snapshots explorer

Deployed at https://brands.rj11.io/

A Next.js app that browses the sibling `../snapshots/` workspace: the snapshot
list, each capture's active / archived / integration sections, and per-brand
pages with OG cards, favicons, palette and manifests.

How it reads data: server components parse each snapshot's `SNAPSHOT.json`;
the images and manifests are streamed by `app/files/[...path]/route.ts`
straight from `../snapshots/` (immutable, so cached hard). There is no copy
step — create a snapshot with `../scripts/create_snapshot.py` and reload.
Assets are rendered exact-pixel (plain `img`, favicons pixelated) on purpose:
never let an optimizer resample them.

Built on the shared starter: TypeScript, Tailwind CSS, shadcn/ui, theming,
path aliases.

## Local development

This app requires Node.js and npm. It does not currently use environment
variables.

```bash
npm install
npm run dev
```

## Commands

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Next.js development server |
| `npm run build` | Create a production build |
| `npm run start` | Serve the production build |
| `npm run lint` | Run ESLint |
| `npm run typecheck` | Check TypeScript without emitting files |
| `npm run format` | Format TypeScript and TSX files with Prettier |

## Adding components

The shadcn/ui configuration writes components to `components/ui/`:

```bash
npx shadcn@latest add <component>
```

## Using components

To use the components in your app, import them as follows:

```tsx
import { Button } from "@/components/ui/button";
```
