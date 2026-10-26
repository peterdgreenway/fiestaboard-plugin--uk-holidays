# FiestaBoard plugin: UK National Holidays

Next UK bank holiday on a **Vestaboard Note** (15×3), with themed colour pixels and names capped at **45 characters**.

## Note layout

```
{{uk_holidays.note_row1}}
{{uk_holidays.note_row2}}
{{uk_holidays.note_row3}}
```

Christmas Day example:

```
{63}{66} 25 DEC
CHRISTMAS DAY
     TODAY
```

## Install

```bash
curl -X POST http://localhost:4420/api/plugins/install \
  -H "Content-Type: application/json" \
  -d '{"repository": "https://github.com/peterdgreenway/fiestaboard-plugin--uk-holidays"}'
```

Plugin id: `uk_holidays`

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| region | england_wales | Default England & Wales; also scotland / northern_ireland / all |
| show_countdown | true | Show TODAY / TOMORROW / IN nD on the Note |
| date_format | short | short (25 DEC) or long (25 December 2026) |
| show_weekday | false | Include weekday the holiday falls on |
| show_substitute | false | Append “ (substitute)” when the day is a substitute bank holiday |
| refresh_seconds | 3600 | Min 300 |

## Licence

MIT
