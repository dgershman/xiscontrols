export type CartItem = {
  id: string; // product id (slug)
  sku: string; // ordered part number (option part if chosen)
  title: string;
  price: number | null;
  qty: number;
  url: string;
  img: string;
};

const KEY = 'xis-order-request';

function read(): CartItem[] {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as CartItem[]) : [];
  } catch {
    return [];
  }
}
function write(items: CartItem[]) {
  try {
    localStorage.setItem(KEY, JSON.stringify(items));
  } catch {
    /* storage blocked: cart lives for this page only */
  }
  memo = items;
  window.dispatchEvent(new CustomEvent('cart:change', { detail: items }));
}
let memo: CartItem[] | null = null;

export const cart = {
  items(): CartItem[] {
    if (memo === null) memo = read();
    return memo;
  },
  add(item: Omit<CartItem, 'qty'>, qty = 1) {
    const items = [...this.items()];
    const hit = items.find((i) => i.sku === item.sku && i.id === item.id);
    if (hit) hit.qty += qty;
    else items.push({ ...item, qty });
    write(items);
  },
  setQty(sku: string, qty: number) {
    write(
      this.items()
        .map((i) => (i.sku === sku ? { ...i, qty: Math.max(0, Math.min(999, qty)) } : i))
        .filter((i) => i.qty > 0),
    );
  },
  remove(sku: string) {
    write(this.items().filter((i) => i.sku !== sku));
  },
  clear() {
    write([]);
  },
  count(): number {
    return this.items().reduce((n, i) => n + i.qty, 0);
  },
  subtotal(): { total: number; unpriced: number } {
    let total = 0;
    let unpriced = 0;
    for (const i of this.items()) {
      if (i.price === null) unpriced += 1;
      else total += i.price * i.qty;
    }
    return { total, unpriced };
  },
};

export function initCartBadge() {
  const paint = () => {
    const n = cart.count();
    document.querySelectorAll<HTMLElement>('[data-cart-count]').forEach((el) => (el.textContent = String(n)));
  };
  paint();
  window.addEventListener('cart:change', paint);
  window.addEventListener('storage', (e) => {
    if (e.key === KEY) {
      memo = null;
      paint();
    }
  });
}
