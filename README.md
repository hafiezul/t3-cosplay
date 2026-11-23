# t3-cosplay 🎭

> T3 Code, dressing up as other apps for fun.

A small collection of [T3 Code](https://github.com/pingdotgg/t3code) themes that make your coding agent look like the tools you either love or still see in your nightmares.

## The themes

| Theme | Costume | Vibe | Best in |
| --- | --- | --- | --- |
| 🧡 [**Cursor**](./themes/cursor.json) | Warm off-black `#14120B` and paper-cream `#F7F7F4`, Cursor orange `#F54E00` accent, ink-colored send button | Calm, focused, a little bit literary | Both |
| 💜 [**Teams**](./themes/teams.json) | Purple header bar `#464775`, lavender bubbles, purple underline on the message box, Segoe UI | Corporate flashbacks, now with type-checking | Light |
| 🍆 [**Slack**](./themes/slack.json) | Aubergine sidebar `#3F0E40`, blue selected row `#1164A3`, green send button `#007A5A`, Lato | Every thread is a huddle now | Light |
| 🎮 [**Discord**](./themes/discord.json) | Charcoal `#313338`, blurple `#5865F2`, borderless filled message box, green switches | Gaming chat, but the raid is a refactor | Dark |
| 📝 [**Notion**](./themes/notion.json) | Warm ink `#37352F` on white, `#F7F7F5` sidebar, blue `#2383E2`, red inline-code chips, soft shadows | Your agent, but make it a doc | Light |
| 🐙 [**GitHub**](./themes/github.json) | Primer `#0D1117` / `#010409`, green merge-style send button, blue focus ring, monospace inline code | Feels like code review at 2am | Dark |
| 🎧 [**Spotify**](./themes/spotify.json) | Black and `#121212`, green `#1ED760` with black text, pill buttons, send button grows on hover | Lo-fi beats to ship features to | Dark |

Every theme ships both light and dark variants. Spotify has no light mode, so its light variant is our own take.

## Install

1. Download the `.json` file you want from [`themes/`](./themes).
2. In T3 Code, open **Settings → Themes** and click **Add theme**.
3. Click **Choose files** and pick the `.json` file, or paste its contents into the box.

That's it: the theme is selected, and its card gets the full set of buttons (duplicate, edit, export, remove) like any theme you made yourself.

> **Don't copy the file into `~/.t3/userdata/themes/`.** T3 Code treats themes in that folder (and themes the agent applies for you) as part of the environment. They only get a duplicate button, so you can't edit or remove them from Settings, only by deleting the file.

## Undo

Click the trash icon on the theme's card in **Settings → Themes**, or just switch back to **T3 Code** (the stock theme).

## Disclaimer

These are fan-made, *inspired-by* themes. They aren't affiliated with or endorsed by Anysphere (Cursor), Microsoft (Teams, GitHub), Salesforce (Slack), Discord Inc., Notion Labs or Spotify. No logos, no trademarks, just colors and vibes.

## License

MIT
