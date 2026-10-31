import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const parts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/parts' }),
  schema: z.object({
    sku: z.string(),
    title: z.string(),
    category: z.string(),
    order: z.number().default(999),
    price: z.preprocess((v) => (v === '' || v === undefined ? null : v), z.number().nullable()).default(null),
    price_note: z.string().default(''),
    options: z
      .array(z.object({ part: z.string(), price: z.preprocess((v) => (v === '' || v === undefined ? null : v), z.number().nullable()) }))
      .default([]),
    status: z
      .enum(['in-stock', 'limited', 'special-order', 'backorder', 'out-of-stock', 'coming-soon', 'call', 'sold-out'])
      .default('in-stock'),
    best_choice: z.boolean().default(false),
    hidden: z.boolean().default(false),
    brands: z.array(z.string()).default([]),
    models: z.array(z.string()).default([]),
    style: z.array(z.string()).default([]),
    also_known_as: z.array(z.string()).default([]),
    keywords: z.array(z.string()).default([]),
    images: z.array(z.string()).default([]),
    documents: z.array(z.object({ label: z.string(), file: z.string() })).default([]),
    related: z.array(z.string()).default([]),
    notes: z.array(z.string()).default([]),
    legacy_row: z.number().optional(),
  }),
});

export const collections = { parts };
