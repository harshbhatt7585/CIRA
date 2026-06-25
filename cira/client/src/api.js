// Browser-facing API helpers.
//
// The React app owns the UI/state flow. Azure/OpenAI requests still go through
// the same-origin Vercel/FastAPI route so API keys remain server-side.
const API_BASE =
  import.meta.env.VITE_API_BASE ??
  (import.meta.env.DEV ? `http://${window.location.hostname}:8000` : '');

async function requestJson(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.json();
}

export function loadPlaybook(subcategoryId) {
  return requestJson(`/api/playbook/${subcategoryId}`);
}

export function sendChatMessage(payload) {
  return requestJson('/api/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
