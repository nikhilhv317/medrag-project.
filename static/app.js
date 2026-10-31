// MedRAG UI: talks to api.py. No build step, no framework.
const $ = (sel) => document.querySelector(sel);
const state = { token: sessionStorage.getItem("medrag-token") || "", info: null, loaded: {}, history: [] };
const HISTORY_TURNS = 3; // earlier questions and answers sent with each question, so follow-ups work

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// Report Markdown is rendered (and sanitised) when the CDN libraries loaded; otherwise shown as plain text.
function markdown(text) {
  if (window.marked && window.DOMPurify) return `<div class="md">${DOMPurify.sanitize(marked.parse(text))}</div>`;
  return `<pre>${esc(text)}</pre>`;
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(path, { ...options, headers });
  if (res.status === 401 && path !== "/api/login") { showLogin(); throw new Error("Sign in first"); }
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch { /* not JSON */ }
    throw new Error(detail);
  }
  return res;
}
const getJSON = async (path) => (await api(path)).json();

function table(rows, columns) {
  if (!rows.length) return '<p class="muted">Nothing to show.</p>';
  columns = columns || Object.keys(rows[0]);
  const cell = (v) => (typeof v === "string" && /^\d{4}-\d\d-\d\dT/.test(v) ? v.slice(0, 10) : v);
  const head = columns.map((c) => `<th>${esc(c)}</th>`).join("");
  const body = rows.map((r) => `<tr>${columns.map((c) => `<td>${esc(cell(r[c]))}</td>`).join("")}</tr>`).join("");
  return `<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}

// ---------------- sign-in ----------------
function showLogin() {
  $("#app").classList.add("hidden");
  $("#login").classList.remove("hidden");
}

$("#login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(e.target);
  $("#login-error").textContent = "";
  try {
    const res = await api("/api/login", { method: "POST", body: JSON.stringify(Object.fromEntries(form)) });
    state.token = (await res.json()).token;
    sessionStorage.setItem("medrag-token", state.token);
    e.target.reset();
    start();
  } catch (err) {
    $("#login-error").textContent = err.message;
  }
});

$("#logout").addEventListener("click", async () => {
  await api("/api/logout", { method: "POST" }).catch(() => {});
  state.token = "";
  sessionStorage.removeItem("medrag-token");
  showLogin();
});

// ---------------- settings ----------------
const settings = () => ({
  llm: $("#llm").value.trim() || null, mode: $("#mode").value, top_k: Number($("#topk").value), index: $("#index").value,
});
const indexParam = () => `index=${encodeURIComponent($("#index").value)}`;

async function start() {
  try {
    state.info = await getJSON("/api/info");
  } catch (err) {
    if (err.message !== "Sign in first") document.body.innerHTML = `<p class="error" style="padding:16px">${esc(err.message)}</p>`;
    return;
  }
  const info = state.info;
  $("#login").classList.add("hidden");
  $("#app").classList.remove("hidden");
  $("#index").innerHTML = info.indexes.map((i) => `<option ${i.name === info.default_index ? "selected" : ""}>${esc(i.name)}</option>`).join("");
  $("#mode").innerHTML = info.modes.map((m) => `<option ${m === "hybrid+rerank" ? "selected" : ""}>${esc(m)}</option>`).join("");
  $("#llm").value = info.llm;
  $("#topk").value = info.top_k;
  $("#topk-value").textContent = info.top_k;
  showIndexInfo();
  $("#whoami").textContent = info.auth ? `Signed in as ${info.user.username} (${info.user.role})`
    : "Local mode: no sign-in. Set USERS_FILE to require one.";
  $("#logout").classList.toggle("hidden", !info.auth);
  $("#patient-q").disabled = !info.user.sees_records;
  if (!info.user.sees_records) $("#patient-results").innerHTML =
    `<p class="muted">Your role (${esc(info.user.role)}) does not give access to individual patient records.</p>`;
}

function showIndexInfo() {
  const i = state.info.indexes.find((x) => x.name === $("#index").value);
  if (!i) { $("#index-info").textContent = ""; return; }
  const pending = i.in_use && i.in_use !== i.built_at ? " · newer version loading…" : "";
  $("#index-info").textContent = `${i.chunks.toLocaleString()} chunks · ${i.dim}-d · updated ${(i.in_use || i.built_at).replace("T", " ")}${pending}`;
}

// New records are indexed in the background (python -m medrag watch); keep the "updated" label current.
setInterval(async () => {
  if (!state.info || document.hidden) return;
  try { state.info = { ...state.info, indexes: (await getJSON("/api/info")).indexes }; showIndexInfo(); } catch { /* next time */ }
}, 30000);
$("#index").addEventListener("change", () => { showIndexInfo(); state.loaded = {}; });
$("#topk").addEventListener("input", (e) => { $("#topk-value").textContent = e.target.value; });

// ---------------- tabs ----------------
document.querySelectorAll(".tabs button").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".tabs button").forEach((x) => x.classList.toggle("active", x === b));
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.id === `tab-${b.dataset.tab}`));
  const load = { quality: loadQuality, eval: loadEvalRuns, audit: loadAudit }[b.dataset.tab];
  if (load && !state.loaded[b.dataset.tab]) { state.loaded[b.dataset.tab] = true; load(); }
}));

// ---------------- chat ----------------
function addMessage(role, html) {
  $(".messages .empty")?.remove();
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.innerHTML = html;
  $("#messages").append(div);
  div.scrollIntoView({ block: "end" });
  return div;
}

// [S1]-style citations become links to their source. Answers quote records, so the Markdown is rendered and then
// sanitised (DOMPurify); without the libraries the answer is shown as escaped plain text.
function answerHTML(text, id) {
  const cite = (s) => s.replace(/\[S(\d+)((?:\s*[,;]\s*S?\d+)*)\]/g, (m) =>
    m.replace(/S?(\d+)/g, (n, d) => `<a class="cite" data-target="${id}-s${d}">S${d}</a>`));
  if (window.marked && window.DOMPurify) return DOMPurify.sanitize(marked.parse(cite(text)));
  return `<div class="plain">${cite(esc(text))}</div>`;
}

$("#messages").addEventListener("click", (e) => {
  const link = e.target.closest(".cite");
  if (!link) return;
  const target = document.getElementById(link.dataset.target);
  if (!target) return;
  target.closest("details").open = true;
  target.scrollIntoView({ block: "center", behavior: "smooth" });
  target.classList.add("flash");
  setTimeout(() => target.classList.remove("flash"), 1500);
});

$("#question").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("#ask-form").requestSubmit(); }
});

$("#clear").addEventListener("click", () => {
  $("#messages").innerHTML = '<div class="empty muted">Chat cleared.</div>';
  state.history = [];
});

$("#ask-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = $("#question").value.trim();
  if (!question) return;
  $("#question").value = "";
  $("#send").disabled = true;
  addMessage("user", esc(question));
  const id = `a${Date.now()}`;
  const msg = addMessage("assistant", '<div class="meta">Searching the records...</div><div class="answer"></div>');
  const started = performance.now();
  let text = "", firstToken = 0;
  try {
    const res = await api("/api/ask", { method: "POST",
      body: JSON.stringify({ question, history: state.history.slice(-HISTORY_TURNS), ...settings() }) });
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();
      for (const line of lines.filter(Boolean)) {
        const ev = JSON.parse(line);
        if (ev.type === "meta") showMeta(msg, ev, id, started);
        else if (ev.type === "token") {
          if (!firstToken) firstToken = performance.now();
          text += ev.text;
          msg.querySelector(".answer").innerHTML = answerHTML(text, id);
        } else if (ev.type === "check") {
          showCheck(msg, ev.unverified_dates, text);
        } else if (ev.type === "error") {
          msg.querySelector(".answer").insertAdjacentHTML("beforeend", `<p class="error">Error: ${esc(ev.text)}</p>`);
        }
      }
    }
    if (text) state.history = [...state.history, { question, answer: text }].slice(-HISTORY_TURNS);
    const total = ((performance.now() - started) / 1000).toFixed(1);
    msg.querySelector(".answer").insertAdjacentHTML("afterend",
      `<div class="timing">${firstToken ? `first words after ${((firstToken - started) / 1000).toFixed(1)} s · ` : ""}done in ${total} s</div>`);
  } catch (err) {
    msg.querySelector(".meta").textContent = "";
    msg.querySelector(".answer").innerHTML = `<p class="error">Error: ${esc(err.message)}</p>`;
  } finally {
    $("#send").disabled = false;
    $("#question").focus();
  }
});

// The exact record of each patient in an overview, straight from the database (the LLM only summarises it).
function overviewHTML(o) {
  const who = [o.gender, o.age != null ? `age ${o.age}` : ""].filter(Boolean).join(", ");
  const rows = o.studies.map((s) => `<tr class="${s.abnormal ? "abnormal" : ""}"><td>${esc(s.date)}</td>
      <td>${esc(s.modality)} ${esc(s.body_part)}</td><td>${esc(s.priority)}</td><td>${esc(s.finding)}</td>
      <td>${esc(s.recommendation)}</td></tr>`).join("");
  const docs = o.documents.length ? `<h4>Documents (${o.documents.length})</h4>
      <p class="muted small">Public documents linked to this synthetic patient for testing; they may not match the patient.</p>
      <ul class="docs">${o.documents.map((d) => `<li><b>${esc(d.date)}</b> · ${esc(d.title)} · ${esc(d.specialty)}
        ${d.conclusion ? `<br><span class="muted">${esc(d.conclusion)}</span>` : ""}</li>`).join("")}</ul>` : "";
  return `<div class="record"><div class="record-head"><b>${esc(o.name)}</b> · ${esc(o.mrn)}${who ? " · " + esc(who) : ""}
      ${o.conditions ? `<br><span class="muted small">Conditions: ${esc(o.conditions)}</span>` : ""}
      <br><span class="muted small">${o.studies.length} studies, ${o.abnormal} with abnormal findings (highlighted), newest first</span></div>
      <div class="table-wrap"><table><thead><tr><th>Date</th><th>Study</th><th>Priority</th><th>Finding</th><th>Recommendation</th></tr></thead>
      <tbody>${rows}</tbody></table></div>${docs}</div>`;
}

function showCheck(msg, unverified, text) {
  const mentioned = /\b\d{4}-\d{2}-\d{2}\b/.test(text);
  const html = unverified.length
    ? `<p class="flag warn">Check against the table below: ${unverified.map(esc).join("; ")}.</p>`
    : mentioned ? '<p class="flag ok">Every date in this summary matches the patient\'s records.</p>' : "";
  msg.querySelector(".answer").insertAdjacentHTML("afterend", html);
}

function showMeta(msg, ev, id, started) {
  const secs = ((performance.now() - started) / 1000).toFixed(1);
  msg.querySelector(".meta").textContent = `Filters: ${ev.filters}${ev.notes.length ? " · " + ev.notes.join(" ") : ""} · found in ${secs} s`;
  if (ev.overview) {
    msg.insertAdjacentHTML("beforeend", `<details class="records" open><summary>Patient record (exact, from the database)</summary>
      ${ev.overview.map(overviewHTML).join("")}</details>`);
  }
  const sources = ev.sources.map((s, i) => `<div class="source" id="${id}-s${i + 1}">
      <b>[S${i + 1}]</b> ${esc(s.doc_id)} <span class="muted small">(${esc(s.via)}, score ${Number(s.score).toFixed(3)})</span>
      <pre>${esc(s.text)}</pre></div>`).join("");
  const cols = ["doc_id", "via", "patient_name", "mrn", "study_date", "modality", "body_part", "priority"];
  const rows = ev.sources.map((s, i) => ({ src: `S${i + 1}`, ...s }));
  msg.insertAdjacentHTML("beforeend", `<details><summary>Sources (${ev.sources.length})</summary>
      ${table(rows, ["src", ...cols.filter((c) => c in (ev.sources[0] || {}))])}${sources}</details>`
    + (ev.facts ? `<details><summary>Computed facts (exact database counts)</summary><pre>${esc(ev.facts)}</pre></details>` : ""));
}

// ---------------- patients ----------------
$("#patient-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = $("#patient-q").value.trim();
  if (!q) return;
  const out = $("#patient-results");
  out.innerHTML = '<p class="muted">Searching...</p>';
  try {
    const r = await getJSON(`/api/patients?q=${encodeURIComponent(q)}&${indexParam()}`);
    out.innerHTML = `<p>${r.total} match(es)${r.total > r.patients.length ? `, showing ${r.patients.length}` : ""}</p>`
      + r.patients.map((p) => `<details class="card" data-id="${p.patient_id}"><summary>${esc(p.patient_name)} · ${esc(p.mrn)} · id ${p.patient_id}</summary>
          <div class="detail muted">Loading...</div></details>`).join("");
    out.querySelectorAll("details").forEach((d) => d.addEventListener("toggle", () => d.open && loadPatient(d), { once: true }));
    if (r.patients.length === 1) out.querySelector("details").open = true;
  } catch (err) {
    out.innerHTML = `<p class="error">${esc(err.message)}</p>`;
  }
});

async function loadPatient(details) {
  const box = details.querySelector(".detail");
  try {
    const p = await getJSON(`/api/patients/${details.dataset.id}?${indexParam()}`);
    box.classList.remove("muted");
    box.innerHTML = `<pre>${esc(p.profile)}</pre>
      <h4>Studies (${p.studies.length})</h4>${table(p.studies)}`
      + (p.documents.length ? `<h4>Uploaded documents (${p.documents.length})</h4>` + p.documents.map((d) =>
        `<details><summary>${esc(d.date)} · ${esc(d.title)} · ${esc(d.specialty)} · source: ${esc(d.source)}</summary><pre>${esc(d.text)}</pre></details>`).join("") : "");
  } catch (err) {
    box.innerHTML = `<p class="error">${esc(err.message)}</p>`;
  }
}

// ---------------- data quality, evaluation, audit ----------------
async function loadQuality() {
  const out = $("#quality");
  out.innerHTML = '<p class="muted">Loading...</p>';
  try {
    const q = await getJSON(`/api/quality?${indexParam()}`);
    out.innerHTML = `<div class="metrics">
        <div class="metric"><b>${q.patients.toLocaleString()}</b>patients</div>
        <div class="metric"><b>${q.studies.toLocaleString()}</b>studies indexed</div>
        <div class="metric"><b>${q.chunks.toLocaleString()}</b>chunks</div></div>`
      + Object.entries(q.reports).map(([name, text], i) =>
        `<details class="card" ${i === 0 ? "open" : ""}><summary>${esc(name)}</summary>${markdown(text)}</details>`).join("");
  } catch (err) {
    out.innerHTML = `<p class="error">${esc(err.message)}</p>`;
  }
}

async function loadEvalRuns() {
  try {
    const runs = await getJSON("/api/evals");
    if (!runs.length) { $("#eval").innerHTML = '<p class="muted">No evaluation yet. Run <code>python -m medrag eval</code>.</p>'; return; }
    $("#eval-run").innerHTML = runs.map((r) => `<option>${esc(r)}</option>`).join("");
    loadEval();
  } catch (err) {
    $("#eval").innerHTML = `<p class="error">${esc(err.message)}</p>`;
  }
}
$("#eval-run").addEventListener("change", loadEval);

async function loadEval() {
  const out = $("#eval");
  out.innerHTML = '<p class="muted">Loading...</p>';
  try {
    const r = await getJSON(`/api/evals/${encodeURIComponent($("#eval-run").value)}`);
    out.innerHTML = `<div class="card">${markdown(r.summary)}</div>`
      + (r.answers.length ? `<h3>Answers (${r.answers.length})</h3>${table(r.answers)}` : "");
  } catch (err) {
    out.innerHTML = `<p class="error">${esc(err.message)}</p>`;
  }
}

async function loadAudit() {
  const out = $("#audit");
  out.innerHTML = '<p class="muted">Loading...</p>';
  try {
    const a = await getJSON("/api/audit");
    out.innerHTML = `<p>${a.total.toLocaleString()} audit events${a.total > a.events.length ? ` (latest ${a.events.length} shown)` : ""}</p>
      ${table(a.events)}<h3>Request metrics</h3><div class="card">${markdown(a.metrics)}</div>`;
  } catch (err) {
    out.innerHTML = `<p class="muted">${esc(err.message)}</p>`;
  }
}

start();
