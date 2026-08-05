import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { listSnapshots } from "@/lib/snapshots"

export const dynamic = "force-dynamic"

export default async function Page() {
  const snapshots = await listSnapshots()

  return (
    <main className="mx-auto w-full max-w-3xl px-6 py-16">
      <header className="mb-10">
        <h1 className="font-mono text-2xl font-semibold tracking-tight">
          11brands snapshots
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Immutable captures of the whole brand system — every active brand,
          every archived candidate, and the integration runs, as they stood.
        </p>
      </header>

      {snapshots.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          No snapshots yet. Create one with{" "}
          <code className="font-mono">
            v1/scripts/create_snapshot.py
          </code>
          .
        </p>
      ) : (
        <ul className="flex flex-col gap-4">
          {snapshots.map((snapshot) => (
            <li key={snapshot.stamp}>
              <Link href={`/${encodeURIComponent(snapshot.stamp)}`}>
                <Card className="transition-colors hover:bg-accent/50">
                  <CardHeader>
                    <CardTitle className="font-mono text-base">
                      {snapshot.stamp}
                    </CardTitle>
                    <CardDescription className="flex flex-wrap gap-2 pt-1">
                      <Badge variant="secondary">
                        {snapshot.active} active
                      </Badge>
                      <Badge variant="outline">
                        {snapshot.archived} archived
                      </Badge>
                      <Badge variant="outline">
                        {snapshot.integrationRuns} integration run
                        {snapshot.integrationRuns === 1 ? "" : "s"}
                      </Badge>
                      <span className="text-xs">created {snapshot.created}</span>
                    </CardDescription>
                  </CardHeader>
                </Card>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
