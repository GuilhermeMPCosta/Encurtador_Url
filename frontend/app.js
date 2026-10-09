const API_BASE =
  new URLSearchParams(window.location.search).get("api") ||
  window.URL_SHORTENER_API ||
  "http://localhost:5000";
const HISTORY_KEY = "encurta.links";
const MAX_HISTORY = 5;

const form = document.querySelector("#shorten-form");
const input = document.querySelector("#url-input");
const submitButton = document.querySelector("#submit-button");
const buttonLabel = submitButton.querySelector(".button-label");
const clearButton = document.querySelector("#clear-button");
const formMessage = document.querySelector("#form-message");
const resultCard = document.querySelector("#result-card");
const resultUrl = document.querySelector("#result-url");
const copyButton = document.querySelector("#copy-button");
const historyList = document.querySelector("#history-list");
const historyCount = document.querySelector("#history-count");

let currentShortUrl = "";
let history = loadHistory();

function loadHistory() {
  try {
    const saved = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
    if (!Array.isArray(saved)) {
      throw new TypeError("O histórico salvo não tem o formato esperado.");
    }
    return saved.filter(
      (item) =>
        item &&
        typeof item.shortUrl === "string" &&
        typeof item.originalUrl === "string",
    );
  } catch (error) {
    console.warn("Não foi possível carregar o histórico de links.", error);
    return [];
  }
}

function saveHistory() {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  } catch (error) {
    console.error("Não foi possível salvar o histórico de links.", error);
    showMessage("O link foi criado, mas não foi possível salvar o histórico neste dispositivo.");
  }
}

function normalizeUrl(value) {
  const candidate = /^[a-zA-Z][a-zA-Z\d+.-]*:/.test(value)
    ? value
    : `https://${value}`;
  const parsed = new URL(candidate);

  if (!["http:", "https:"].includes(parsed.protocol) || !parsed.hostname) {
    throw new TypeError("Informe um endereço válido começando com http:// ou https://.");
  }

  return parsed.href;
}

function showMessage(message) {
  formMessage.textContent = message;
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  form.setAttribute("aria-busy", String(isLoading));
  buttonLabel.textContent = isLoading ? "Encurtando..." : "Encurtar link";
}

function renderHistory() {
  historyCount.textContent = `${history.length} ${history.length === 1 ? "link" : "links"}`;
  historyList.replaceChildren();

  if (history.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M10.2 13.8a4 4 0 0 0 5.66 0l2.12-2.12a4 4 0 0 0-5.66-5.66l-1.22 1.22" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
        <path d="M13.8 10.2a4 4 0 0 0-5.66 0l-2.12 2.12a4 4 0 0 0 5.66 5.66l1.22-1.22" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
      </svg>
      <span>Seus links encurtados vão aparecer aqui.</span>
    `;
    historyList.append(empty);
    return;
  }

  for (const item of history) {
    const row = document.createElement("article");
    row.className = "history-item";

    const icon = document.createElement("span");
    icon.className = "history-link-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.innerHTML = `
      <svg viewBox="0 0 20 20" fill="none">
        <path d="M8.5 11.5a3 3 0 0 0 4.24 0l1.59-1.59a3 3 0 0 0-4.24-4.24l-.92.92" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
        <path d="M11.5 8.5a3 3 0 0 0-4.24 0l-1.59 1.59a3 3 0 0 0 4.24 4.24l.92-.92" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
      </svg>
    `;

    const details = document.createElement("div");
    details.className = "history-details";

    const shortLink = document.createElement("a");
    shortLink.className = "history-short";
    shortLink.href = item.shortUrl;
    shortLink.target = "_blank";
    shortLink.rel = "noopener noreferrer";
    shortLink.textContent = item.shortUrl;
    shortLink.title = item.shortUrl;

    const originalLink = document.createElement("span");
    originalLink.className = "history-original";
    originalLink.textContent = item.originalUrl;
    originalLink.title = item.originalUrl;

    details.append(shortLink, originalLink);

    const copy = document.createElement("button");
    copy.className = "history-copy";
    copy.type = "button";
    copy.setAttribute("aria-label", `Copiar ${item.shortUrl}`);
    copy.innerHTML = `
      <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
        <rect x="7" y="7" width="9" height="10" rx="1.5" stroke="currentColor" stroke-width="1.5" />
        <path d="M13 7V4.5A1.5 1.5 0 0 0 11.5 3h-7A1.5 1.5 0 0 0 3 4.5v8A1.5 1.5 0 0 0 4.5 14H7" stroke="currentColor" stroke-width="1.5" />
      </svg>
    `;
    copy.addEventListener("click", () => copyToClipboard(item.shortUrl, copy));

    row.append(icon, details, copy);
    historyList.append(row);
  }
}

async function copyToClipboard(value, button) {
  const label = button.querySelector("span");
  const originalContent = button.innerHTML;
  try {
    await navigator.clipboard.writeText(value);
    if (label) {
      label.textContent = "Copiado!";
      window.setTimeout(() => {
        label.textContent = "Copiar";
      }, 1800);
    } else {
      button.classList.add("is-copied");
      button.innerHTML = `
        <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="m4.5 10 3.4 3.4 7.6-7.6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      `;
      button.setAttribute("aria-label", "Link copiado");
      window.setTimeout(() => {
        button.classList.remove("is-copied");
        button.innerHTML = originalContent;
        button.setAttribute("aria-label", `Copiar ${value}`);
      }, 1800);
    }
  } catch (error) {
    console.error("Não foi possível copiar o link.", error);
    showMessage("Não foi possível copiar automaticamente. Selecione e copie o link manualmente.");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage("");
  resultCard.hidden = true;

  let originalUrl;
  try {
    originalUrl = normalizeUrl(input.value.trim());
  } catch {
    showMessage("Digite um endereço válido. Exemplo: https://exemplo.com");
    input.focus();
    return;
  }

  setLoading(true);
  try {
    const response = await fetch(`${API_BASE.replace(/\/+$/, "")}/encurtar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: originalUrl }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Não foi possível encurtar este link.");
    }
    if (typeof data.url_encurtada !== "string" || !data.url_encurtada) {
      throw new Error("A resposta do servidor não trouxe o link encurtado.");
    }

    currentShortUrl = data.url_encurtada;
    resultUrl.href = currentShortUrl;
    resultUrl.textContent = currentShortUrl;
    resultCard.hidden = false;

    history = [
      { shortUrl: currentShortUrl, originalUrl },
      ...history.filter((item) => item.shortUrl !== currentShortUrl),
    ].slice(0, MAX_HISTORY);
    saveHistory();
    renderHistory();
  } catch (error) {
    console.error("Falha ao encurtar o link.", error);
    const isNetworkError = error instanceof TypeError;
    showMessage(
      isNetworkError
        ? "Não foi possível conectar ao serviço. Verifique se a API está rodando e permite acesso a esta página."
        : error.message,
    );
  } finally {
    setLoading(false);
  }
});

input.addEventListener("input", () => {
  clearButton.hidden = input.value.length === 0;
  if (formMessage.textContent) {
    showMessage("");
  }
});

clearButton.addEventListener("click", () => {
  input.value = "";
  clearButton.hidden = true;
  showMessage("");
  resultCard.hidden = true;
  input.focus();
});

copyButton.addEventListener("click", () => copyToClipboard(currentShortUrl, copyButton));

renderHistory();
