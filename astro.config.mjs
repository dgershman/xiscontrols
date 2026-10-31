import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://xiscontrols.com',
  output: 'static',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
});
