# UK National Holidays — Setup

Shows **today’s** UK bank holiday on a **Vestaboard Note** (15×3) with themed colour tiles.

If there is **no** national holiday on the current date, the **next** one is shown (example: on **26 October 2026** → **Christmas Day**, 25 December 2026).

## Enable

1. **Integrations** → enable **UK National Holidays**
2. **Region** defaults to **England & Wales** (or choose Scotland / Northern Ireland / All)
3. **Show countdown** (default on) — optional `TODAY` / `TOMORROW` / `IN nD` on the Note
4. **Show “(substitute)”** (default off) — append to names when the bank holiday is a substitute day
5. **Save Changes**

No API key required — dates are built into the plugin (2026–2028).

## Note page layout

```
{{uk_holidays.note_row1}}
{{uk_holidays.note_row2}}
{{uk_holidays.note_row3}}
```

### Example — Christmas Day

```
{63}{66} 25 DEC     ← red + green tiles + date
CHRISTMAS DAY       ← name (≤ 45 chars total for the holiday title)
     TODAY          ← or IN 12D / TOMORROW
```

## Colour themes

| Holiday type | Colours |
|--------------|---------|
| Christmas | Red + Green |
| Boxing Day | Green + Red |
| New Year | Yellow + Violet |
| Easter | Violet + Yellow |
| May holidays | Green + Blue |
| Summer bank holiday | Orange + Yellow |
| St Andrew's Day | Blue + White |
| St Patrick's Day | Green + Orange |
| Battle of the Boyne | Orange + Blue |

Colour codes: `{63}` red, `{64}` orange, `{65}` yellow, `{66}` green, `{67}` blue, `{68}` violet, `{69}` white.

## Variables

| Variable | Description |
|----------|-------------|
| `holiday_name` | Official name (max 45) e.g. Christmas Day |
| `holiday_date` | ISO date |
| `days_until` | Days until the holiday |
| `is_today` | YES / NO |
| `color` / `color2` | Theme colour codes |
| `holidays` | Array of upcoming holidays |

## Regions

- **england_wales** — standard 8 bank holidays  
- **scotland** — includes 2nd January, St Andrew's Day, early August summer holiday  
- **northern_ireland** — includes St Patrick's Day, Battle of the Boyne  
- **all** — union of the above  


## Install from GitHub

```bash
curl -X POST http://localhost:4420/api/plugins/install \
  -H "Content-Type: application/json" \
  -d '{"repository": "https://github.com/peterdgreenway/fiestaboard-plugin--uk-holidays"}'
```
