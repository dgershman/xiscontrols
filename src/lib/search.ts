import Fuse from 'fuse.js';
import { SYNONYMS } from './catalog-synonyms';

export type Row = {
  id: string; url: string; sku: string; title: string; cat: string; brands: string[]; models: string[];
  style: string[]; aka: string[]; kw: string[]; norms: string[]; price: string; status: string; tone: string; img: string; text: string;
};

let rows: Row[] | null = null;
let fuse: Fuse<Row> | null = null;
let loading: Promise<void> | null = null;

export function load(): Promise<void> {
  if (fuse) return Promise.resolve();
  if (!loading) {
    loading = fetch('/search-index.json')
      .then((r) => r.json())
      .then((data: Row[]) => {
        rows = data;
        fuse = new Fuse(data, {
          includeScore: true,
          ignoreLocation: true,
          threshold: 0.34,
          useExtendedSearch: true,
          keys: [
            { name: 'sku', weight: 3 },
            { name: 'aka', weight: 2.5 },
            { name: 'title', weight: 2 },
            { name: 'models', weight: 1.6 },
            { name: 'brands', weight: 1.5 },
            { name: 'cat', weight: 1.2 },
            { name: 'kw', weight: 1 },
            { name: 'style', weight: 0.8 },
            { name: 'text', weight: 0.5 },
          ],
        });
      });
  }
  return loading;
}

/** Swap shop-floor words for catalog words: "dog" -> "pawl", "limit switch" -> "microswitch". */
export function expand(q: string): string {
  let s = ' ' + q.toLowerCase().replace(/[^a-z0-9.\-/+ ]/g, ' ') + ' ';
  const pairs: [string, string][] = [];
  for (const [canon, aliases] of Object.entries(SYNONYMS)) for (const a of aliases) pairs.push([a, canon]);
  pairs.sort((a, b) => b[0].length - a[0].length);
  for (const [alias, canon] of pairs) {
    s = s.replace(new RegExp(`\\s${alias.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}s?\\s`, 'g'), ` ${canon} `);
  }
  return s.replace(/\s+/g, ' ').trim();
}

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');

export function search(q: string, limit = 60): Row[] {
  if (!fuse || !rows) return [];
  const query = q.trim();
  if (!query) return [];
  const n = norm(query);
  const exact: Row[] = [];
  if (/\d/.test(query) && n.length >= 3) {
    for (const r of rows) {
      if (r.norms.some((x) => x === n)) exact.unshift(r);
      else if (r.norms.some((x) => x.startsWith(n) || (n.length >= 5 && x.includes(n)))) exact.push(r);
    }
  }
  const expanded = expand(query);
  const fuzzy = fuse.search(expanded, { limit: limit * 2 }).map((h) => h.item);
  const seen = new Set<string>();
  const out: Row[] = [];
  for (const r of [...exact, ...fuzzy]) {
    if (!seen.has(r.id)) {
      seen.add(r.id);
      out.push(r);
    }
    if (out.length >= limit) break;
  }
  return out;
}
