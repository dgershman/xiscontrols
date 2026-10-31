import { getCollection, type CollectionEntry } from 'astro:content';
import categories from '../data/categories.json';
import brands from '../data/brands.json';

export type Part = CollectionEntry<'parts'>;
export type Category = (typeof categories)[number];

export { categories, brands };

export async function getParts(): Promise<Part[]> {
  const all = await getCollection('parts', (p) => !p.data.hidden);
  return all.sort((a, b) => {
    const ca = categories.findIndex((c) => c.slug === a.data.category);
    const cb = categories.findIndex((c) => c.slug === b.data.category);
    return ca - cb || a.data.order - b.data.order;
  });
}

export const partUrl = (p: Part) => `/parts/${p.id}/`;
export const categoryUrl = (slug: string) => `/category/${slug.toLowerCase()}/`;
export const brandSlug = (name: string) => name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
export const brandUrl = (name: string) => `/brand/${brandSlug(name)}/`;

export function categoryOf(slug: string): Category | undefined {
  return categories.find((c) => c.slug === slug);
}

export function money(n: number | null | undefined): string {
  if (n === null || n === undefined) return '';
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
}

export const STATUS: Record<string, { label: string; tone: 'ok' | 'warn' | 'stop' | 'info' }> = {
  'in-stock': { label: 'In stock', tone: 'ok' },
  limited: { label: 'Limited supply', tone: 'warn' },
  'special-order': { label: 'Special order', tone: 'info' },
  backorder: { label: 'On backorder', tone: 'warn' },
  'out-of-stock': { label: 'Out of stock, call for lead time', tone: 'stop' },
  'coming-soon': { label: 'Coming soon', tone: 'info' },
  call: { label: 'Call for price', tone: 'info' },
  'sold-out': { label: 'Sold out', tone: 'stop' },
};

export const canOrder = (p: Part) => !['sold-out', 'coming-soon'].includes(p.data.status);

export function priceLabel(p: Part): string {
  const d = p.data;
  if (d.options.length > 1) {
    const ps = d.options.map((o) => o.price).filter((x): x is number => typeof x === 'number');
    if (ps.length) {
      const lo = Math.min(...ps);
      const hi = Math.max(...ps);
      return lo === hi ? money(lo) : `${money(lo)} to ${money(hi)}`;
    }
  }
  if (d.price !== null) return money(d.price);
  return d.status === 'sold-out' ? 'Sold out' : 'Call for price';
}

export { SYNONYMS } from './catalog-synonyms';

export function images(p: Part): string[] {
  return p.data.images.length ? p.data.images : ['/media/brand/no-photo.svg'];
}
