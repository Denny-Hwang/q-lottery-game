"""Per-game info blocks shown above the generator UI.

All images are served from the local ``src/`` folder so we never break when an
external CDN goes away.
"""
from __future__ import annotations

import streamlit as st

from i18n import get_lang

_COPY = {
    "lotto": {
        "ko": ("한국 로또 *Lotto 6/45*", "1부터 45 사이의 숫자 6개를 뽑습니다.", "https://dhlottery.co.kr/"),
        "en": ("Korea — *Lotto 6/45*", "Pick six numbers from 1 to 45.", "https://dhlottery.co.kr/"),
    },
    "powerball": {
        "ko": (
            "미국 *Powerball*",
            "흰 공 5개를 1~69 사이에서, 파워볼 1개를 1~26 사이에서 뽑습니다.",
            "https://www.powerball.com/",
        ),
        "en": (
            "USA — *Powerball*",
            "Pick five white balls from 1–69 and one Powerball from 1–26.",
            "https://www.powerball.com/",
        ),
    },
    "lotto_india": {
        "ko": (
            "인도 *Lotto India*",
            "1~50 사이의 숫자 6개와 1~5 사이의 조커 볼 1개를 뽑습니다.",
            "https://www.lotto.in/",
        ),
        "en": (
            "India — *Lotto India*",
            "Pick six numbers from 1–50 and one Joker ball from 1–5.",
            "https://www.lotto.in/",
        ),
    },
    "lotto7": {
        "ko": (
            "일본 *Lotto7*",
            "1~37 사이의 숫자 7개를 뽑습니다.",
            "https://en.lottolyzer.com/how-to-play/japan/lotto-7",
        ),
        "en": (
            "Japan — *Lotto7*",
            "Pick seven numbers from 1 to 37.",
            "https://en.lottolyzer.com/how-to-play/japan/lotto-7",
        ),
    },
    "french": {
        "ko": (
            "프랑스 *Loto*",
            "1~49 사이의 숫자 5개와 1~10 사이의 럭키 넘버 1개를 뽑습니다.",
            "http://france-lottery.com/",
        ),
        "en": (
            "France — *French Loto*",
            "Pick five numbers from 1–49 and one Lucky number from 1–10.",
            "http://france-lottery.com/",
        ),
    },
    "custom": {
        "ko": ("Custom Q-Lottery", "원하는 범위로 양자 난수를 직접 만들어 보세요.", None),
        "en": ("Custom Q-Lottery", "Customize the range of your quantum random numbers.", None),
    },
}


def _render(image_path: str | None, key: str, *, width: int = 280) -> None:
    title, body, link = _COPY[key].get(get_lang(), _COPY[key]["en"])
    if image_path:
        st.image(image_path, width=width, caption=title)
    st.title(title)
    st.write(body)
    if link:
        st.caption(f"🔗 [{link}]({link})")


def lotto_doc() -> None:
    _render("src/Lotto645.jpg", "lotto", width=320)


def powerball_doc() -> None:
    _render("src/Powerball.png", "powerball", width=260)


def lotto_india_doc() -> None:
    _render("src/logo.png", "lotto_india", width=260)


def lotto7_doc() -> None:
    _render("src/lotto7mediumlogo.png", "lotto7", width=260)


def french_lottery_doc() -> None:
    _render("src/Logo_FDJ.svg", "french", width=240)


def custom_doc() -> None:
    _render(None, "custom")
