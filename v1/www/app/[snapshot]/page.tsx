import Link from "next/link"
import { notFound } from "next/navigation"

import { Badge } from "@/components/ui/badge"
import { getSnapshot, ogWebUrl, type SnapshotBrand } from "@/lib/snapshots"

export const dynamic = "force-dynamic"

function BrandCard({
  stamp,
  section,
  brand,
}: {
  stamp: string
  section: "brands" | "archive"
  brand: SnapshotBrand
}) {
  return (
    <Link
      href={`/${encodeURIComponent(stamp)}/${section}/${encodeURIComponent(brand.key)}`}
      className="group overflow-hidden rounded-xl border border-border bg-card transition-colors hover:border-foreground/30"
    >
      {/* eslint-disable-next-line @next/next/no-img-element -- streamed from snapshots/, next/image optimization not wanted for exact-pixel assets */}
      <img
        src={ogWebUrl(stamp, section, brand.key)}
        alt={`${brand.key} website OG card`}
        width={1200}
        height={630}
        className="aspect-[1200/630] w-full object-cover"
      />
      <div className="flex items-center justify-between gap-2 px-4 py-3">
        <div className="min-w-0">
          <p className="truncate font-mono text-sm font-medium">{brand.key}</p>
          <p className="truncate text-xs text-muted-foreground">
            {brand.domain}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <span
            className="size-4 rounded-sm border border-border"
            style={{ backgroundColor: brand.colors.signal }}
            title={`signal ${brand.colors.signal}`}
          />
          <Badge variant="outline" className="font-mono text-xs">
            {brand.contrast.toFixed(2)}:1
          </Badge>
        </div>
      </div>
    </Link>
  )
}

export default async function SnapshotPage({
  params,
}: {
  params: Promise<{ snapshot: string }>
}) {
  const { snapshot: stamp } = await params
  const snapshot = await getSnapshot(decodeURIComponent(stamp))
  if (!snapshot) notFound()

  const sections: {
    id: "brands" | "archive"
    label: string
    blurb: string
  }[] = [
    { id: "brands", label: "Active brands", blurb: "the registry as captured" },
    { id: "archive", label: "Archived", blurb: "retired candidates, generated from their configs" },
  ]

  return (
    <main className="mx-auto w-full max-w-6xl px-6 py-12">
      <header className="mb-10">
        <Link
          href="/"
          className="text-xs text-muted-foreground hover:text-foreground"
        >
          ← snapshots
        </Link>
        <h1 className="mt-2 font-mono text-2xl font-semibold tracking-tight">
          {snapshot.stamp}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          created {snapshot.created}
        </p>
      </header>

      {sections.map(({ id, label, blurb }) => (
        <section key={id} className="mb-12">
          <h2 className="text-lg font-semibold">{label}</h2>
          <p className="mb-4 text-sm text-muted-foreground">{blurb}</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {snapshot.sections[id].brands.map((brand) => (
              <BrandCard
                key={brand.key}
                stamp={snapshot.stamp}
                section={id}
                brand={brand}
              />
            ))}
          </div>
        </section>
      ))}

      {snapshot.sections.integrations ? (
        <section className="mb-12">
          <h2 className="text-lg font-semibold">Integration runs</h2>
          <p className="mb-4 text-sm text-muted-foreground">
            consumer-triggered generations, copied verbatim at capture time
          </p>
          <ul className="flex flex-col gap-2">
            {snapshot.sections.integrations.runs.map((run) => (
              <li
                key={run.run}
                className="flex flex-wrap items-center gap-2 rounded-lg border border-border px-4 py-3"
              >
                <span className="font-mono text-sm">{run.run}</span>
                {run.sources.map((source) => (
                  <Badge key={source} variant="secondary">
                    {source}
                  </Badge>
                ))}
                <span className="text-xs text-muted-foreground">
                  {run.keys.join(", ")}
                </span>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </main>
  )
}
