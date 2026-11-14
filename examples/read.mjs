// Node.js 18+에서 실행: node examples/read.mjs
import { readFile } from 'node:fs/promises';
const data = JSON.parse(await readFile(new URL('../data/hexagrams.json', import.meta.url), 'utf8'));
const hexagram = data.hexagrams.find(h => h.number === 1);
console.log(hexagram.full_name_ko, hexagram.symbol, hexagram.judgment_zh);
console.log(hexagram.lines[0].label_zh, hexagram.lines[0].text_zh);
