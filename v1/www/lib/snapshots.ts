import fs from "node:fs/promises"
import path from "node:path"

/** The explorer reads the sibling snapshots/ workspace directly. */
export const SNAPSHOTS_DIR = path.resolve(process.cwd(), "..", "snapshots")

export type BrandColors = {
  signal: string
  ground: string
  ink: string
  footer: string
}

export type SnapshotBrand = {
  key: string
  domain: string
  mode: "dark" | "light"
  colors: BrandColors
  contrast: number
  text: {
    masthead: string | null
    website_row: string | null
    footer_text: string | null
    title: string | null
  }
  files: Record<string, string[]>
}

export type IntegrationRun = {
  run: string
  keys: string[]
  sources: string[]
}

export type Snapshot = {
  stamp: string
  created: string
  sections: {
    brands: { brands: SnapshotBrand[] }
    archive: { brands: SnapshotBrand[] }
    integrations?: { runs: IntegrationRun[] }
  }
}

export type SnapshotSummary = {
  stamp: string
  created: string
  active: number
  archived: number
  integrationRuns: number
}

async function readIndex(stamp: string): Promise<Snapshot | null> {
  try {
    const raw = await fs.readFile(
      path.join(SNAPSHOTS_DIR, stamp, "SNAPSHOT.json"),
      "utf8"
    )
    return JSON.parse(raw) as Snapshot
  } catch {
    return null
  }
}

export async function listSnapshots(): Promise<SnapshotSummary[]> {
  let entries: string[]
  try {
    entries = await fs.readdir(SNAPSHOTS_DIR)
  } catch {
    return []
  }
  const summaries: SnapshotSummary[] = []
  for (const stamp of entries.sort().reverse()) {
    const index = await readIndex(stamp)
    if (!index) continue
    summaries.push({
      stamp: index.stamp,
      created: index.created,
      active: index.sections.brands.brands.length,
      archived: index.sections.archive.brands.length,
      integrationRuns: index.sections.integrations?.runs.length ?? 0,
    })
  }
  return summaries
}

export async function getSnapshot(stamp: string): Promise<Snapshot | null> {
  if (!/^[A-Za-z0-9._-]+$/.test(stamp)) return null
  return readIndex(stamp)
}

/** URL under the streaming route for a file inside a snapshot. */
export function fileUrl(...segments: string[]): string {
  return "/files/" + segments.map(encodeURIComponent).join("/")
}

export function ogWebUrl(stamp: string, section: string, key: string): string {
  return fileUrl(stamp, section, key, "og-web", `${key}-og-web.png`)
}
