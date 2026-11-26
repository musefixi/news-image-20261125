// news-image-20261125: "Sum up 25 November's world news in one image."
//
// The picture of the day is drawn by draw.py (a deterministic Pillow
// program: six news panels plus a sports strip, 1024x1024) and sits beside
// this file as entry.png. The two programs split the work on purpose:
//
//   draw.py  — the artist. Pure drawing, no network, no randomness; running
//              `python3 draw.py` regenerates entry.png byte-for-byte.
//   main.ts  — the courier. The grader runs this program in a sandbox with
//              no network and reads only /output/entry.png, so the whole
//              job here is a faithful byte-for-byte copy of the bundled
//              image into the output directory. Copying instead of
//              re-drawing keeps the graded run free of any font or Pillow
//              dependency: Node's standard library is all it needs.
//
// Fix (resubmission): the first version copied from the bare relative path
// "entry.png", which Node resolves against the process working directory.
// The grader starts `node /bot/main.ts` from a different directory, so the
// copy failed with ENOENT and the run exited 1. The source is now anchored
// to this file's own location via import.meta.url, exactly like the
// previous day's passing entry, so the lookup works from any cwd.
//
// Locally, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// To redraw the picture from scratch instead:
//   python3 draw.py          # regenerates entry.png in place

// Runs with no network and no dependencies: Node's standard library only.
// The image is drawn once, ahead of time, and bundled with the program.

import { copyFileSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";

// entry.png lives beside main.ts in the repository. The URL form keeps the
// lookup anchored to this file whatever directory the grader starts from.
const source = new URL("./entry.png", import.meta.url);
if (!existsSync(source)) {
  throw new Error("entry.png is missing beside main.ts; nothing to submit");
}

// The grader writes to /output; local runs override it through the env var,
// which keeps the same program usable both in the sandbox and on a laptop.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outputDir, "entry.png");

copyFileSync(source, target);

// The gate accepts at most 1 MiB; log the size so a local run shows at a
// glance that the bundled image is inside the limit.
const { size } = statSync(target);
console.log(`entry.png written to ${target} (${size} of 1048576 bytes)`);
