(function () {
  function initOilTracker() {
    const shell = document.querySelector("[data-oil-tracker-shell]");
    if (!shell) {
      return;
    }

    const specEl = shell.querySelector("#oil-tracker-spec");
    const configEl = shell.querySelector("#oil-tracker-config");
    const chartEl = shell.querySelector("[data-oil-chart]");
    const windowSelect = shell.querySelector("[data-oil-window]");
    const tagSelect = shell.querySelector("[data-oil-tags]");
    const clearButton = shell.querySelector("[data-oil-clear]");
    const status = shell.querySelector("[data-oil-status]");
    const backdrop = shell.querySelector("[data-oil-backdrop]");
    const popup = shell.querySelector("[data-oil-popup]");
    const popupContent = shell.querySelector("[data-oil-popup-content]");
    const closeButton = shell.querySelector("[data-oil-close]");

    if (!specEl || !configEl || !chartEl || !windowSelect || !tagSelect || !clearButton || !status || !backdrop || !popup || !popupContent || !closeButton) {
      return;
    }

    if (typeof vegaEmbed === "undefined") {
      window.setTimeout(initOilTracker, 50);
      return;
    }

    const baseSpec = JSON.parse(specEl.textContent);
    const config = JSON.parse(configEl.textContent);
    const windowMap = {
      recent: { label: "Mid-1970s onward", start: "1974-01-01", end: null },
      full: { label: "Full history", start: null, end: null },
      iran80s: { label: "1980s Gulf conflicts", start: "1978-01-01", end: "1989-12-31" },
      midEast2020s: { label: "2020s Middle East conflicts", start: "2020-01-01", end: null },
    };

    const defaultWindow = config.defaultWindow || "recent";
    windowSelect.value = defaultWindow;

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function parseDateOnly(value) {
      if (value === null || value === undefined || value === "") {
        return null;
      }

      const parts = String(value).slice(0, 10).split("-");
      if (parts.length !== 3) {
        return null;
      }

      const year = Number(parts[0]);
      const month = Number(parts[1]);
      const day = Number(parts[2]);
      if (!Number.isFinite(year) || !Number.isFinite(month) || !Number.isFinite(day)) {
        return null;
      }

      return new Date(Date.UTC(year, month - 1, day));
    }

    function formatDateOnly(value) {
      if (value instanceof Date && !Number.isNaN(value.valueOf())) {
        return new Intl.DateTimeFormat("en-US", {
          year: "numeric",
          month: "short",
          day: "2-digit",
          timeZone: "UTC",
        }).format(value);
      }

      const date = parseDateOnly(value);
      if (!date) {
        return "Unknown date";
      }

      return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "2-digit",
        timeZone: "UTC",
      }).format(date);
    }

    function closePopup() {
      popup.style.display = "none";
      backdrop.style.display = "none";
      popupContent.innerHTML = "";
    }

    function getSelectedTags() {
      return Array.from(tagSelect.selectedOptions)
        .map((option) => option.value)
        .filter(Boolean);
    }

    function inWindow(row, windowConfig) {
      if (!windowConfig.start && !windowConfig.end) {
        return true;
      }

      const rowDate = parseDateOnly(row.date);
      if (!rowDate) {
        return true;
      }

      if (windowConfig.start && rowDate < parseDateOnly(windowConfig.start)) {
        return false;
      }

      if (windowConfig.end) {
        const endDate = parseDateOnly(windowConfig.end);
        endDate.setUTCHours(23, 59, 59, 999);
        if (rowDate > endDate) {
          return false;
        }
      }

      return true;
    }

    function matchesTags(row, selectedTags) {
      if (!selectedTags.length) {
        return true;
      }

      const rowTags = String(row.tags ?? "")
        .split(";")
        .map((tag) => tag.trim())
        .filter(Boolean);

      if (!rowTags.length) {
        return false;
      }

      return selectedTags.some((tag) => rowTags.includes(tag));
    }

    function filteredSpec() {
      const spec = JSON.parse(JSON.stringify(baseSpec));
      const selectedTags = getSelectedTags();
      const windowConfig = windowMap[windowSelect.value] || windowMap.recent;

      for (const datasetName of Object.keys(spec.datasets || {})) {
        spec.datasets[datasetName] = spec.datasets[datasetName].filter((row) => {
          if (!inWindow(row, windowConfig)) {
            return false;
          }

          if (row.description) {
            return matchesTags(row, selectedTags);
          }

          return true;
        });
      }

      return spec;
    }

    function updateStatus() {
      const windowLabel = (windowMap[windowSelect.value] || windowMap.recent).label;
      const selectedTags = getSelectedTags();
      const tagLabel = selectedTags.length ? `tags: ${selectedTags.join(", ")}` : "all tags";

      status.textContent = `${windowLabel} · ${tagLabel}`;
    }

    function openPopup(datum, x, y) {
      const eventDate = formatDateOnly(datum.event_date);
      const priceDate = formatDateOnly(datum.date);
      const priceValue = Number(datum.price_usd_per_barrel);
      const price = Number.isFinite(priceValue)
        ? priceValue.toLocaleString(undefined, {
          style: "currency",
          currency: "USD",
          maximumFractionDigits: 2,
        }) + " / bbl"
        : "No price attached";
      const gapValue = Number(datum.days_from_price_date);
      const gapText = Number.isFinite(gapValue)
        ? `${escapeHtml(gapValue)} day${gapValue === 1 ? "" : "s"} from price date`
        : "Matched to nearest price date";
      const tags = String(datum.tags ?? "")
        .split(";")
        .map((tag) => tag.trim())
        .filter(Boolean)
        .map((tag) => `<span class="oil-tracker-tag-chip">${escapeHtml(tag)}</span>`)
        .join("") || `<span class="oil-tracker-tag-chip oil-tracker-tag-chip-empty">Uncategorized</span>`;

      popupContent.innerHTML = `
        <div class="oil-tracker-popup-topline">${escapeHtml(eventDate)} · ${escapeHtml(datum.countries)}</div>
        <div class="oil-tracker-popup-title">Event detail</div>
        <div class="oil-tracker-popup-text">${escapeHtml(datum.description)}</div>
        <div class="oil-tracker-popup-tags">
          <div class="oil-tracker-popup-tags-label">Tags</div>
          <div class="oil-tracker-tag-list">${tags}</div>
        </div>
        <div class="oil-tracker-popup-meta-grid">
          <div class="oil-tracker-popup-meta"><span>Matched price date</span><strong>${escapeHtml(priceDate)}</strong></div>
          <div class="oil-tracker-popup-meta"><span>Timing gap</span><strong>${escapeHtml(gapText)}</strong></div>
          <div class="oil-tracker-popup-meta"><span>Price</span><strong>${escapeHtml(price)}</strong></div>
        </div>
        ${datum.source ? `<div class="oil-tracker-popup-link"><a href="${escapeHtml(datum.source)}" target="_blank" rel="noopener noreferrer">Source</a></div>` : ""}
      `;

      backdrop.style.display = "block";
      popup.style.visibility = "hidden";
      popup.style.display = "block";

      const popupRect = popup.getBoundingClientRect();
      const left = Math.min(x + 16, window.innerWidth - popupRect.width - 12);
      const top = Math.min(y + 16, window.innerHeight - popupRect.height - 12);

      popup.style.left = `${Math.max(12, left)}px`;
      popup.style.top = `${Math.max(12, top)}px`;
      popup.style.visibility = "visible";
    }

    function renderChart() {
      updateStatus();
      closePopup();

      const spec = filteredSpec();
      chartEl.innerHTML = "";

      vegaEmbed(chartEl, spec, {
        actions: false,
        renderer: "canvas",
      }).then((result) => {
        result.view.addEventListener("click", (event, item) => {
          const datum = item && item.datum;
          if (datum && datum.description) {
            openPopup(datum, event.clientX, event.clientY);
          } else {
            closePopup();
          }
        });
      });
    }

    closeButton.addEventListener("click", closePopup);
    backdrop.addEventListener("click", closePopup);
    clearButton.addEventListener("click", () => {
      Array.from(tagSelect.options).forEach((option) => {
        option.selected = false;
      });
      renderChart();
    });
    windowSelect.addEventListener("change", renderChart);
    tagSelect.addEventListener("change", renderChart);
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closePopup();
      }
    });

    renderChart();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initOilTracker);
  } else {
    initOilTracker();
  }
})();
