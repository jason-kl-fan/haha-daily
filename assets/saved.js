(function () {
  const STORAGE_KEY = 'hahaDailySavedStories';

  function loadSaved() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch (err) {
      return [];
    }
  }

  function saveSaved(items) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }

  function normalize(text) {
    return (text || '').replace(/\s+/g, ' ').trim();
  }

  function slug(text) {
    return normalize(text)
      .toLowerCase()
      .replace(/[^\p{L}\p{N}]+/gu, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 80);
  }

  function articleToStory(article) {
    const title = normalize(article.querySelector('h3')?.textContent || '未命名報導');
    const takeaway = normalize(article.querySelector('p strong')?.textContent || '');
    const summary = normalize(article.querySelector('p.small')?.textContent || '');
    const sourceWrap = article.querySelector('.source');
    const source = normalize(sourceWrap?.querySelector('strong')?.textContent || '未知來源');
    const linkEl = sourceWrap?.querySelector('a[href]');
    const sourceUrl = linkEl?.href || '';
    const pageUrl = new URL(window.location.href);
    pageUrl.hash = slug(title);

    const crumbs = Array.from(document.querySelectorAll('.pill')).map((el) => normalize(el.textContent));
    const topic = crumbs.find((text) => text && text !== '哈哈狗報') || document.title.split('｜').pop()?.trim() || '未分類';
    const dateMatch = document.title.match(/(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日/);
    const date = dateMatch ? `${dateMatch[1]}-${String(dateMatch[2]).padStart(2, '0')}-${String(dateMatch[3]).padStart(2, '0')}` : '';

    return {
      id: `${window.location.pathname}::${slug(title)}`,
      title,
      takeaway,
      summary,
      source,
      sourceUrl,
      pageUrl: pageUrl.toString(),
      pagePath: window.location.pathname,
      topic,
      date,
      savedAt: new Date().toISOString()
    };
  }

  function isSaved(id) {
    return loadSaved().some((item) => item.id === id);
  }

  function toggleStory(story) {
    const items = loadSaved();
    const idx = items.findIndex((item) => item.id === story.id);
    if (idx >= 0) {
      items.splice(idx, 1);
      saveSaved(items);
      return false;
    }
    items.unshift(story);
    saveSaved(items);
    return true;
  }

  function updateButton(button, active) {
    button.dataset.saved = active ? 'true' : 'false';
    button.setAttribute('aria-pressed', active ? 'true' : 'false');
    button.innerHTML = active ? '★ 已收藏' : '☆ 加入 Saved';
  }

  function enhanceStories() {
    const articles = document.querySelectorAll('article.story');
    articles.forEach((article) => {
      if (article.querySelector('.save-btn')) return;
      const story = articleToStory(article);
      article.id = article.id || slug(story.title);

      const toolbar = document.createElement('div');
      toolbar.className = 'story-toolbar';

      const button = document.createElement('button');
      button.className = 'save-btn';
      button.type = 'button';
      updateButton(button, isSaved(story.id));
      button.addEventListener('click', function () {
        const next = toggleStory(story);
        updateButton(button, next);
      });

      toolbar.appendChild(button);
      article.prepend(toolbar);
    });
  }

  function escapeHtml(text) {
    return String(text || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderSavedPage() {
    const mount = document.querySelector('[data-saved-list]');
    const empty = document.querySelector('[data-saved-empty]');
    if (!mount) return;

    const items = loadSaved();
    if (!items.length) {
      if (empty) empty.hidden = false;
      mount.innerHTML = '';
      return;
    }

    if (empty) empty.hidden = true;
    mount.innerHTML = items.map((item) => `
      <article class="story saved-story" id="saved-${escapeHtml(slug(item.title))}">
        <div class="story-toolbar">
          <div class="saved-meta">
            <span class="saved-tag">${escapeHtml(item.topic || '未分類')}</span>
            ${item.date ? `<span class="saved-date">${escapeHtml(item.date)}</span>` : ''}
          </div>
          <button class="save-btn" type="button" data-remove-id="${escapeHtml(item.id)}" data-saved="true" aria-pressed="true">★ 已收藏</button>
        </div>
        <h3>${escapeHtml(item.title)}</h3>
        ${item.takeaway ? `<p><strong>${escapeHtml(item.takeaway)}</strong></p>` : ''}
        ${item.summary ? `<p class="small">${escapeHtml(item.summary)}</p>` : ''}
        <p class="source">來源：<strong>${escapeHtml(item.source || '未知來源')}</strong>${item.sourceUrl ? ` · <a href="${escapeHtml(item.sourceUrl)}">原文連結</a>` : ''}${item.pageUrl ? ` · <a href="${escapeHtml(item.pageUrl)}">站內定位</a>` : ''}</p>
      </article>
    `).join('');

    mount.querySelectorAll('[data-remove-id]').forEach((button) => {
      button.addEventListener('click', function () {
        const id = button.getAttribute('data-remove-id');
        const next = loadSaved().filter((item) => item.id !== id);
        saveSaved(next);
        renderSavedPage();
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    enhanceStories();
    renderSavedPage();
  });
})();
