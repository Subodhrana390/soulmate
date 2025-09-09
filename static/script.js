/* ---------- Navigation ---------- */
const screens = [...document.querySelectorAll(".screen")];
const navButtons = [...document.querySelectorAll(".nav")];
navButtons.forEach(btn => {
  btn.onclick = () => {
    navButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const id = btn.dataset.screen;
    screens.forEach(s => s.classList.toggle("visible", s.id === id));
  };
});

/* ---------- Notepad (localStorage) ---------- */
const notesEl = document.getElementById("notes");
const saveNotesBtn = document.getElementById("saveNotes");
const clearNotesBtn = document.getElementById("clearNotes");
const notesStatus = document.getElementById("notesStatus");
notesEl.value = localStorage.getItem("soultalk_notes") || "";
saveNotesBtn.onclick = () => {
  localStorage.setItem("soultalk_notes", notesEl.value.trim());
  notesStatus.textContent = "✅ Saved locally.";
  setTimeout(() => (notesStatus.textContent = ""), 1800);
};
clearNotesBtn.onclick = () => {
  notesEl.value = "";
  localStorage.removeItem("soultalk_notes");
  notesStatus.textContent = "🗑️ Cleared.";
  setTimeout(() => (notesStatus.textContent = ""), 1500);
};

/* ---------- Chat Assistant (rule-based demo) ---------- */
const chatWindow = document.getElementById("chatWindow");
const chatInput  = document.getElementById("chatInput");
const sendBtn    = document.getElementById("sendBtn");
const micBtn     = document.getElementById("micBtn");
let lastInputType = "text"; // "voice" or "text"

function getStyle() {
  return document.querySelector('input[name="style"]:checked').value;
}
function addBubble(role, text) {
  const div = document.createElement("div");
  div.className = `bubble ${role}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
function ruleBasedReply(msg, style) {
  const m = msg.toLowerCase();
  let base;
  if (m.includes("sad") || m.includes("down")) {
    base = "I’m sorry you’re feeling low. You’re not alone, and this moment will pass.";
  } else if (m.includes("happy") || m.includes("great") || m.includes("good")) {
    base = "That’s lovely to hear! Keep the good vibes flowing ✨";
  } else if (m.includes("anxious") || m.includes("stress")) {
    base = "Try a slow breath with me: inhale 4, hold 7, exhale 8. You’ve got this.";
  } else {
    base = "I hear you. Thank you for sharing. Tell me a bit more?";
  }
  if (style === "Motivational") {
    return "🔥 " + base.replace("I hear you. ", "Remember, ").replace("You’re not alone, ", "");
  }
  if (style === "Therapist") {
    return "💙 " + base + " What happened just before you felt this way?";
  }
  return "🌷 " + base;
}
function speak(text) {
  if (!("speechSynthesis" in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1; utter.pitch = 1;
  speechSynthesis.speak(utter);
}
function handleSend() {
  const msg = chatInput.value.trim();
  if (!msg) return;
  addBubble("user", msg);
  const reply = ruleBasedReply(msg, getStyle());
  setTimeout(() => {
    addBubble("ai", reply);
    if (lastInputType === "voice") speak(reply); // speak only when user spoke
  }, 250);
  chatInput.value = "";
  lastInputType = "text";
}
sendBtn.onclick = handleSend;
chatInput.addEventListener("keydown", e => {
  if (e.key === "Enter") handleSend();
});

/* ---------- Speech to Text (Improved) ---------- */
let rec;

// 🎤 Language selector (English default)
let selectedLang = "en-US";  // change default if you want Hindi
// Example: "hi-IN" (Hindi), "pa-IN" (Punjabi), "en-GB" (UK English)

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  rec = new SR();
  rec.lang = selectedLang;
  rec.interimResults = false;
  rec.maxAlternatives = 1;

  rec.onresult = e => {
    const text = e.results[0][0].transcript;
    chatInput.value = text;
    lastInputType = "voice";
    handleSend(); // auto send after speaking
  };

  rec.onerror = (e) => {
    console.error("Speech Recognition Error:", e.error);
    if (e.error === "no-speech") {
      alert("🎤 No speech detected. Please try again.");
    } else if (e.error === "audio-capture") {
      alert("🎤 No microphone found. Please check your mic settings.");
    } else if (e.error === "not-allowed") {
      alert("🎤 Permission denied. Please allow microphone access.");
    } else {
      alert("⚠️ Could not understand audio. Please try again.");
    }
  };
} else {
  micBtn.disabled = true;
  micBtn.title = "Speech recognition not supported in this browser.";
}
micBtn.onclick = () => rec && rec.start();

/* ---------- Affirmations ---------- */
const AFFIRM = [
  "You are stronger than you think.",
  "Every day is a fresh start.",
  "Your feelings are valid.",
  "You are enough, just as you are.",
  "Good things are coming your way."
];
document.getElementById("nextAffirmation").onclick = () => {
  const text = AFFIRM[Math.floor(Math.random()*AFFIRM.length)];
  document.getElementById("affirmation").textContent = text;
};

/* ---------- Health Tips ---------- */
const TIPS = [
  "Drink 8 glasses of water today 💧",
  "Take a 5-minute stretch break 🧘",
  "Go for a 10-minute walk 🚶",
  "Eat a colorful plate of veggies 🍎🥕",
  "Try 4-7-8 breathing to relax 🌬️"
];
document.getElementById("nextTip").onclick = () => {
  const text = TIPS[Math.floor(Math.random()*TIPS.length)];
  document.getElementById("healthTip").textContent = text;
};

/* ---------- Music by Mood ---------- */
const SONGS = {
  low: [
    { title:"Chill Lofi Beats", link:"https://www.youtube.com/watch?v=jfKfPfyJRdk" },
    { title:"Soft Piano Calm", link:"https://www.youtube.com/watch?v=lFcSrYw-ARY" }
  ],
  balanced: [
    { title:"Focus / Study Mix", link:"https://www.youtube.com/watch?v=WPni755-Krg" },
    { title:"Indie Good Vibes", link:"https://www.youtube.com/watch?v=IxxstCcJlsc" }
  ],
  high: [
    { title:"Feel-Good Pop", link:"https://www.youtube.com/watch?v=fRh_vgS2dFE" },
    { title:"Dance / EDM Energy", link:"https://www.youtube.com/watch?v=60ItHLz5WEA" }
  ]
};
const moodSlider = document.getElementById("moodSlider");
const moodEmoji  = document.getElementById("moodEmoji");
const moodLabel  = document.getElementById("moodLabel");
const songList   = document.getElementById("songList");
function renderSongs(level){
  songList.innerHTML = "";
  SONGS[level].forEach(s => {
    const c = document.createElement("div");
    c.className = "card";
    c.innerHTML = `<div>${s.title}</div><a href="${s.link}" target="_blank">Play ▶</a>`;
    songList.appendChild(c);
  });
}
function moodUI(v){
  let level, emoji, label;
  if (v <= 3){ level="low"; emoji="😔"; label="Low"; }
  else if (v <= 7){ level="balanced"; emoji="🙂"; label="Balanced"; }
  else { level="high"; emoji="😄"; label="High"; }
  moodEmoji.textContent = emoji;
  moodLabel.textContent = label;
  renderSongs(level);
}
moodSlider.oninput = e => moodUI(+e.target.value);
moodUI(+moodSlider.value);

/* ---------- Breathing Timer (4-7-8) ---------- */
const circle = document.getElementById("timerCircle");
document.getElementById("startBreath").onclick = async () => {
  const phase = async (text, secs) => {
    circle.textContent = text;
    circle.animate([{transform:"scale(1)"},{transform:"scale(1.1)"},{transform:"scale(1)"}],
                   {duration: secs*1000, easing:"ease-in-out"});
    await new Promise(r => setTimeout(r, secs*1000));
  };
  await phase("Inhale 4", 4);
  await phase("Hold 7", 7);
  await phase("Exhale 8", 8);
  circle.textContent = "Done";
};
