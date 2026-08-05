import Link from "next/link"
import { notFound } from "next/navigation"

import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { fileUrl, getSnapshot } from "@/lib/snapshots"

export const dynamic = "force-dynamic"

export default async function BrandPage({
  params,
}: {
  params: Promise<{ snapshot: string; section: string; key: string }>
}) {
  const raw = await params
  const stamp = decodeURIComponent(raw.snapshot)
  const section = raw.section as "brands" | "archive"
  const key = decodeURIComponent(raw.key)

  if (section !== "brands" && section !== "archive") notFound()
  const snapshot = await getSnapshot(stamp)
  const brand = snapshot?.sections[section]?.brands.find((b) => b.key === key)
  if (!snapshot || !brand) notFound()

  const colorRows = Object.entries(brand.colors)
  const textRows = Object.entries(brand.text)
  const favicons = brand.files["favicons"] ?? []
  const ogContent = brand.files["og-content"] ?? []
  const pngFavicons = favicons.filter((f) => f.endsWith(".png"))

  return (
    <main className="mx-auto w-full max-w-4xl px-6 py-12">
      <header className="mb-8">
        <Link
          href={`/${encodeURIComponent(stamp)}`}
          className="text-xs text-muted-foreground hover:text-foreground"
        >
          ← {stamp}
        </Link>
        <div className="mt-2 flex flex-wrap items-center gap-3">
          <h1 className="font-mono text-2xl font-semibold tracking-tight">
            {brand.key}
          </h1>
          <Badge variant={section === "archive" ? "outline" : "secondary"}>
            {section === "archive" ? "archived" : "active"}
          </Badge>
          <Badge variant="outline">{brand.mode}</Badge>
          <Badge variant="outline" className="font-mono">
            {brand.contrast.toFixed(2)}:1
          </Badge>
        </div>
        <p className="mt-1 text-sm text-muted-foreground">{brand.domain}</p>
      </header>

      <section className="mb-10">
        <h2 className="mb-3 text-lg font-semibold">Website OG</h2>
        {/* eslint-disable-next-line @next/next/no-img-element -- exact-pixel snapshot asset */}
        <img
          src={fileUrl(stamp, section, brand.key, "og-web", `${brand.key}-og-web.png`)}
          alt={`${brand.key} website OG card`}
          width={1200}
          height={630}
          className="w-full rounded-xl border border-border"
        />
      </section>

      {ogContent.length > 0 ? (
        <section className="mb-10">
          <h2 className="mb-3 text-lg font-semibold">Content OG</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {ogContent.map((file) => (
              // eslint-disable-next-line @next/next/no-img-element -- exact-pixel snapshot asset
              <img
                key={file}
                src={fileUrl(stamp, section, brand.key, "og-content", file)}
                alt={file}
                width={1200}
                height={630}
                className="w-full rounded-xl border border-border"
              />
            ))}
          </div>
        </section>
      ) : null}

      {pngFavicons.length > 0 ? (
        <section className="mb-10">
          <h2 className="mb-3 text-lg font-semibold">Favicons</h2>
          <div className="flex flex-wrap items-end gap-4 rounded-xl border border-border p-4">
            {pngFavicons.map((file) => (
              <figure key={file} className="text-center">
                {/* eslint-disable-next-line @next/next/no-img-element -- exact-pixel favicon, must not be resampled */}
                <img
                  src={fileUrl(stamp, section, brand.key, "favicons", file)}
                  alt={file}
                  className="mx-auto border border-border/50 [image-rendering:pixelated]"
                  style={{ maxWidth: 96, maxHeight: 96 }}
                />
                <figcaption className="mt-1 font-mono text-[10px] text-muted-foreground">
                  {file}
                </figcaption>
              </figure>
            ))}
          </div>
        </section>
      ) : null}

      <section className="mb-10 grid grid-cols-1 gap-8 sm:grid-cols-2">
        <div>
          <h2 className="mb-3 text-lg font-semibold">Palette</h2>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Role</TableHead>
                <TableHead>Value</TableHead>
                <TableHead />
              </TableRow>
            </TableHeader>
            <TableBody>
              {colorRows.map(([role, value]) => (
                <TableRow key={role}>
                  <TableCell className="capitalize">{role}</TableCell>
                  <TableCell className="font-mono text-xs">{value}</TableCell>
                  <TableCell>
                    <span
                      className="inline-block size-4 rounded-sm border border-border align-middle"
                      style={{ backgroundColor: value }}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div>
          <h2 className="mb-3 text-lg font-semibold">Text</h2>
          <Table>
            <TableBody>
              {textRows.map(([field, value]) => (
                <TableRow key={field}>
                  <TableCell className="whitespace-nowrap text-muted-foreground">
                    {field.replace("_", " ")}
                  </TableCell>
                  <TableCell className="text-xs">
                    {value ?? <em className="text-muted-foreground">omitted</em>}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </section>

      <p className="text-xs text-muted-foreground">
        Manifests:{" "}
        {Object.keys(brand.files).map((kind, i) => (
          <span key={kind}>
            {i > 0 ? " · " : ""}
            <a
              className="underline hover:text-foreground"
              href={fileUrl(stamp, section, brand.key, kind, "MANIFEST.md")}
            >
              {kind}
            </a>
          </span>
        ))}
      </p>
    </main>
  )
}
