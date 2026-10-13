<div class="page-shell">
  <header class="topbar">
    <a class="brand" href="{{ url('/') }}" aria-label="encurta. início">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M10.2 13.8a4 4 0 0 0 5.66 0l2.12-2.12a4 4 0 0 0-5.66-5.66l-1.22 1.22" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          <path d="M13.8 10.2a4 4 0 0 0-5.66 0l-2.12 2.12a4 4 0 0 0 5.66 5.66l1.22-1.22" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </span>
      <span>encurta<span class="brand-period">.</span></span>
    </a>
    <span class="topbar-note">
      <span class="status-dot" aria-hidden="true"></span>
      Simples assim
    </span>
  </header>

  <main>
    <section class="hero" aria-labelledby="page-title">
      <div class="eyebrow">
        <span class="eyebrow-line" aria-hidden="true"></span>
        SEU LINK, SEM COMPLICAÇÃO
      </div>
      <h1 id="page-title">Links mais curtos,<br />ideias <span>mais longe.</span></h1>
      <p class="hero-copy">Transforme URLs enormes em links prontos para compartilhar.</p>
    </section>

    <section class="shortener-card" aria-label="Encurtar um link">
      <form wire:submit="shorten" novalidate>
        <label for="url-input">Cole seu link aqui</label>
        <div class="input-row">
          <div class="url-field">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M10.2 13.8a4 4 0 0 0 5.66 0l2.12-2.12a4 4 0 0 0-5.66-5.66l-1.22 1.22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
              <path d="M13.8 10.2a4 4 0 0 0-5.66 0l-2.12 2.12a4 4 0 0 0 5.66 5.66l1.22-1.22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            </svg>
            <input
              id="url-input"
              type="text"
              inputmode="url"
              autocomplete="url"
              placeholder="https://exemplo.com/seu-link-bem-grande"
              wire:model="url"
              aria-describedby="form-message"
              required
            />
            @if ($url !== '')
              <button class="clear-button" type="button" wire:click="clearUrl" aria-label="Limpar link">
                <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
                  <path d="m5 5 10 10M15 5 5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                </svg>
              </button>
            @endif
          </div>
          <button class="submit-button" type="submit" wire:loading.attr="disabled" wire:target="shorten">
            <span class="button-label" wire:loading.remove wire:target="shorten">Encurtar link</span>
            <span class="button-label" wire:loading wire:target="shorten">Aguarde...</span>
            <svg class="button-arrow" viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <path d="M4 10h12m-5-5 5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </button>
        </div>
        <p class="form-message" id="form-message" role="status" aria-live="polite">
          @error('url') {{ $message }} @enderror
          @if ($notice) {{ $notice }} @endif
        </p>
      </form>

      @if ($shortUrl)
        <div class="result-card" aria-live="polite">
          <div class="result-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="m5 12 4.5 4.5L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </div>
          <div class="result-content">
            <span class="result-label">Seu link está pronto</span>
            <a class="result-url" href="{{ $shortUrl }}" target="_blank" rel="noopener noreferrer">{{ $shortUrl }}</a>
          </div>
          <button class="copy-button" type="button" x-data x-on:click="navigator.clipboard.writeText(@js($shortUrl))">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
              <rect x="7" y="7" width="9" height="10" rx="1.5" stroke="currentColor" stroke-width="1.6" />
              <path d="M13 7V4.5A1.5 1.5 0 0 0 11.5 3h-7A1.5 1.5 0 0 0 3 4.5v8A1.5 1.5 0 0 0 4.5 14H7" stroke="currentColor" stroke-width="1.6" />
            </svg>
            <span>Copiar</span>
          </button>
        </div>
      @endif
    </section>

    <div class="trust-row">
      <span>
        <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M10 2.5 4 5v4.2c0 3.7 2.6 6.9 6 8.3 3.4-1.4 6-4.6 6-8.3V5l-6-2.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" />
          <path d="m7.5 9.8 1.7 1.7 3.5-3.7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        Links prontos em segundos
      </span>
      <span class="trust-divider" aria-hidden="true"></span>
      <span>
        <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M3 10h14M10 3v14M4.8 4.8l10.4 10.4m0-10.4L4.8 15.2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
        </svg>
        Grátis e sem cadastro
      </span>
    </div>

    <section class="history-section" aria-labelledby="history-title">
      <div class="section-heading">
        <div>
          <h2 id="history-title">Seus links recentes</h2>
          <p>Os últimos links que você encurtou neste dispositivo.</p>
        </div>
        <span class="history-count">0 links</span>
      </div>
      <div class="history-list">
        <div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M10.2 13.8a4 4 0 0 0 5.66 0l2.12-2.12a4 4 0 0 0-5.66-5.66l-1.22 1.22" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
            <path d="M13.8 10.2a4 4 0 0 0-5.66 0l-2.12 2.12a4 4 0 0 0 5.66 5.66l1.22-1.22" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
          </svg>
          <span>Seus links encurtados vão aparecer aqui.</span>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <span>Feito para compartilhar sem complicação.</span>
    <span class="footer-mark">encurta<span>.</span></span>
  </footer>
</div>
