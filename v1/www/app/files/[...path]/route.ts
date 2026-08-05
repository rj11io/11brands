import fs from "node:fs/promises"
import path from "node:path"

import { SNAPSHOTS_DIR } from "@/lib/snapshots"

const CONTENT_TYPES: Record<string, string> = {
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".json": "application/json",
  ".md": "text/markdown; charset=utf-8",
}

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path: segments } = await params
  const target = path.resolve(SNAPSHOTS_DIR, ...segments.map(decodeURIComponent))

  // Serve only from inside snapshots/, and only known types.
  if (!target.startsWith(SNAPSHOTS_DIR + path.sep)) {
    return new Response("Not found", { status: 404 })
  }
  const type = CONTENT_TYPES[path.extname(target).toLowerCase()]
  if (!type) {
    return new Response("Not found", { status: 404 })
  }

  try {
    const body = await fs.readFile(target)
    return new Response(new Uint8Array(body), {
      headers: {
        "Content-Type": type,
        // Snapshots are immutable, so their files can cache hard.
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    })
  } catch {
    return new Response("Not found", { status: 404 })
  }
}
