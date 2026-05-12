"""Minimal translation layer for the Q-Lottery UI.

Usage::

    from i18n import t
    st.write(t("button.generate"))

Language is read from ``st.session_state['lang']`` and falls back to English.
"""
from __future__ import annotations

import streamlit as st

DEFAULT_LANG = "en"
SUPPORTED = ("ko", "en")

LANG_LABEL = {"ko": "한국어", "en": "English"}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── App shell ──────────────────────────────────────────────────────────
    "app.title": {
        "ko": "Q-Lottery Game · 양자 로또 번호 생성기",
        "en": "Q-Lottery Game · Quantum Lottery Generator",
    },
    "sidebar.menu": {"ko": "메뉴 선택", "en": "Select menu"},
    "sidebar.language": {"ko": "언어", "en": "Language"},
    "sidebar.about": {"ko": "Q-Lottery 소개", "en": "About Q-Lottery Game"},
    "sidebar.custom": {"ko": "Custom 모드", "en": "Custom"},
    "sidebar.tagline": {
        "ko": "IBM Quantum 시뮬레이터로 만든 진짜 난수",
        "en": "Real random numbers, powered by IBM Quantum",
    },
    # ── Controls ───────────────────────────────────────────────────────────
    "mode.label": {"ko": "모드 선택", "en": "Mode"},
    "mode.simple": {"ko": "단순 Q-RNG", "en": "Simple Q-RNG"},
    "mode.birthday": {
        "ko": "생일 얽힘 Q-RNG",
        "en": "Birthday-entangled Q-RNG",
    },
    "mode.simple.help": {
        "ko": "Hadamard 게이트만 사용한 순수 양자 난수.",
        "en": "Pure Hadamard-based quantum randomness.",
    },
    "mode.birthday.help": {
        "ko": "생월/생일을 회전각으로 인코딩해 결과를 살짝 편향시킵니다.",
        "en": "Encodes your birthday as a rotation angle to gently bias the outcome.",
    },
    "birthday.label": {"ko": "생일을 알려주세요", "en": "When is your birthday?"},
    "birthday.value": {"ko": "입력한 생일:", "en": "Your birthday:"},
    "games.count": {"ko": "몇 게임 뽑을까요?", "en": "How many games?"},
    "details.toggle": {
        "ko": "양자 회로와 디코딩 과정 보기",
        "en": "Show quantum circuit & decoding details",
    },
    "details.help": {
        "ko": "체크하면 각 게임의 양자 회로 그림과 이진→십진 변환 표가 나옵니다.",
        "en": "Reveals the quantum circuit diagram and bit→decimal mapping for each game.",
    },
    "button.generate": {
        "ko": "🎰 번호 뽑기",
        "en": "🎰 Generate my numbers",
    },
    "button.generating": {
        "ko": "양자 회로 측정 중…",
        "en": "Measuring the quantum circuit…",
    },
    "button.copy": {"ko": "📋 결과 복사", "en": "📋 Copy results"},
    "button.clear_history": {
        "ko": "🗑️ 이력 지우기",
        "en": "🗑️ Clear history",
    },
    # ── Result ─────────────────────────────────────────────────────────────
    "result.heading": {"ko": "🎉 행운의 번호", "en": "🎉 Your lucky numbers"},
    "result.game": {"ko": "게임", "en": "Game"},
    "result.bonus": {"ko": "보너스", "en": "Bonus"},
    "result.share_caption": {
        "ko": "결과 텍스트는 아래에서 복사할 수 있어요.",
        "en": "Copy the result text from the box below.",
    },
    "history.heading": {"ko": "📜 최근 생성 이력", "en": "📜 Recent history"},
    "history.empty": {
        "ko": "아직 생성한 번호가 없어요.",
        "en": "No numbers generated yet.",
    },
    # ── Details ────────────────────────────────────────────────────────────
    "details.heading": {
        "ko": "양자 회로 & 디코딩 상세",
        "en": "Quantum Circuit & Decoding Details",
    },
    "details.circuit": {"ko": "양자 회로", "en": "Quantum circuit"},
    "details.circuit.main": {
        "ko": "메인 번호 회로",
        "en": "Main numbers circuit",
    },
    "details.circuit.bonus": {
        "ko": "보너스 볼 회로",
        "en": "Bonus ball circuit",
    },
    "details.decoding": {
        "ko": "이진수 → 십진수 변환",
        "en": "Binary → Decimal decoding",
    },
    "details.col.ball": {"ko": "공", "en": "Ball"},
    "details.col.binary": {"ko": "측정값 (이진)", "en": "Measurement (binary)"},
    "details.col.decimal": {"ko": "번호 (십진)", "en": "Number (decimal)"},
    "details.caption": {
        "ko": "H 게이트는 양자 동전 던지기 역할을 하고, 측정 결과가 이진수로 떨어집니다.",
        "en": "The H gate acts as a quantum coin flip; the measurement yields the bits below.",
    },
    # ── Custom ─────────────────────────────────────────────────────────────
    "custom.title": {
        "ko": "Custom Q-Lottery Game",
        "en": "Custom Q-Lottery Game",
    },
    "custom.intro": {
        "ko": "원하는 범위로 양자 난수를 만들어 보세요.",
        "en": "Customize the range and pull your own quantum random numbers.",
    },
    "custom.count": {
        "ko": "몇 개의 난수가 필요한가요? (1~10)",
        "en": "How many Q-random numbers? (1–10)",
    },
    "custom.upper": {
        "ko": "최댓값을 골라주세요 (2~9,000,000,000,000,000)",
        "en": "Choose the upper bound (2–9,000,000,000,000,000)",
    },
    # ── Caution / About ────────────────────────────────────────────────────
    "caution.title": {"ko": "⚠️ 주의", "en": "⚠️ Caution"},
    "caution.body": {
        "ko": "양자 난수가 의사 난수보다 통계적으로 더 무작위하지만, **당첨 확률을 높이지는 않습니다**. 재미로만 즐겨주세요!",
        "en": "Quantum randomness is statistically more uniform than PRNG, but **does not improve your odds of winning**. Just for fun!",
    },
    "about.cta": {
        "ko": "왼쪽 메뉴에서 게임을 골라 바로 시작해 보세요!",
        "en": "Pick a game from the sidebar to get started!",
    },
    # ── Errors ─────────────────────────────────────────────────────────────
    "error.qrng": {
        "ko": "양자 난수 생성에 실패했어요. 다시 시도해 주세요.",
        "en": "Could not generate a quantum random number. Please retry.",
    },
    # ── Download ───────────────────────────────────────────────────────────
    "download.button": {
        "ko": "🖼️ 결과 카드 다운로드 (PNG)",
        "en": "🖼️ Download result card (PNG)",
    },
    "download.help": {
        "ko": "친구한테 자랑할 수 있는 이미지 한 장으로 저장해요.",
        "en": "Save a shareable image you can show off to friends.",
    },
    # ── Circuit caption ────────────────────────────────────────────────────
    "details.circuit.caption": {
        "ko": "H 게이트가 양자 동전 던지기 역할을 합니다. 측정 결과를 이진수로 읽고 십진수로 변환합니다.",
        "en": "The H gate acts as a quantum coin flip; the measurement is read out as a bit string and converted to decimal.",
    },
    # ── Comparison with the latest Korean Lotto draw ───────────────────────
    "compare.heading": {
        "ko": "📡 이번 주 회차와 비교",
        "en": "📡 Compare with this week's draw",
    },
    "compare.fetching": {
        "ko": "최신 회차 정보를 가져오는 중…",
        "en": "Fetching the latest draw…",
    },
    "compare.unavailable": {
        "ko": "최신 회차 정보를 가져오지 못했어요. 잠시 후 다시 시도해 주세요.",
        "en": "Couldn't fetch the latest draw right now. Please try again later.",
    },
    "compare.draw_header": {
        "ko": "{n}회차 ({date}) 당첨번호",
        "en": "Draw #{n} ({date}) winning numbers",
    },
    "compare.bonus": {"ko": "보너스", "en": "Bonus"},
    "compare.row_summary": {
        "ko": "{label} → 일치 {match}개{bonus_suffix} · {rank}",
        "en": "{label} → {match} matched{bonus_suffix} · {rank}",
    },
    "compare.bonus_hit_suffix": {
        "ko": " + 보너스",
        "en": " + bonus",
    },
    "compare.rank.1st": {"ko": "🥇 1등!", "en": "🥇 1st prize!"},
    "compare.rank.2nd": {"ko": "🥈 2등!", "en": "🥈 2nd prize!"},
    "compare.rank.3rd": {"ko": "🥉 3등", "en": "🥉 3rd prize"},
    "compare.rank.4th": {"ko": "🎉 4등", "en": "🎉 4th prize"},
    "compare.rank.5th": {"ko": "🎈 5등", "en": "🎈 5th prize"},
    "compare.rank.none": {"ko": "꽝 (다음 기회에!)", "en": "No prize (better luck next time!)"},
    "compare.disclaimer": {
        "ko": "🙃 이번 회차 결과는 이미 확정된 번호이며, 양자 RNG로 생성한 번호와는 사후 비교일 뿐입니다.",
        "en": "🙃 The draw has already happened — this is a retrospective comparison with quantum-generated picks.",
    },
}


def get_lang() -> str:
    return st.session_state.get("lang", DEFAULT_LANG)


def set_lang(lang: str) -> None:
    if lang not in SUPPORTED:
        lang = DEFAULT_LANG
    st.session_state["lang"] = lang


def t(key: str) -> str:
    """Translate ``key`` using the current language; falls back to English."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    lang = get_lang()
    return entry.get(lang) or entry.get(DEFAULT_LANG) or key
