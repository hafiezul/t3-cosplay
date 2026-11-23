# t3-cosplay 🎭

> T3 Code, dressing up as other apps for fun.

A small collection of [T3 Code](https://github.com/pingdotgg/t3code) themes that make your coding agent look like the tools you either love or still see in your nightmares.

| Theme | Costume | Vibe |
| --- | --- | --- |
| **Cursor-inspired OLED** | Cursor's dark editor, taken to pure `#000000` | Calm, focused, battery-friendly |
| **Teams-inspired** | That purple header bar. You know the one. | Corporate flashbacks, now with type-checking |

## The themes

### 🖤 Cursor-inspired OLED (`cursor-oled.json`)

Built from the colors in Cursor's own Cursor Dark and Cursor Light themes, then pushed to true black for OLED screens.

- Pure black backgrounds everywhere, so those pixels just switch off
- Soft hairline borders (`#171717`) instead of grey panels
- Muted blue accent (`#81A1C1`) taken from Cursor Dark
- High-contrast white send button and visible switches, so you always know when you can hit send
- Matching light mode based on Cursor Light

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
2. Put it in your T3 Code themes folder:

   ```sh
   mkdir -p ~/.t3/userdata/themes
   cp themes/teams-inspired.json ~/.t3/userdata/themes/
   ```

3. Reload T3 Code and pick it from **Settings → Themes**.

Or just ask the agent inside T3 Code: *"apply the theme from this JSON"* and paste the file.

## Undo

Choose **T3 Code** (the stock theme) in **Settings → Themes**.

## Disclaimer

These are fan-made, *inspired-by* themes. They aren't affiliated with or endorsed by Anysphere (Cursor) or Microsoft (Teams). No logos, no trademarks, just colors and vibes.

## License

MIT
