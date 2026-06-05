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
    "sidebar.lab": {"ko": "🔬 양자 실험실", "en": "🔬 Quantum Lab"},
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
    # ── Quantum Lab (interactive learning page) ────────────────────────────
    "lab.title": {"ko": "🔬 양자 실험실", "en": "🔬 Quantum Lab"},
    "lab.subtitle": {
        "ko": "블로흐 구에서 시작해 내 로또 번호가 되기까지, 한 단계씩 직접 체험",
        "en": "Experience every step, from the Bloch sphere to your lottery number",
    },
    "lab.intro": {
        "ko": "아래 단계를 따라가며 양자 난수가 **어떻게** 만들어지는지 눈으로 확인해 보세요. "
              "큐비트 개수·위상·얽힘을 바꿔가며 자유롭게 실험할 수 있어요.",
        "en": "Follow the steps below to *see* how a quantum random number is born. "
              "Experiment freely by changing the number of qubits, phase, and entanglement.",
    },
    # Controls
    "lab.controls.bits": {"ko": "큐비트(비트) 개수", "en": "Number of qubits (bits)"},
    "lab.controls.phase": {"ko": "위상 게이트 추가 (T)", "en": "Add a phase gate (T)"},
    "lab.controls.phase_help": {
        "ko": "H 다음에 T 게이트를 끼워 적도 위에서 위상이 회전하는 모습을 봅니다. 측정 확률은 그대로!",
        "en": "Insert a T gate after H to watch the phase spin around the equator. Probabilities stay 50/50!",
    },
    "lab.controls.entangle": {"ko": "생일 얽힘 추가 (CRY)", "en": "Add birthday entanglement (CRY)"},
    "lab.controls.entangle_help": {
        "ko": "생일 보조 큐비트를 CRY로 얽혀 블로흐 벡터가 수축하는 모습을 봅니다. 2비트 이상 필요.",
        "en": "Entangle birthday ancillas via CRY and watch the Bloch vector shrink. Needs ≥ 2 bits.",
    },
    "lab.controls.month": {"ko": "생월", "en": "Birth month"},
    "lab.controls.day": {"ko": "생일", "en": "Birth day"},
    "lab.controls.maxnum": {"ko": "로또 범위 최댓값", "en": "Lottery max number"},
    "lab.controls.maxnum_help": {
        "ko": "디코딩한 십진수가 1 ~ 이 값 범위면 채택, 아니면 재추첨(rejection).",
        "en": "A decoded number in 1…this value is accepted; otherwise it is rejected and redrawn.",
    },
    # Stepper navigation + short stage names
    "lab.nav.prev": {"ko": "◀ 이전", "en": "◀ Back"},
    "lab.nav.next": {"ko": "다음 ▶", "en": "Next ▶"},
    "lab.stage.init": {"ko": "① 초기화", "en": "① Initialize"},
    "lab.stage.superposition": {"ko": "② 중첩", "en": "② Superposition"},
    "lab.stage.phase": {"ko": "③ 위상", "en": "③ Phase"},
    "lab.stage.entangle": {"ko": "④ 얽힘", "en": "④ Entangle"},
    "lab.stage.measure": {"ko": "⑤ 측정", "en": "⑤ Measure"},
    "lab.stage.decode": {"ko": "⑥ 디코딩", "en": "⑥ Decode"},
    # Stage explanations
    "lab.explain.init": {
        "ko": "### ① 초기화 — 모든 큐비트는 |0⟩\n"
              "양자 컴퓨터의 큐비트는 항상 **|0⟩ 상태**에서 출발합니다. 블로흐 구에서 |0⟩은 "
              "**북극**을 가리키는 화살표예요. 아직 아무 일도 없었으니 측정하면 100% 확률로 0이 나옵니다.",
        "en": "### ① Initialize — every qubit starts at |0⟩\n"
              "Qubits always begin in the **|0⟩ state**. On the Bloch sphere, |0⟩ is the arrow pointing "
              "at the **north pole**. Nothing random yet: measuring now gives 0 with 100% probability.",
    },
    "lab.explain.superposition": {
        "ko": "### ② 중첩 — H 게이트로 적도로\n"
              "**아다마르(H) 게이트**는 화살표를 북극에서 **적도**로 눕힙니다. 이제 큐비트는 0과 1을 "
              "**동시에** 품은 중첩 상태가 되어, 측정하면 **50:50**으로 0 또는 1이 나옵니다. "
              "이것이 양자 동전 던지기, 곧 진짜 난수의 원천입니다.",
        "en": "### ② Superposition — H tips the arrow to the equator\n"
              "The **Hadamard (H) gate** rotates the arrow from the north pole down to the **equator**. "
              "The qubit now holds 0 and 1 **at the same time**; measuring yields 0 or 1 with **50/50** odds. "
              "This quantum coin flip is the source of true randomness.",
    },
    "lab.explain.phase": {
        "ko": "### ③ 위상 — 적도 위에서 도는 화살표\n"
              "**위상(phase) 게이트**(여기선 T)는 화살표를 적도 위에서 빙글 돌립니다. 신기하게도 "
              "**측정 확률(P0, P1)은 전혀 변하지 않아요** — 아래 확률 막대를 보세요. 위상은 측정값을 "
              "직접 바꾸지 않지만, 여러 큐비트가 **간섭(interference)** 할 때 결정적인 역할을 합니다.",
        "en": "### ③ Phase — spinning around the equator\n"
              "A **phase gate** (here, T) spins the arrow *around* the equator. Remarkably, the "
              "**measurement probabilities (P0, P1) don't change at all** — check the bars below. Phase "
              "doesn't move the odds directly, but it is what makes **interference** between qubits possible.",
    },
    "lab.explain.entangle": {
        "ko": "### ④ 얽힘 — 생일 보조 큐비트와 연결\n"
              "**CRY 게이트**가 생일(월·일) 보조 큐비트를 메인 큐비트와 **얽히게** 합니다. 얽힌 큐비트는 "
              "더 이상 혼자만의 상태를 갖지 않아서, 블로흐 화살표의 **길이가 1보다 짧아집니다(|r|<1)**. "
              "'부분만 떼어 보면 상태가 흐려진다' — 이것이 얽힘의 핵심입니다.",
        "en": "### ④ Entanglement — linking the birthday ancillas\n"
              "The **CRY gate** entangles the birthday (month/day) ancillas with the result qubits. An "
              "entangled qubit no longer has a state of its own, so its Bloch arrow **shrinks below length "
              "1 (|r|<1)**. 'Look at only part of an entangled system and it goes fuzzy' — that's entanglement.",
    },
    "lab.explain.measure": {
        "ko": "### ⑤ 측정 — 중첩이 collapse!\n"
              "측정하는 순간 중첩이 깨지고, 각 큐비트는 **0 또는 1로 확정**됩니다. 적도에 있던 화살표가 "
              "**북극(0·파랑)** 또는 **남극(1·빨강)** 으로 탁 붙어요. 어느 쪽이 될지는 위에서 본 확률을 "
              "따릅니다. 버튼을 눌러 직접 collapse 시켜 보세요!",
        "en": "### ⑤ Measurement — the collapse!\n"
              "Measuring breaks the superposition: each qubit snaps to a **definite 0 or 1**. The equator "
              "arrow jumps to the **north pole (0, blue)** or the **south pole (1, red)**, following the odds "
              "you just saw. Press the button to collapse it yourself!",
    },
    "lab.explain.decode": {
        "ko": "### ⑥ 디코딩 — 비트열에서 내 로또 번호로\n"
              "측정으로 얻은 비트열을 **자리값(1, 2, 4, 8, …)** 에 따라 더하면 하나의 **십진수**가 됩니다. "
              "그 수가 로또 범위 안이면 번호로 채택하고, 벗어나면 버리고 다시 뽑습니다(**rejection sampling**). "
              "이렇게 *진짜* 양자 난수가 내 번호가 됩니다.",
        "en": "### ⑥ Decode — from bits to your lottery number\n"
              "Add up the measured bits weighted by their **place values (1, 2, 4, 8, …)** to get a single "
              "**decimal number**. If it lands inside the lottery range we keep it; if not, we throw it away "
              "and draw again (**rejection sampling**). That's how a *real* quantum random number becomes your pick.",
    },
    # Bloch / probability / circuit sections
    "lab.bloch.heading": {"ko": "블로흐 구 (드래그하면 돌아갑니다)", "en": "Bloch spheres (drag to rotate)"},
    "lab.prob.heading": {"ko": "측정 확률", "en": "Measurement probabilities"},
    "lab.prob.caption": {
        "ko": "파랑 = 0이 나올 확률, 빨강 = 1이 나올 확률.",
        "en": "Blue = chance of measuring 0, red = chance of measuring 1.",
    },
    "lab.circuit.heading": {"ko": "지금까지의 회로", "en": "The circuit so far"},
    "lab.qubit.main": {"ko": "q{i}", "en": "q{i}"},
    "lab.qubit.month": {"ko": "월(보조)", "en": "month (anc.)"},
    "lab.qubit.day": {"ko": "일(보조)", "en": "day (anc.)"},
    "lab.entangle.note": {
        "ko": "🔗 {qubits} 의 화살표가 짧아졌나요? 얽힘 때문에 '부분 상태'가 혼합되어 |r|<1 이 된 것입니다.",
        "en": "🔗 Notice {qubits} got shorter? Entanglement makes the reduced state mixed, so |r| < 1.",
    },
    # Measurement view
    "lab.measure.before": {
        "ko": "지금은 중첩 상태입니다. 측정 버튼을 누르면 collapse 됩니다.",
        "en": "Still in superposition — press measure to make it collapse.",
    },
    "lab.measure.button": {"ko": "🎲 측정하기", "en": "🎲 Measure"},
    "lab.measure.again": {"ko": "🔄 다시 측정", "en": "🔄 Measure again"},
    "lab.measure.result": {
        "ko": "측정 결과: `{bits}` (2진) → **{dec}** (10진)",
        "en": "Result: `{bits}` (binary) → **{dec}** (decimal)",
    },
    "lab.measure.collapsed_caption": {
        "ko": "각 큐비트가 북극(0)·남극(1)으로 확정되었습니다.",
        "en": "Every qubit has snapped to the north (0) or south (1) pole.",
    },
    # Decode view
    "lab.decode.need_measure": {
        "ko": "먼저 ⑤ 측정 단계에서 측정해 주세요.",
        "en": "Please run a measurement in step ⑤ first.",
    },
    "lab.decode.col.qubit": {"ko": "큐비트", "en": "Qubit"},
    "lab.decode.col.bit": {"ko": "비트", "en": "Bit"},
    "lab.decode.col.place": {"ko": "자리값", "en": "Place value"},
    "lab.decode.col.contrib": {"ko": "기여값", "en": "Contributes"},
    "lab.decode.formula": {"ko": "**{terms} = {total}**", "en": "**{terms} = {total}**"},
    "lab.decode.rejected": {
        "ko": "❌ {total} 은(는) 1~{max} 범위 밖이라 버려집니다 → 다시 측정해요 (rejection sampling).",
        "en": "❌ {total} is outside 1–{max}, so it is rejected → draw again (rejection sampling).",
    },
    "lab.decode.inrange": {
        "ko": "✅ {total} 은(는) 1~{max} 범위 안! 로또 번호로 채택합니다.",
        "en": "✅ {total} is within 1–{max} — accepted as a lottery number!",
    },
    "lab.decode.ball_caption": {
        "ko": "축하해요! 이 공이 바로 양자 난수로 뽑은 번호입니다.",
        "en": "Congrats — this ball is your quantum-drawn number.",
    },
    "lab.summary": {
        "ko": "🎉 |0⟩ → H(중첩) → 측정(collapse) → 비트열 → 십진수 → 로또 번호! "
              "이 과정을 번호 개수만큼 반복하면 한 게임이 완성됩니다.",
        "en": "🎉 |0⟩ → H (superposition) → measurement (collapse) → bits → decimal → lottery number! "
              "Repeat this for each number to complete a full game.",
    },
    "lab.cta": {
        "ko": "🔬 **양자 실험실**에서 블로흐 구로 난수가 만들어지는 과정을 단계별로 직접 "
              "체험해 보세요! (왼쪽 메뉴 → 🔬 양자 실험실)",
        "en": "🔬 Try the **Quantum Lab** to step through how randomness is born on the Bloch "
              "sphere! (sidebar → 🔬 Quantum Lab)",
    },
    "details.lab_hint": {
        "ko": "🔬 블로흐 구와 측정 collapse를 인터랙티브하게 보고 싶다면 왼쪽 메뉴의 **양자 실험실**을 열어보세요.",
        "en": "🔬 Want an interactive Bloch sphere and collapse view? Open the **Quantum Lab** from the sidebar.",
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
