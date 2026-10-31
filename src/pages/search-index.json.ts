import type { APIRoute } from 'astro';
import { getParts, categoryOf, partUrl, priceLabel, STATUS } from '../lib/catalog';

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');

export const GET: APIRoute = async () => {
  const parts = await getParts();
  const rows = parts.map((p) => {
    const d = p.data;
    const body = (p.body ?? '').replace(/\s+/g, ' ').trim();
    return {
      id: p.id,
      url: partUrl(p),
      sku: d.sku,
      title: d.title,
      cat: categoryOf(d.category)?.name ?? d.category,
      brands: d.brands,
      models: d.models,
      style: d.style,
      aka: [...d.also_known_as, ...d.options.map((o) => o.part)],
      kw: d.keywords,
      norms: [d.sku, ...d.also_known_as, ...d.options.map((o) => o.part)].map(norm),
      price: priceLabel(p),
      status: STATUS[d.status]?.label ?? '',
      tone: STATUS[d.status]?.tone ?? 'info',
      img: d.images[0] ?? '/media/brand/no-photo.svg',
      text: body.slice(0, 400),
    };
  });
  return new Response(JSON.stringify(rows), { headers: { 'Content-Type': 'application/json' } });
};
