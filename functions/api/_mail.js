// Shared mail helper for Cloudflare Pages Functions. Uses Resend (https://resend.com).
// Required env vars (Cloudflare Pages > Settings > Environment variables):
//   RESEND_API_KEY   API key from Resend
//   MAIL_FROM        e.g. "XIS Controls <orders@xiscontrols.com>" (domain must be verified in Resend)
//   ORDER_TO         where requests go, defaults to xiscontrols@gmail.com

export const esc = (s) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

export const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

export async function send(env, { to, replyTo, subject, html, text, attachments }) {
  if (!env.RESEND_API_KEY || !env.MAIL_FROM) throw new Error('mail not configured');
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.MAIL_FROM,
      to: Array.isArray(to) ? to : [to],
      reply_to: replyTo,
      subject,
      html,
      text,
      attachments,
    }),
  });
  if (!res.ok) throw new Error(`resend ${res.status}: ${await res.text()}`);
}

export const validEmail = (s) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(s || ''));
