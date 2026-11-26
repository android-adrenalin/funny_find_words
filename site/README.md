# Сайт Funny Find Words

Исходники сайта. Готовые страницы собираются в `../docs/` — этот каталог отдаёт GitHub Pages.

| Файл | Назначение |
|---|---|
| `build.py` | сборщик: читает `privacy.md` и `terms.md`, пишет страницы в `docs/` |
| `site.css` | общие стили всех страниц (палитра игры, без внешних шрифтов и CDN) |
| `privacy.md`, `terms.md` | официальные тексты; такие же файлы лежат в корне репозитория |

Страницы: `index.html` (главная игры), `updates.html` (версия и порог обновления),
`privacy.html`, `terms.html`, `404.html`.

## Пересборка

```shell
python3 site/build.py docs
```

Нужен модуль `markdown` (`python3 -m pip install markdown`). Сборщик пишет HTML-страницы
и копирует `site.css` в `docs/`.

## Что собирается вручную

`docs/version.json` — конфиг проверки обновлений, его приложение читает при запуске.
Скрипт его не трогает: при релизе вручную поднимайте `latestVersionCode` и
`latestVersionName`, а `minSupportedVersionCode` — только при несовместимых изменениях.

## Адреса

- Сайт: <https://android-adrenalin.github.io/funny_find_words/>
- Политика: <https://android-adrenalin.github.io/funny_find_words/privacy.html>
- Условия: <https://android-adrenalin.github.io/funny_find_words/terms.html>
- Конфиг обновлений: <https://android-adrenalin.github.io/funny_find_words/version.json>