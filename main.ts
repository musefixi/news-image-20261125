import { copyFileSync, mkdirSync } from "node:fs";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync("entry.png", `${outDir}/entry.png`);
console.log(`copied entry.png to ${outDir}/entry.png`);
