"""UK National Holidays — Vestaboard Note display with themed colour tiles."""

from __future__ import annotations

import logging
import re
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Tuple

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

NOTE_WIDTH = 15
NOTE_ROWS = 3
NAME_MAX = 45

RED = "{63}"
ORANGE = "{64}"
YELLOW = "{65}"
GREEN = "{66}"
BLUE = "{67}"
VIOLET = "{68}"
WHITE = "{69}"
BLACK = "{70}"

HOLIDAYS: List[Dict[str, Any]] = [
    {"date": "2026-01-01", "name": "New Year's Day", "region": "uk", "theme": "new_year", "substitute": False},
    {"date": "2026-04-03", "name": "Good Friday", "region": "uk", "theme": "easter", "substitute": False},
    {"date": "2026-04-06", "name": "Easter Monday", "region": "ew_ni", "theme": "easter", "substitute": False},
    {"date": "2026-05-04", "name": "Early May Bank Holiday", "region": "uk", "theme": "may", "substitute": False},
    {"date": "2026-05-25", "name": "Spring Bank Holiday", "region": "uk", "theme": "may", "substitute": False},
    {"date": "2026-08-31", "name": "Summer Bank Holiday", "region": "ew_ni", "theme": "summer", "substitute": False},
    {"date": "2026-11-30", "name": "St Andrew's Day", "region": "scotland", "theme": "scotland", "substitute": False},
    {"date": "2026-12-25", "name": "Christmas Day", "region": "uk", "theme": "christmas", "substitute": False},
    {"date": "2026-12-28", "name": "Boxing Day", "region": "uk", "theme": "boxing", "substitute": True},
    {"date": "2027-01-01", "name": "New Year's Day", "region": "uk", "theme": "new_year", "substitute": False},
    {"date": "2027-01-04", "name": "2nd January", "region": "scotland", "theme": "new_year", "substitute": True},
    {"date": "2027-03-17", "name": "St Patrick's Day", "region": "ni", "theme": "patrick", "substitute": False},
    {"date": "2027-03-26", "name": "Good Friday", "region": "uk", "theme": "easter", "substitute": False},
    {"date": "2027-03-29", "name": "Easter Monday", "region": "ew_ni", "theme": "easter", "substitute": False},
    {"date": "2027-05-03", "name": "Early May Bank Holiday", "region": "uk", "theme": "may", "substitute": False},
    {"date": "2027-05-31", "name": "Spring Bank Holiday", "region": "uk", "theme": "may", "substitute": False},
    {"date": "2027-07-12", "name": "Battle of the Boyne", "region": "ni", "theme": "boyne", "substitute": False},
    {"date": "2027-08-02", "name": "Summer Bank Holiday", "region": "scotland", "theme": "summer", "substitute": False},
    {"date": "2027-08-30", "name": "Summer Bank Holiday", "region": "ew_ni", "theme": "summer", "substitute": False},
    {"date": "2027-11-30", "name": "St Andrew's Day", "region": "scotland", "theme": "scotland", "substitute": False},
    {"date": "2027-12-27", "name": "Christmas Day", "region": "uk", "theme": "christmas", "substitute": True},
    {"date": "2027-12-28", "name": "Boxing Day", "region": "uk", "theme": "boxing", "substitute": True},
    {"date": "2028-01-03", "name": "New Year's Day", "region": "uk", "theme": "new_year", "substitute": True},
    {"date": "2028-01-04", "name": "2nd January", "region": "scotland", "theme": "new_year", "substitute": True},
    {"date": "2028-03-17", "name": "St Patrick's Day", "region": "ni", "theme": "patrick", "substitute": False},
    {"date": "2028-04-14", "name": "Good Friday", "region": "uk", "theme": "easter", "substitute": False},
    {"date": "2028-04-17", "name": "Easter Monday", "region": "ew_ni", "theme": "easter", "substitute": False},
    {"date": "2028-05-01", "name": "Early May Bank Holiday", "region": "uk", "theme": "may", "substitute": False},
    {"date": "2028-05-29", "name": "Spring Bank Holiday", "region": "uk", "theme": "may", "substitute": False},
    {"date": "2028-07-12", "name": "Battle of the Boyne", "region": "ni", "theme": "boyne", "substitute": False},
    {"date": "2028-08-07", "name": "Summer Bank Holiday", "region": "scotland", "theme": "summer", "substitute": False},
    {"date": "2028-08-28", "name": "Summer Bank Holiday", "region": "ew_ni", "theme": "summer", "substitute": False},
    {"date": "2028-11-30", "name": "St Andrew's Day", "region": "scotland", "theme": "scotland", "substitute": False},
    {"date": "2028-12-25", "name": "Christmas Day", "region": "uk", "theme": "christmas", "substitute": False},
    {"date": "2028-12-26", "name": "Boxing Day", "region": "uk", "theme": "boxing", "substitute": False},
]

REGION_FILTERS = {
    "england_wales": {"uk", "ew_ni"},
    "scotland": {"uk", "scotland"},
    "northern_ireland": {"uk", "ew_ni", "ni"},
    "all": {"uk", "ew_ni", "scotland", "ni"},
}

THEMES: Dict[str, Dict[str, str]] = {
    "christmas": {"color": RED, "color2": GREEN, "accent": "FESTIVE"},
    "boxing": {"color": GREEN, "color2": RED, "accent": "BOXING"},
    "new_year": {"color": YELLOW, "color2": VIOLET, "accent": "NEW YEAR"},
    "easter": {"color": VIOLET, "color2": YELLOW, "accent": "EASTER"},
    "may": {"color": GREEN, "color2": BLUE, "accent": "MAY DAY"},
    "summer": {"color": ORANGE, "color2": YELLOW, "accent": "SUMMER"},
    "scotland": {"color": BLUE, "color2": WHITE, "accent": "SCOTLAND"},
    "patrick": {"color": GREEN, "color2": ORANGE, "accent": "IRELAND"},
    "boyne": {"color": ORANGE, "color2": BLUE, "accent": "NI"},
    "default": {"color": BLUE, "color2": WHITE, "accent": "HOLIDAY"},
}


def _parse_date(s: str) -> date:
    return date.fromisoformat(s)


def _clamp_name(name: str) -> str:
    name = (name or "").strip()
    if len(name) > NAME_MAX:
        name = name[: NAME_MAX - 1].rsplit(" ", 1)[0][:NAME_MAX]
    return name


def _display_name(name: str, is_substitute: bool, show_substitute: bool) -> str:
    name = _clamp_name(name)
    if is_substitute and show_substitute:
        suffix = " (substitute)"
        if len(name) + len(suffix) <= NAME_MAX:
            name = name + suffix
        else:
            short = " (sub)"
            if len(name) + len(short) <= NAME_MAX:
                name = name + short
    return _clamp_name(name)


def _tile_len(s: str) -> int:
    """Each {NN} colour marker counts as 1 tile."""
    codes = re.findall(r"\{\d{2}\}", s)
    stripped = re.sub(r"\{\d{2}\}", "", s)
    return len(stripped) + len(codes)


def _wrap_name(name: str, width: int = NOTE_WIDTH, rows: int = 2) -> List[str]:
    words = (name or "").upper().split()
    lines: List[str] = []
    cur = ""
    for w in words:
        cand = f"{cur} {w}".strip() if cur else w
        if len(cand) <= width:
            cur = cand
        else:
            if cur:
                lines.append(cur[:width].ljust(width))
            cur = w[:width]
            if len(lines) >= rows:
                cur = ""
                break
    if cur and len(lines) < rows:
        lines.append(cur[:width].ljust(width))
    while len(lines) < rows:
        lines.append(" " * width)
    return [ln[:width].ljust(width) for ln in lines[:rows]]


def _format_note(
    holiday_name: str,
    d: date,
    theme: str,
    is_today: bool,
    days_until: int,
    show_countdown: bool = True,
) -> Tuple[str, str, str, str, str, str]:
    """Every Note row is at most 15 tiles."""
    t = THEMES.get(theme, THEMES["default"])
    c1, c2 = t["color"], t["color2"]
    name = _clamp_name(holiday_name)
    date_str = d.strftime("%d %b").lstrip("0").upper()

    if is_today:
        status = "TODAY"
    elif not show_countdown:
        status = "NEXT"
    elif days_until == 1:
        status = "TOMORROW"
    elif days_until > 1:
        status = f"IN {days_until}D"
    else:
        status = "NEXT"

    # Row 1: 2 colour tiles + 13 text chars = 15 tiles
    text_budget = NOTE_WIDTH - 2
    row1_text = f" {date_str}"[:text_budget].ljust(text_budget)
    row1 = f"{c1}{c2}{row1_text}"
    while _tile_len(row1) > NOTE_WIDTH and len(row1_text) > 0:
        row1_text = row1_text[:-1]
        row1 = f"{c1}{c2}{row1_text.ljust(text_budget)[:text_budget]}"

    name_lines = _wrap_name(name, width=NOTE_WIDTH, rows=2)
    row2 = name_lines[0][:NOTE_WIDTH].ljust(NOTE_WIDTH)
    row3 = name_lines[1][:NOTE_WIDTH].ljust(NOTE_WIDTH)

    if status:
        if not row3.strip():
            row3 = status.center(NOTE_WIDTH)[:NOTE_WIDTH].ljust(NOTE_WIDTH)
        elif len(row3.strip()) + 1 + len(status) <= NOTE_WIDTH and status not in row3:
            row3 = f"{row3.strip()} {status}"[:NOTE_WIDTH].ljust(NOTE_WIDTH)

    row2 = row2[:NOTE_WIDTH].ljust(NOTE_WIDTH)
    row3 = row3[:NOTE_WIDTH].ljust(NOTE_WIDTH)
    block = f"{row1}\n{row2}\n{row3}"
    return block, row1, row2, row3, c1, c2


class UkHolidaysPlugin(PluginBase):
    """Today's UK bank holiday, or the next one if none today."""

    @property
    def plugin_id(self) -> str:
        return "uk_holidays"

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        region = config.get("region", "england_wales")
        if region not in REGION_FILTERS:
            errors.append(
                "region must be one of: england_wales, scotland, northern_ireland, all"
            )
        refresh = config.get("refresh_seconds", 3600)
        if not isinstance(refresh, int) or refresh < 300:
            errors.append("refresh_seconds must be an integer >= 300")
        for key in ("show_countdown", "show_substitute"):
            if key in config and not isinstance(config[key], bool):
                errors.append(f"{key} must be a boolean")
        return errors

    def on_config_change(self, old_config: Dict[str, Any], new_config: Dict[str, Any]) -> None:
        try:
            self.clear_cache()
        except Exception:
            pass

    def fetch_data(self) -> PluginResult:
        try:
            region = self.config.get("region", "england_wales")
            allowed = REGION_FILTERS.get(region, REGION_FILTERS["england_wales"])
            show_countdown = bool(self.config.get("show_countdown", True))
            show_substitute = bool(self.config.get("show_substitute", False))
            today = datetime.now(timezone.utc).date()

            upcoming: List[Dict[str, Any]] = []
            for h in HOLIDAYS:
                if h["region"] not in allowed:
                    continue
                d = _parse_date(h["date"])
                name = _display_name(h["name"], bool(h.get("substitute")), show_substitute)
                days = (d - today).days
                upcoming.append(
                    {
                        "date": h["date"],
                        "date_obj": d,
                        "name": name,
                        "theme": h["theme"],
                        "region": h["region"],
                        "substitute": bool(h.get("substitute")),
                        "days_until": days,
                        "is_today": days == 0,
                        "is_past": days < 0,
                    }
                )

            future = [x for x in upcoming if x["days_until"] > 0]
            today_list = [x for x in upcoming if x["days_until"] == 0]
            past = [x for x in upcoming if x["days_until"] < 0]

            if today_list:
                current = today_list[0]
            elif future:
                current = future[0]
            elif past:
                current = past[-1]
            else:
                return PluginResult(available=False, error="No holidays configured")

            block, r1, r2, r3, c1, c2 = _format_note(
                current["name"],
                current["date_obj"],
                current["theme"],
                current["is_today"],
                current["days_until"],
                show_countdown=show_countdown,
            )
            r2 = r2[:NOTE_WIDTH].ljust(NOTE_WIDTH)
            r3 = r3[:NOTE_WIDTH].ljust(NOTE_WIDTH)
            block = f"{r1}\n{r2}\n{r3}"

            if today_list and current in today_list:
                next_h = future[0] if future else None
            else:
                next_h = future[1] if len(future) > 1 else None

            remaining = []
            for x in (today_list + future)[:12]:
                remaining.append(
                    {
                        "date": x["date"],
                        "name": x["name"][:45],
                        "days_until": str(x["days_until"]),
                        "theme": x["theme"],
                    }
                )

            data = {
                "holiday_name": current["name"][:45],
                "holiday_date": current["date"],
                "holiday_date_short": current["date_obj"].strftime("%d %b %Y"),
                "holiday_theme": current["theme"],
                "is_substitute": "YES" if current.get("substitute") else "NO",
                "is_today": "YES" if current["is_today"] else "NO",
                "is_next": "NO" if current["is_today"] else "YES",
                "status_label": (
                    "TODAY"
                    if current["is_today"]
                    else ("TOMORROW" if current["days_until"] == 1 else f"IN {current['days_until']}D")
                ),
                "days_until": str(max(0, current["days_until"])),
                "color": c1,
                "color2": c2,
                "note_row1": r1,
                "note_row2": r2,
                "note_row3": r3,
                "note_block": block,
                "next_holiday_name": (next_h["name"] if next_h else "")[:45],
                "next_holiday_date": next_h["date"] if next_h else "",
                "next_days_until": str(next_h["days_until"]) if next_h else "",
                "region": region,
                "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                "holidays": remaining,
            }
            return PluginResult(available=True, data=data)
        except Exception as e:
            logger.exception("uk_holidays error")
            return PluginResult(available=False, error=str(e)[:120])
