"""Marketing / educational copy for the landing page.

All copy uses the ``i18n.t()`` helper so the same page can be served in both
Korean and English.
"""
from __future__ import annotations

import streamlit as st

from i18n import get_lang


_COPY = {
    "ko": {
        "title": "양자 로또 번호 생성기",
        "subtitle": "IBM Quantum 시뮬레이터로 만드는 *진짜* 난수",
        "section_real": "1) 진짜 난수란?",
        "real_body": (
            "**진짜 난수(TRNG)** 는 측정으로부터 얻은 물리 현상을 바탕으로 생성되어 예측이 불가능합니다.\n"
            "반면 우리가 흔히 쓰는 **의사 난수(PRNG)** 는 시드 값에서 결정론적으로 만들어집니다.\n\n"
            "이 앱은 IBM Qiskit 의 `AerSimulator` 를 사용해 양자 회로를 측정하고, 그 결과를 난수로 사용합니다."
        ),
        "section_modes": "2) 두 가지 생성 모드",
        "simple_title": "A) 단순 Q-RNG",
        "simple_body": "Hadamard 게이트로 모든 큐비트를 50:50 중첩 상태로 만든 뒤 측정합니다.",
        "birthday_title": "B) 생일 얽힘 Q-RNG",
        "birthday_body": (
            "- 보조 큐비트 2개를 추가하고\n"
            "- 생월·생일을 Ry 회전각으로 인코딩한 뒤\n"
            "- CRY 게이트로 *서로 다른* 메인 큐비트와 얽혀\n"
            "- 결과를 자연스럽게 살짝만 편향시킵니다."
        ),
        "section_games": "3) 지원하는 로또",
        "games_body": (
            "- 한국 Lotto 6/45\n"
            "- 미국 Powerball\n"
            "- 인도 Lotto India\n"
            "- 일본 Lotto7\n"
            "- 프랑스 Loto\n"
            "- Custom (직접 범위 지정)"
        ),
        "cta_caption": "왼쪽 메뉴에서 게임을 골라 바로 시작해 보세요!",
        "example_simple": "> 단순 Q-RNG 회로 예시",
        "example_birthday": "> 생일 얽힘 Q-RNG 회로 예시 (8월 30일)",
        "generated": "생성된 번호 : ",
        "binary": "이진",
        "decimal": "십진",
    },
    "en": {
        "title": "Quantum Lottery Game",
        "subtitle": "*Real* random numbers, generated with an IBM Quantum simulator",
        "section_real": "1) What is *real* random number generation?",
        "real_body": (
            "**True random number generation (TRNG)** measures a physical phenomenon and is unpredictable.\n"
            "**Pseudo random number generation (PRNG)** is fully determined by an initial seed.\n\n"
            "This app builds quantum circuits with IBM Qiskit and runs them on the local `AerSimulator` backend."
        ),
        "section_modes": "2) Two generation modes",
        "simple_title": "A) Simple Q-RNG",
        "simple_body": "Apply a Hadamard gate to every qubit, putting each into a 50/50 superposition, then measure.",
        "birthday_title": "B) Birthday-entangled Q-RNG",
        "birthday_body": (
            "- Add two ancilla qubits\n"
            "- Encode birth month and day as Ry rotation angles\n"
            "- Use CRY gates to entangle with two *distinct* main qubits\n"
            "- Result: a gentle, non-collapsing bias from your birthday."
        ),
        "section_games": "3) Supported lotteries",
        "games_body": (
            "- Korea: Lotto 6/45\n"
            "- USA: Powerball\n"
            "- India: Lotto India\n"
            "- Japan: Lotto7\n"
            "- France: French Loto\n"
            "- Custom (your own range)"
        ),
        "cta_caption": "Pick a game from the sidebar to get started!",
        "example_simple": "> Simple Q-RNG example circuit",
        "example_birthday": "> Birthday-entangled example circuit (Aug 30)",
        "generated": "Generated number: ",
        "binary": "binary",
        "decimal": "decimal",
    },
}


def _c() -> dict:
    return _COPY.get(get_lang(), _COPY["en"])


def intro_header() -> None:
    c = _c()
    st.title(c["title"])
    st.caption(c["subtitle"])


def intro_concept() -> None:
    c = _c()
    st.subheader(c["section_real"])
    st.write(c["real_body"])


def intro_modes_simple() -> None:
    c = _c()
    st.subheader(c["section_modes"])
    st.markdown(f"#### {c['simple_title']}")
    st.write(c["simple_body"])


def intro_modes_birthday() -> None:
    c = _c()
    st.markdown(f"#### {c['birthday_title']}")
    st.write(c["birthday_body"])


def intro_games() -> None:
    c = _c()
    st.subheader(c["section_games"])
    st.write(c["games_body"])
    st.info(c["cta_caption"])


def example_simple_caption() -> str:
    return _c()["example_simple"]


def example_birthday_caption() -> str:
    return _c()["example_birthday"]


def example_result_line(raw_bits: str, decimal: int) -> str:
    c = _c()
    return f"{c['generated']}`{raw_bits}` ({c['binary']}) → **{decimal}** ({c['decimal']})"
