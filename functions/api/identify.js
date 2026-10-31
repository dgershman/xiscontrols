import { esc, json, send, validEmail } from './_mail.js';

const MAX_FILES = 6;
const MAX_TOTAL = 18 * 1024 * 1024;

function b64(buf) {
  let s = '';
  const bytes = new Uint8Array(buf);
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(s);
}

export async function onRequestPost({ request, env }) {
  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ error: 'bad request' }, 400);
  }
  if (form.get('website')) return json({ ok: true }); // honeypot
  const f = (k) => String(form.get(k) || '').trim().slice(0, 4000);
  const name = f('name'), email = f('email'), what = f('what');
  if (!name || !what || !validEmail(email)) return json({ error: 'invalid' }, 422);

  const files = form.getAll('photos').filter((x) => typeof x === 'object' && x.size).slice(0, MAX_FILES);
  let total = 0;
  const attachments = [];
  for (const [i, file] of files.entries()) {
    total += file.size;
    if (total > MAX_TOTAL) break;
    if (!String(file.type).startsWith('image/')) continue;
    attachments.push({ filename: `photo-${i + 1}.jpg`, content: b64(await file.arrayBuffer()) });
  }
  const html = `<h2>Help me identify</h2>
    <p><b>${esc(name)}</b>${f('company') ? `, ${esc(f('company'))}` : ''}<br>${esc(email)}${f('phone') ? ` &middot; ${esc(f('phone'))}` : ''}</p>
    <p><b>Machine:</b> ${esc(f('machine')) || '(not given)'}</p>
    <p><b>What's going on:</b><br>${esc(what).replace(/\n/g, '<br>')}</p>
    <p>${attachments.length} photo(s) attached.</p>`;
  try {
    await send(env, {
      to: env.ORDER_TO || 'xiscontrols@gmail.com',
      replyTo: email,
      subject: `Identify request: ${f('machine') || name}`,
      html,
      text: `${name} ${email} ${f('phone')}\n${f('machine')}\n\n${what}`,
      attachments,
    });
  } catch (e) {
    console.error(e);
    return json({ error: 'send failed' }, 502);
  }
  return json({ ok: true });
}
