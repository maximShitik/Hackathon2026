const form = document.getElementById("chatForm");
const input = document.getElementById("chatInput");
const messages = document.getElementById("messages");

const storesMessage = document.getElementById("storesMessage");
const storeChips = document.getElementById("storeChips");
const couponQuestion = document.getElementById("couponQuestion");

function addMessage(text, who) {
  const msg = document.createElement("div");
  msg.className = `msg ${who}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = who === "user" ? "אתה" : "בוט";

  msg.appendChild(bubble);
  msg.appendChild(meta);
  messages.appendChild(msg);

messages.scrollTop = messages.scrollHeight;
}

function showStores(stores) {
  storeChips.innerHTML = "";

  stores.forEach((s) => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.type = "button";
    btn.textContent = s;

    btn.addEventListener("click", () => {
      addMessage(`בחרתי: ${s}`, "user");

      // מעבירים את שאלת הקופון לסוף ומציגים
      messages.appendChild(couponQuestion);
      couponQuestion.hidden = false;

      messages.scrollTop = messages.scrollHeight;
    });

    storeChips.appendChild(btn);
  });

  // מעבירים את הבלוק של החנויות לסוף ומציגים
  messages.appendChild(storesMessage);
  storesMessage.hidden = false;

  // גלילה לתחתית (לא scrollIntoView)
  messages.scrollTop = messages.scrollHeight;
}


form.addEventListener("submit", (e) => {
  e.preventDefault();

  const text = input.value.trim();
  if (!text) return;

  // אם מתחילים חיפוש חדש, עדיף להסתיר מצבים קודמים
  storesMessage.hidden = true;
  couponQuestion.hidden = true;

  addMessage(text, "user");
  input.value = "";

  addMessage("מחפש... רגע 🙂", "bot");

  setTimeout(() => {
    showStores(["Nike", "Adidas", "Steimatzky"]);
  }, 500);
});
