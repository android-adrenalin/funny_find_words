#!/usr/bin/env python3
"""Сборка статических страниц сайта Funny Find Words.

Пишет рядом с собой: index.html, updates.html, privacy.html, terms.html, 404.html.
Тексты политики и условий берутся из privacy.md и terms.md в этой же папке.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).parent
PLAY_URL = (
    "https://play.google.com/store/apps/details"
    "?id=com.androidadrenalin.funny_find_words"
)
EMAIL = "android.adrenalin@outlook.com"

# Палитра плиток из lib/style/palette.dart (порядок — как в игровом логотипе).
PALETTE = [
    "#BD84A4", "#FFACB8", "#9898BC", "#487BA6", "#F2DCDC", "#A9BCF0", "#7FA9E0",
    "#2EBEC4", "#8DCEB9", "#BEC5BD", "#F4A259", "#E9C46A", "#90BE6D", "#C77DFF",
    "#F28482", "#8ECAE6",
]

# Небольшая сетка для первого экрана: подсвечено слово WORDS в первом столбце.
BOARD_LETTERS = "WAVEST" "ODLINE" "RUSTYK" "DAISYM" "SONGBT" "ATLASE"
BOARD_HIGHLIGHT = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)}

DECOR = """
    <div class="decor" aria-hidden="true">
      <i style="width:180px;height:180px;left:-60px;top:80px"></i>
      <i style="width:320px;height:320px;right:-110px;top:-80px"></i>
      <i style="width:120px;height:120px;left:12%;bottom:18%"></i>
      <i style="width:260px;height:260px;right:6%;bottom:-90px"></i>
      <u style="width:120px;left:6%;top:34%"></u>
      <u style="width:70px;left:22%;top:12%"></u>
      <u style="width:90px;right:10%;top:46%"></u>
      <u style="width:60px;right:18%;bottom:26%"></u>
    </div>
"""


def head(title: str, description: str, depth: str = "./") -> str:
    """Общая голова документа."""
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#10182F">
  <meta name="description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <title>{title}</title>
  <link rel="stylesheet" href="{depth}site.css">
</head>
<body>
{DECOR}<div class="page">"""


def nav() -> str:
    """Шапка сайта."""
    mark = "".join(
        f'<span style="--c:{color}"></span>' for color in PALETTE[:4]
    )
    return f"""
  <header class="nav">
    <a class="brand" href="./">
      <span class="mark" aria-hidden="true">{mark}</span>
      Funny Find Words
    </a>
    <nav>
      <a href="./updates.html">Обновления</a>
      <a href="./privacy.html">Политика</a>
      <a href="./terms.html">Условия</a>
    </nav>
  </header>"""


def foot() -> str:
    """Подвал сайта."""
    return f"""
  <footer class="foot">
    <span>© 2024–2026 AdrenalinAndroid · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
    <span class="links">
      <a href="{PLAY_URL}">Google Play</a>
      <a href="./privacy.html">Политика конфиденциальности</a>
      <a href="./terms.html">Условия использования</a>
    </span>
  </footer>
</div>
</body>
</html>
"""


def play_icon() -> str:
    """Белый треугольник «play» для кнопки."""
    return (
        '<svg width="14" height="16" viewBox="0 0 14 16" aria-hidden="true">'
        '<path fill="currentColor" d="M1 1.2v13.6c0 .5.5.8.9.5l11-6.8a.6.6 0 0 0 0-1L1.9.7'
        'C1.5.4 1 .7 1 1.2Z"/></svg>'
    )


def wordmark() -> str:
    """Логотип плитками: FUNNY / FIND WORDS."""
    words = ["FUNNY", "FIND", "WORDS"]
    tiles: list[str] = []
    index = 0
    for word in words:
        group = "".join(
            f'<span class="tile" style="--c:{PALETTE[(index + i) % len(PALETTE)]}">'
            f"{letter}</span>"
            for i, letter in enumerate(word)
        )
        index += len(word)
        tiles.append(f'<span class="grp">{group}</span>')
    return f'<h1 class="wordmark">{"".join(tiles)}</h1>'


def board() -> str:
    """Декоративное игровое поле."""
    cells = []
    for row in range(6):
        for col in range(6):
            letter = BOARD_LETTERS[row * 6 + col]
            if (row, col) in BOARD_HIGHLIGHT:
                color = PALETTE[row % len(PALETTE)]
                cells.append(f'<b class="on" style="--c:{color}">{letter}</b>')
            else:
                cells.append(f"<b>{letter}</b>")
    return '<div class="board" aria-hidden="true">' + "".join(cells) + "</div>"


def index_page() -> str:
    """Главная страница игры."""
    cards = [
        (
            PALETTE[11],
            "Восемь направлений",
            "Слова спрятаны по горизонтали, вертикали и диагоналям — "
            "путь можно вести в обе стороны.",
        ),
        (
            PALETTE[6],
            "Бонусные слова",
            "Незагаданные слова на сетке тоже засчитываются: за них дают монеты, "
            "а монеты можно обменять на подсказки.",
        ),
        (
            PALETTE[8],
            "Русский и английский",
            "Сто уровней на каждом языке: интерфейс и словари доступны "
            "на русском и английском.",
        ),
    ]
    cards_html = "".join(
        f"""
      <article class="card" style="--c:{color}">
        <h3>{title}</h3>
        <p>{text}</p>
      </article>"""
        for color, title, text in cards
    )

    body = f"""
{nav()}
  <main>
    <section class="hero">
      <div>
        <p class="eyebrow">Головоломка со словами</p>
        {wordmark()}
        <p class="tagline">Найди все слова!</p>
        <p class="lead">
          Слова спрятаны в сетке букв: ведите путь по клеткам — и найденное слово
          закрашивается. Сто уровней, бонусные слова и подсказки.
        </p>
        <div class="actions">
          <a class="btn btn-play" href="{PLAY_URL}">{play_icon()}Открыть в Google Play</a>
          <a class="btn btn-ghost" href="./updates.html">Что нового</a>
        </div>
        <p class="meta">
          <span>Бесплатно</span>
          <span class="dash" aria-hidden="true"></span>
          <span>Android</span>
          <span class="dash" aria-hidden="true"></span>
          <span>Версия <span data-version>1.1.1</span></span>
        </p>
      </div>
      {board()}
    </section>

    <section class="section" id="features">
      <h2>Как играть</h2>
      <div class="cards">{cards_html}
      </div>
    </section>

    <section class="section">
      <div class="ver">
        <div>
          <p class="label">Версия в Google Play</p>
          <p class="num" data-version>1.1.1</p>
          <p class="sub" data-published>Дата публикации уточняется…</p>
        </div>
        <a class="btn btn-ghost" href="./updates.html">Все обновления</a>
      </div>
    </section>
  </main>
{foot()}"""
    script = """
<script>
  // Дата приходит из version.json в виде ГГГГ-ММ-ДД, показываем её по-русски.
  function formatDate(value) {
    if (!value) { return ''; }
    var date = new Date(value + 'T00:00:00');
    if (isNaN(date)) { return value; }
    return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  // Версия и дата берутся из version.json, чтобы страница не устаревала.
  fetch('./version.json?ts=' + Date.now(), { cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)); })
    .then(function (c) {
      if (c.latestVersionName) {
        document.querySelectorAll('[data-version]').forEach(function (n) {
          n.textContent = c.latestVersionName;
        });
      }
      var published = document.querySelector('[data-published]');
      if (published && c.publishedAt) {
        published.textContent = 'Опубликовано ' + formatDate(c.publishedAt);
      }
    })
    .catch(function () {
      var published = document.querySelector('[data-published]');
      if (published) {
        published.textContent = 'Данные о версии сейчас недоступны';
      }
    });
</script>
"""
    return head(
        "Funny Find Words — головоломка со словами",
        "Игра «найди слова»: сто уровней, бонусные слова и подсказки, "
        "русский и английский языки. Бесплатно в Google Play.",
    ) + body.replace("</body>", script + "</body>")


def updates_page() -> str:
    """Страница обновлений: читает version.json."""
    body = f"""
{nav()}
  <main class="doc">
    <h1>Обновления</h1>
    <p class="updated">
      Если версия игры устарела, приложение попросит обновиться из Google Play.
    </p>

    <p class="status" id="status">
      <span class="dot" id="status-dot" aria-hidden="true"></span>
      <span id="status-text">Читаю данные…</span>
    </p>

    <div class="stats">
      <div class="stat">
        <p class="k">Текущая версия</p>
        <p class="v" id="latest-name">—</p>
        <p class="sub" id="latest-code"></p>
      </div>
      <div class="stat">
        <p class="k">Минимальная версия</p>
        <p class="v" id="min-code">—</p>
        <p class="sub">Ниже неё игра просит обновление</p>
      </div>
      <div class="stat">
        <p class="k">Дата публикации</p>
        <p class="v small" id="published-at">—</p>
      </div>
    </div>

    <div class="actions">
      <a class="btn btn-play" href="{PLAY_URL}">{play_icon()}Открыть в Google Play</a>
      <a class="btn btn-ghost" href="./version.json">version.json</a>
    </div>
  </main>
{foot()}"""
    script = """
<script>
  (function () {
    var text = document.getElementById('status-text');
    var dot = document.getElementById('status-dot');
    var fields = {
      latestName: document.getElementById('latest-name'),
      latestCode: document.getElementById('latest-code'),
      minCode: document.getElementById('min-code'),
      published: document.getElementById('published-at')
    };

    function fail(message) {
      text.textContent = message;
      dot.classList.add('error');
    }

    function formatDate(value) {
      if (!value) { return '—'; }
      var date = new Date(value + 'T00:00:00');
      if (isNaN(date)) { return value; }
      return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
    }

    fetch('./version.json?ts=' + Date.now(), { cache: 'no-store' })
      .then(function (r) {
        if (!r.ok) { throw new Error('HTTP ' + r.status); }
        return r.json();
      })
      .then(function (c) {
        fields.latestName.textContent = c.latestVersionName || '—';
        fields.latestCode.textContent = c.latestVersionCode
          ? 'Код версии ' + c.latestVersionCode : '';
        fields.minCode.textContent = c.minSupportedVersionCode;
        fields.published.textContent = formatDate(c.publishedAt);
        text.textContent = 'Данные загружены';
      })
      .catch(function (error) {
        fail('Не удалось прочитать version.json: ' + error.message);
      });
  })();
</script>
"""
    return head(
        "Funny Find Words — обновления",
        "Текущая версия игры Funny Find Words и минимальная поддерживаемая версия.",
    ) + body.replace("</body>", script + "</body>")


def doc_html(source: Path, title: str, lead: str, effective: str) -> str:
    """Оформленная страница из markdown-файла политики или условий."""
    rows = []
    for line in source.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        # Строки вида **Заголовок** в исходнике — это разделы, а не абзацы.
        if len(text) > 4 and text.startswith("**") and text.endswith("**") and text.count("**") == 2:
            rows.append("## " + text[2:-2])
        else:
            rows.append(line)
    html = markdown.markdown("\n".join(rows), extensions=["extra"])
    # Первый раздел повторяет заголовок страницы — убираем его.
    html = re.sub(r"<h2>.*?</h2>\s*", "", html, count=1)
    body = f"""
{nav()}
  <main class="doc">
    <h1>{title}</h1>
    <p class="updated">{lead} Действует с {effective}.</p>
    {html}
  </main>
{foot()}"""
    return head(title, lead) + body


def page_404() -> str:
    """Страница «не найдено»."""
    body = f"""
{nav()}
  <main class="doc">
    <h1>Страница не найдена</h1>
    <p class="updated">Такой страницы на сайте нет.</p>
    <p><a class="btn btn-ghost" href="./">На главную</a></p>
  </main>
{foot()}"""
    return head("Страница не найдена — Funny Find Words", "Страница не найдена.") + body


def main(output_dir: Path) -> None:
    """Собирает страницы в output_dir; по умолчанию — рядом со скриптом."""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(index_page(), encoding="utf-8")
    (output_dir / "updates.html").write_text(updates_page(), encoding="utf-8")
    (output_dir / "privacy.html").write_text(
        doc_html(
            HERE / "privacy.md",
            "Политика конфиденциальности",
            "Политика конфиденциальности приложения Funny Find Words.",
            "6 октября 2024",
        ),
        encoding="utf-8",
    )
    (output_dir / "terms.html").write_text(
        doc_html(
            HERE / "terms.md",
            "Условия использования",
            "Условия использования приложения Funny Find Words.",
            "6 октября 2024",
        ),
        encoding="utf-8",
    )
    (output_dir / "404.html").write_text(page_404(), encoding="utf-8")
    if output_dir.resolve() != HERE.resolve():
        shutil.copyfile(HERE / "site.css", output_dir / "site.css")
    print("Готово:", ", ".join(sorted(p.name for p in output_dir.glob("*.html"))))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE)