// read shared counts every two seconds without changing saved interests.
async function refreshCounts() {
  const status = document.querySelector("#count-status");
  try {
    const response = await fetch("/counts", { cache: "no-store", signal: AbortSignal.timeout(4000) });
    if (!response.ok) throw new Error("Counts unavailable");
    const states = await response.json();
    document.querySelectorAll("[data-post-id]").forEach((card) => {
      const state = states[card.dataset.postId];
      if (!state) return;
      card.querySelector("[data-count]").textContent = state.count;
      const button = card.querySelector("[data-interest]");
      button.textContent = state.interested ? "Remove interest" : "I'm interested";
      button.setAttribute("aria-pressed", String(state.interested));
    });
    status.textContent = "";
  } catch {
    status.textContent = "Counts could not update. Retrying automatically.";
  } finally {
    window.setTimeout(refreshCounts, 2000);
  }
}

refreshCounts();
