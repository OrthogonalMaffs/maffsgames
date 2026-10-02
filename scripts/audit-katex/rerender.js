// node rerender.js <katex dist dir>   stdin: JSON [[s, display], ...]  stdout: JSON [html, ...]
// Use the same KaTeX 0.16.9 the site loads.
const katex = require(require('path').resolve(process.argv[2], 'katex.js'));
const inp = JSON.parse(require('fs').readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(inp.map(([s, d]) => {
  try { return katex.renderToString(s, {throwOnError: false, displayMode: !!d}); } catch (e) { return null; }
})));
