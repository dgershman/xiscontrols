import { load, search, type Row } from './search';

const esc = (s: string) =>
  s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

export function rowHtml(r: Row) {
  return `<a href="${r.url}" role="option">
    <img src="${encodeURI(r.img)}" alt="" loading="lazy" />
    <span><span class="sd-sku">${esc(r.sku)}</span><span class="sd-title">${esc(r.title)}</span></span>
    <span class="sd-price">${esc(r.price)}</span></a>`;
}

export function initSearchBox() {
  const form = document.querySelector<HTMLFormElement>('[data-search]');
  const input = document.querySelector<HTMLInputElement>('[data-search-input]');
  const drop = document.querySelector<HTMLElement>('[data-search-drop]');
  if (!form || !input || !drop) return;
  const params = new URLSearchParams(location.search);
  if (location.pathname.startsWith('/search') && params.get('q')) input.value = params.get('q')!;

  let active = -1;
  const close = () => {
    drop.hidden = true;
    active = -1;
  };
  const render = async () => {
    const q = input.value.trim();
    if (q.length < 2) return close();
    await load();
    const hits = search(q, 6);
    drop.innerHTML = hits.length
      ? hits.map(rowHtml).join('') +
        `<a class="sd-all" href="/search/?q=${encodeURIComponent(q)}">See all results for "${esc(q)}"</a>`
      : `<p class="sd-none">No match for "${esc(q)}". Try a part number, a brand, or <a href="/identify/">send us a photo</a> and we'll identify it.</p>`;
    drop.hidden = false;
    active = -1;
  };
  let t: number | undefined;
  input.addEventListener('focus', () => load());
  input.addEventListener('input', () => {
    clearTimeout(t);
    t = window.setTimeout(render, 120);
  });
  input.addEventListener('keydown', (e) => {
    const links = [...drop.querySelectorAll<HTMLAnchorElement>('a[role=option]')];
    if (e.key === 'Escape') return close();
    if (!links.length || drop.hidden) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      active = (active + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
      links.forEach((l, i) => l.setAttribute('aria-selected', String(i === active)));
    } else if (e.key === 'Enter' && active >= 0) {
      e.preventDefault();
      location.href = links[active].href;
    }
  });
  document.addEventListener('click', (e) => {
    if (!form.contains(e.target as Node)) close();
  });
}
