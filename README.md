# t3-cosplay 🎭

> T3 Code, dressing up as other apps for fun.

A small collection of [T3 Code](https://github.com/pingdotgg/t3code) themes that make your coding agent look like the tools you either love or still see in your nightmares.

| Theme | Costume | Vibe |
| --- | --- | --- |
| **Cursor-inspired** | cursor.com's warm ink-and-paper look | Calm, focused, a little bit literary |
| **Teams-inspired** | That purple header bar. You know the one. | Corporate flashbacks, now with type-checking |

## The themes

### 🧡 Cursor-inspired (`cursor-inspired.json`)

Built from the colors on [cursor.com](https://cursor.com/): warm off-black and paper-cream instead of grey, with that one orange.

- Warm near-black canvas (`#14120B`) and cream text (`#EDECEC`) in dark mode
- Paper-cream canvas (`#F7F7F4`) and ink text (`#26251E`) in light mode
- Borders and muted text mixed from the text color, the same way the site does it
- Cursor orange (`#F54E00`) for the accent and switches
- Ink-colored send button, like the site's primary buttons

### 💜 Teams-inspired (`teams-inspired.json`)

For when you miss the feeling of a meeting that could have been an email.

- Classic Teams purple header bar (`#464775`) in light mode, muted purple in dark
- Teams purple accent (`#5B5FC7`) and lavender message bubbles
- A purple underline under the message box while you type, just like the real thing
- Squarer 4px corners and Segoe UI if you have it installed
- Outlined switches that fill purple when on

Light mode gives the strongest effect.

## Install

1. Download the `.json` file you want from [`themes/`](./themes).
2. In T3 Code, open **Settings → Themes** and click **Add theme**.
3. Click **Choose files** and pick the `.json` file, or paste its contents into the box.

That's it: the theme is selected, and its card gets the full set of buttons (duplicate, edit, export, remove) like any theme you made yourself.

> **Don't copy the file into `~/.t3/userdata/themes/`.** T3 Code treats themes in that folder (and themes the agent applies for you) as part of the environment. They only get a duplicate button, so you can't edit or remove them from Settings, only by deleting the file.

## Undo

Click the trash icon on the theme's card in **Settings → Themes**, or just switch back to **T3 Code** (the stock theme).

## Disclaimer

These are fan-made, *inspired-by* themes. They aren't affiliated with or endorsed by Anysphere (Cursor) or Microsoft (Teams). No logos, no trademarks, just colors and vibes.

## License

MIT
