"""Tests for uk_holidays plugin."""

import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

fake_base = ModuleType("src.plugins.base")


class PluginBase:
    def __init__(self, manifest=None):
        self.manifest = manifest or {}
        self.config = {}

    def clear_cache(self):
        pass


class PluginResult:
    def __init__(self, available=True, data=None, error=None):
        self.available = available
        self.data = data or {}
        self.error = error


fake_base.PluginBase = PluginBase
fake_base.PluginResult = PluginResult
sys.modules.setdefault("src", ModuleType("src"))
sys.modules.setdefault("src.plugins", ModuleType("src.plugins"))
sys.modules["src.plugins.base"] = fake_base

spec = importlib.util.spec_from_file_location(
    "uk_holidays", Path(__file__).resolve().parent.parent / "__init__.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_plugin_id():
    assert mod.UkHolidaysPlugin({}).plugin_id == "uk_holidays"


def test_names_max_45():
    for h in mod.HOLIDAYS:
        assert len(h["name"]) <= 45, h["name"]


def test_christmas_name():
    names = [h["name"] for h in mod.HOLIDAYS if h["date"].endswith("-12-25") or "Christmas" in h["name"]]
    assert any(n == "Christmas Day" for n in names)


def test_format_note_christmas():
    block, r1, r2, r3, c1, c2 = mod._format_note(
        "Christmas Day", date(2026, 12, 25), "christmas", True, 0
    )
    assert "CHRISTMAS" in r2 or "CHRISTMAS" in r3
    assert c1 == mod.RED
    assert c2 == mod.GREEN


def test_fetch_data():
    p = mod.UkHolidaysPlugin({})
    p.config = {"region": "england_wales", "refresh_seconds": 3600}
    r = p.fetch_data()
    assert r.available
    assert len(r.data["holiday_name"]) <= 45
    assert "note_row1" in r.data
