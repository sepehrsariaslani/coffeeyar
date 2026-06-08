/**
 * post-build script: reads dist/index.html and injects the
 * correct hashed <script> and <link> tags into coffee.html.
 *
 * Run automatically via "postbuild" in package.json.
 */
import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const distIndex = resolve(__dirname, "../dist/index.html");
const coffeeHtml = resolve(
  __dirname,
  "../../coffeeyar/www/coffee.html"
);

const dist = readFileSync(distIndex, "utf-8");

// Extract the hashed filenames from the generated dist/index.html
const jsMatch = dist.match(/src="\/assets\/(index-[^"]+\.js)"/);
const cssMatch = dist.match(/href="\/assets\/(index-[^"]+\.css)"/);

if (!jsMatch || !cssMatch) {
  console.error("❌  Could not find index JS/CSS in dist/index.html");
  process.exit(1);
}

const jsFile = jsMatch[1];
const cssFile = cssMatch[1];

console.log(`✅  JS  → ${jsFile}`);
console.log(`✅  CSS → ${cssFile}`);

let coffee = readFileSync(coffeeHtml, "utf-8");

// Replace both asset references in coffee.html
coffee = coffee.replace(
  /src="\/assets\/coffeeyar\/frontend\/assets\/index-[^"]+\.js"/,
  `src="/assets/coffeeyar/frontend/assets/${jsFile}"`
);
coffee = coffee.replace(
  /href="\/assets\/coffeeyar\/frontend\/assets\/index-[^"]+\.css"/,
  `href="/assets/coffeeyar/frontend/assets/${cssFile}"`
);

writeFileSync(coffeeHtml, coffee, "utf-8");
console.log("✅  coffee.html updated successfully");
