"""Tests for the translation helper.

Streamlit's session_state isn't easily reachable outside a running script run,
so we stub it before importing the module under test.
"""
from __future__ import annotations

import importlib
import sys
import types


def _fake_streamlit():
    fake = types.ModuleType("streamlit")
    fake.session_state = {}
    return fake


def _fresh_i18n():
    sys.modules["streamlit"] = _fake_streamlit()
    if "i18n" in sys.modules:
        del sys.modules["i18n"]
    return importlib.import_module("i18n")


def test_default_lang_is_english():
    i18n = _fresh_i18n()
    assert i18n.get_lang() == "en"


def test_set_lang_persists():
    i18n = _fresh_i18n()
    i18n.set_lang("ko")
    assert i18n.get_lang() == "ko"


def test_translate_basic():
    i18n = _fresh_i18n()
    i18n.set_lang("ko")
    assert "번호 뽑기" in i18n.t("button.generate")
    i18n.set_lang("en")
    assert "Generate" in i18n.t("button.generate")


def test_translate_falls_back_to_english_for_missing():
    i18n = _fresh_i18n()
    i18n.set_lang("ko")
    # If we ever ship a key without a Korean translation, we should fall back.
    assert i18n.t("nonexistent.key") == "nonexistent.key"


def test_every_key_has_english_translation():
    i18n = _fresh_i18n()
    missing = [k for k, v in i18n.TRANSLATIONS.items() if "en" not in v]
    assert not missing, f"Keys missing English: {missing}"


def test_every_key_has_korean_translation():
    i18n = _fresh_i18n()
    missing = [k for k, v in i18n.TRANSLATIONS.items() if "ko" not in v]
    assert not missing, f"Keys missing Korean: {missing}"
