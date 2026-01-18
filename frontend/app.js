// app.js — fetch streaming + render/patch protocol
const chatEl = document.getElementById("chat");
const formEl = document.getElementById("input-form");
const inputEl = document.getElementById("user-input");

const appEl = document.getElementById("app");
const toolLogEl = document.getElementById("tool-log");
console.log("test")
console.log(toolLogEl)
let conversation = [];

function addToolEntry(name, args) {
  const wrap = document.createElement("div");
  wrap.className = "tool-entry";

  const title = document.createElement("div");
  title.className = "tool-name";
  title.textContent = name || "(unknown tool)";

  const pre = document.createElement("pre");
  pre.textContent = typeof args === "string" ? args : JSON.stringify(args, null, 2);

  wrap.appendChild(title);
  wrap.appendChild(pre);
  toolLogEl.appendChild(wrap);
  toolLogEl.scrollTop = toolLogEl.scrollHeight;
}

function maybeLogToolCall(msg) {
  console.log("TOOL EVENT RECEIVED:", msg);
  if (msg.type === "tool_call_generated" && msg.data) {
    const name = msg.data.name;
    const args = msg.data.args ?? "";
    addToolEntry(name, args);
    return;
  }
  if (msg.type === "tool_output_generated" && msg.data) {
    const name = msg.data.name;
    const result = msg.data.result ?? "";
    addToolEntry(name, result);
    return;
  }
}

// Map of rendered items by id -> DOM element
const elById = new Map();

function scrollToBottom() {
  chatEl.scrollTop = chatEl.scrollHeight;
}

function createRow(item) {
  const div = document.createElement("div");
  div.className = `row ${item.kind || "meta"} ${item.role || ""}`.trim();
  if (item.dir) div.dir = item.dir;

  // text is what we render
  div.textContent = item.text ?? "";

  if (item.id) div.dataset.id = item.id;
  if (item.status) div.dataset.status = item.status;

  return div;
}

function renderItem(item) {
  if (item.replace_id) {
    const old = elById.get(item.replace_id);
    if (old) {
      old.remove();
      elById.delete(item.replace_id);
    }
  }

  const div = document.createElement("div");
  div.className = `row ${item.kind || "meta"} ${item.role || ""}`.trim();
  if (item.dir) div.dir = item.dir;

  div.textContent = item.text ?? "";

  if (item.id) {
    div.dataset.id = item.id;
    elById.set(item.id, div);
  }

  chatEl.appendChild(div);
  scrollToBottom();
}

function applyPatch(patch) {
  // Remove placeholder if requested
  if (patch.replace_id) {
    const old = elById.get(patch.replace_id);
    if (old) {
      old.remove();
      elById.delete(patch.replace_id);
    }
  }

  const div = elById.get(patch.id);
  if (!div) return;

  if (patch.op === "append_text") {
    div.textContent += patch.text || "";
  } else if (patch.op === "replace_text") {
    div.textContent = patch.text || "";
  }

  scrollToBottom();
}


function parseSseBuffer(buffer, onMsg) {
  buffer = buffer.replaceAll("\r\n", "\n");

  const parts = buffer.split("\n\n");
  const tail = parts.pop() ?? "";

  for (const part of parts) {
    for (const line of part.split("\n")) {
      if (!line.startsWith("data: ")) continue;

      const jsonStr = line.slice(6).trim();
      try {
        const msg = JSON.parse(jsonStr);
        maybeLogToolCall(msg);
        onMsg(msg);
      } catch (e) {
        console.warn("Failed to parse SSE JSON:", jsonStr, e);
      }
    }
  }
  return tail;
}

async function streamOnce() {
  const resp = await fetch("/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ conversation }),
  });

  if (!resp.ok || !resp.body) {
    renderItem({ kind: "meta", text: `HTTP ${resp.status}` });
    return;
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let buffer = "";
  let lastAssistantText = ""; // capture final assistant message for conversation history

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    buffer = parseSseBuffer(buffer, (msg) => {
      if (msg.type === "render") {
        renderItem(msg.data);

        // If backend sends full assistant text in render, capture it
        if (msg.data?.kind === "message" && msg.data?.role === "assistant" && typeof msg.data?.text === "string") {
          lastAssistantText = msg.data.text;
        }
      } else if (msg.type === "patch") {
        applyPatch(msg.data);

        // If patch targets assistant message, keep an updated copy for history
        const div = elById.get(msg.data?.id);
        if (div && div.className.includes("assistant")) {
          lastAssistantText = div.textContent;
        }
      } else if (msg.type === "placeholder") {
        renderItem(msg.data);
      } else if (msg.type === "done") {
        // stream end marker from backend (optional)
      } else if (msg.type === "error") {
        renderItem({ kind: "meta", text: `Error: ${msg.data?.message || "unknown"}` });
      }
    });
  }

  // Add assistant output into conversation so next turn has context
  if (lastAssistantText.trim()) {
    conversation.push({ role: "assistant", content: lastAssistantText });
  }
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = (inputEl.value || "").trim();
  if (!text) return;

  // Optimistically render user's message (fast UX)
  renderItem({ kind: "message", role: "user", text });

  // Update conversation (stateless backend)
  conversation.push({ role: "user", content: text });

  inputEl.value = "";
  inputEl.focus();

  inputEl.disabled = true;
  formEl.querySelector("button")?.setAttribute("disabled", "true");

  try {
    await streamOnce();
  } finally {
    inputEl.disabled = false;
    formEl.querySelector("button")?.removeAttribute("disabled");
  }
});