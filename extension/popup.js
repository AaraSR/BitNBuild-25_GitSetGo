const LOCAL_URL = "http://localhost:8501/";

function isValidHttpUrl(string) {
  try {
    const u = new URL(string);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch (_) {
    return false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // gradient background
  document.body.style.background = "linear-gradient(135deg, #000046, #300038)";

  const netInput = document.getElementById("network-url");
  const openLocalBtn = document.getElementById("open-local");
  const openNetBtn = document.getElementById("open-network");
  const saveBtn = document.getElementById("save");
  const testBtn = document.getElementById("test");

  // load saved network URL
  chrome.storage.sync.get(["network_url"], (res) => {
    netInput.value = res.network_url || "";
  });

  // open local
  openLocalBtn.addEventListener("click", () => chrome.tabs.create({ url: LOCAL_URL }));

  // open network
  openNetBtn.addEventListener("click", () => openNetworkUrl(netInput.value));

  // save
  saveBtn.addEventListener("click", () => {
    const url = netInput.value.trim();
    if (!isValidHttpUrl(url)) {
      alert("Enter a valid URL (http://...)");
      return;
    }
    chrome.storage.sync.set({ network_url: url }, () => {
      saveBtn.textContent = "Saved ✅";
      setTimeout(() => (saveBtn.textContent = "Save Network"), 1200);
    });
  });

  // test
  testBtn.addEventListener("click", () => openNetworkUrl(netInput.value));

  // press Enter in textbox → open network URL
  netInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      openNetworkUrl(netInput.value);
    }
  });

  function openNetworkUrl(url) {
    const trimmed = (url || "").trim();
    if (!isValidHttpUrl(trimmed)) {
      alert("Please enter a valid network URL (http://...)");
      return;
    }
    chrome.tabs.create({ url: trimmed });
  }
});
