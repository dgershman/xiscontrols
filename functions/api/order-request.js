import { esc, json, send, validEmail } from './_mail.js';

const money = (n) => (typeof n === 'number' ? `$${n.toFixed(2)}` : 'call');

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'bad request' }, 400);
  }
  const c = body.customer || {};
  const items = Array.isArray(body.items) ? body.items.slice(0, 100) : [];
  if (body.website) return json({ ok: true }); // honeypot
  for (const k of ['name', 'company', 'email', 'phone', 'address']) {
    if (!String(c[k] || '').trim()) return json({ error: `missing ${k}` }, 422);
  }
  if (!validEmail(c.email) || !items.length) return json({ error: 'invalid' }, 422);

  const clean = items.map((i) => ({
    sku: String(i.sku || '').slice(0, 40),
    title: String(i.title || '').slice(0, 200),
    qty: Math.max(1, Math.min(999, Number(i.qty) || 1)),
    price: typeof i.price === 'number' ? i.price : null,
    url: String(i.url || '').startsWith('/') ? String(i.url) : '',
  }));
  const subtotal = clean.reduce((s, i) => s + (i.price ?? 0) * i.qty, 0);
  const origin = new URL(request.url).origin;
  const rows = clean
    .map(
      (i) =>
        `<tr><td style="padding:4px 8px">${i.qty}</td><td style="padding:4px 8px"><a href="${origin}${esc(i.url)}"><b>${esc(i.sku)}</b></a> ${esc(i.title)}</td><td style="padding:4px 8px;text-align:right">${money(i.price)}</td></tr>`,
    )
    .join('');
  const who = `${esc(c.name)}, ${esc(c.company)}`;
  const details = `
    <p><b>${who}</b><br>${esc(c.email)} &middot; ${esc(c.phone)}</p>
    <p><b>Ship to:</b><br>${esc(c.address).replace(/\n/g, '<br>')}</p>
    <p><b>Machine:</b> ${esc(c.machine) || '(not given)'}<br><b>PO:</b> ${esc(c.po) || '(none)'}<br><b>Shipping:</b> ${esc(c.shipping)}</p>
    ${c.notes ? `<p><b>Notes:</b><br>${esc(c.notes).replace(/\n/g, '<br>')}</p>` : ''}`;
  const table = `<table style="border-collapse:collapse" border="1"><tr><th>Qty</th><th>Part</th><th>Each</th></tr>${rows}</table>
    <p><b>Parts subtotal: $${subtotal.toFixed(2)}</b> (before shipping)</p>`;
  const text = clean.map((i) => `${i.qty} x ${i.sku} ${i.title} ${money(i.price)}`).join('\n');

  const to = env.ORDER_TO || 'xiscontrols@gmail.com';
  try {
    await send(env, {
      to,
      replyTo: c.email,
      subject: `Order request: ${c.company} (${clean.length} item${clean.length > 1 ? 's' : ''})`,
      html: `<h2>New order request</h2>${details}${table}<p>Reply to this email to reach the customer.</p>`,
      text: `${c.name}, ${c.company}\n${c.email} ${c.phone}\n\n${text}\n\nShip to:\n${c.address}`,
    });
    await send(env, {
      to: c.email,
      replyTo: to,
      subject: 'We got your order request - XIS Controls',
      html: `<p>Thanks, ${esc(c.name)}. We'll check these parts against your machine and email an invoice with the exact shipping. If anything looks off, we'll call you first.</p>${table}<p>Questions? Call 919-412-9200 or reply to this email.</p><p>XIS Controls<br>Making Obsolescence Obsolete</p>`,
      text: `Thanks. We'll confirm your parts and send an invoice with exact shipping.\n\n${text}\n\nXIS Controls 919-412-9200`,
    });
  } catch (e) {
    console.error(e);
    return json({ error: 'send failed' }, 502);
  }
  return json({ ok: true });
}
