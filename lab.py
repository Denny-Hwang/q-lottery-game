"""The interactive "Quantum Lab" page.

Walks the user through the full pipeline one step at a time:

    init → superposition → (phase) → (entangle) → measure/collapse → decode → ball

Heavy lifting (state math) lives in :mod:`q_state`; Bloch/Plotly rendering in
:mod:`bloch_viz`. This module is the Streamlit glue: a stepper, a Bloch grid,
probability bars, the growing circuit, the measurement collapse, and the
bit→decimal→lottery-number decode.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

import bloch_viz
from games import KOREAN_LOTTO_PALETTE
from i18n import t
from q_state import (
    MAX_LAB_BITS,
    bloch_length,
    circuit_stages,
    collapse_to_poles,
    decode_bits,
    sample_main_bits,
)
from ui import render_balls

_BLOCH_PER_ROW = 3


# ── Small helpers ───────────────────────────────────────────────────────────────
def _main_labels(num_main: int) -> list[str]:
    return [t("lab.qubit.main").format(i=q) for q in range(num_main)]


def _all_labels(num_main: int, num_ancilla: int) -> list[str]:
    labels = _main_labels(num_main)
    if num_ancilla:
        labels += [t("lab.qubit.month"), t("lab.qubit.day")]
    return labels


def _bloch_grid(vectors, labels, *, collapsed: bool, key_prefix: str) -> None:
    for start in range(0, len(vectors), _BLOCH_PER_ROW):
        end = min(start + _BLOCH_PER_ROW, len(vectors))
        cols = st.columns(end - start)
        for col, idx in zip(cols, range(start, end)):
            with col:
                fig = bloch_viz.bloch_figure(vectors[idx], label=labels[idx], collapsed=collapsed)
                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"displayModeBar": False},
                    key=f"{key_prefix}_{idx}",
                )


def _prob_grid(p0p1, labels, *, key_prefix: str) -> None:
    for start in range(0, len(p0p1), _BLOCH_PER_ROW):
        end = min(start + _BLOCH_PER_ROW, len(p0p1))
        cols = st.columns(end - start)
        for col, idx in zip(cols, range(start, end)):
            with col:
                st.caption(labels[idx])
                st.plotly_chart(
                    bloch_viz.probability_bar(p0p1[idx][1]),
                    width="stretch",
                    config={"displayModeBar": False},
                    key=f"{key_prefix}_{idx}",
                )


def _collapse_grid(befores, afters, labels, *, key_prefix: str) -> None:
    for start in range(0, len(afters), _BLOCH_PER_ROW):
        end = min(start + _BLOCH_PER_ROW, len(afters))
        cols = st.columns(end - start)
        for col, idx in zip(cols, range(start, end)):
            with col:
                fig = bloch_viz.collapse_animation(befores[idx], afters[idx], label=labels[idx])
                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"displayModeBar": False},
                    key=f"{key_prefix}_{idx}",
                )


def _draw_circuit(circuit) -> None:
    """Draw the partial circuit; prefer matplotlib, fall back to a text diagram."""
    fig = None
    try:  # mpl drawing needs pylatexenc on some setups; degrade gracefully.
        from qiskit.visualization import circuit_drawer

        fig = circuit_drawer(
            circuit, output="mpl", scale=0.8, style={"backgroundcolor": "#FFFFFF"}
        )
    except Exception:
        fig = None
    if fig is not None:
        st.pyplot(fig)
    else:
        st.code(str(circuit.draw(output="text")), language="text")


def _resample(final_stage) -> None:
    st.session_state["lab_measured"] = sample_main_bits(
        final_stage.statevector, final_stage.num_main
    )


# ── Stage / measure / decode views ──────────────────────────────────────────────
def _render_stage(stage) -> None:
    st.markdown(t(f"lab.explain.{stage.key}"))
    labels = _all_labels(stage.num_main, stage.num_ancilla)

    st.markdown(f"#### {t('lab.bloch.heading')}")
    _bloch_grid(stage.bloch, labels, collapsed=False, key_prefix=f"stage_{stage.key}")

    if stage.key == "entangle":
        lengths = [bloch_length(v) for v in stage.bloch[: stage.num_main]]
        mixed = [i for i, ln in enumerate(lengths) if ln < 0.999]
        if mixed:
            st.info(t("lab.entangle.note").format(qubits=", ".join(f"q{i}" for i in mixed)))

    st.markdown(f"#### {t('lab.prob.heading')}")
    _prob_grid(stage.p0p1, labels, key_prefix=f"prob_{stage.key}")
    st.caption(t("lab.prob.caption"))

    st.markdown(f"#### {t('lab.circuit.heading')}")
    _draw_circuit(stage.circuit)


def _render_measure(final_stage) -> None:
    st.markdown(t("lab.explain.measure"))
    labels = _main_labels(final_stage.num_main)
    measured = st.session_state.get("lab_measured")

    if measured is None:
        st.caption(t("lab.measure.before"))
        _bloch_grid(
            final_stage.bloch[: final_stage.num_main], labels,
            collapsed=False, key_prefix="meas_pre",
        )
        if st.button(t("lab.measure.button"), type="primary", width="stretch"):
            _resample(final_stage)
            st.rerun()
        return

    poles = collapse_to_poles(measured)
    befores = final_stage.bloch[: final_stage.num_main]
    _collapse_grid(befores, poles, labels, key_prefix="meas_anim")
    st.caption(t("lab.measure.play_hint"))
    st.success(t("lab.measure.result").format(bits=measured, dec=int(measured, 2)))
    st.caption(t("lab.measure.collapsed_caption"))
    if st.button(t("lab.measure.again"), width="stretch"):
        _resample(final_stage)
        st.rerun()


def _render_decode(final_stage, *, max_num: int) -> None:
    st.markdown(t("lab.explain.decode"))
    measured = st.session_state.get("lab_measured")
    if measured is None:
        st.warning(t("lab.decode.need_measure"))
        if st.button(t("lab.measure.button"), type="primary"):
            _resample(final_stage)
            st.rerun()
        return

    contributions, total = decode_bits(measured)
    table = [
        {
            t("lab.decode.col.qubit"): f"q{c.qubit}",
            t("lab.decode.col.bit"): c.bit,
            t("lab.decode.col.place"): c.place_value,
            t("lab.decode.col.contrib"): c.contribution,
        }
        for c in reversed(contributions)  # most-significant first, as written
    ]
    st.dataframe(pd.DataFrame(table), hide_index=True, width="stretch")

    terms = " + ".join(f"{c.bit}×{c.place_value}" for c in reversed(contributions))
    st.markdown(t("lab.decode.formula").format(terms=terms, total=total))

    if total < 1 or total > max_num:
        st.error(t("lab.decode.rejected").format(total=total, max=max_num))
        if st.button(t("lab.measure.again"), type="primary"):
            _resample(final_stage)
            st.rerun()
        return

    st.success(t("lab.decode.inrange").format(total=total, max=max_num))
    render_balls([total], upper_bound=max_num, palette=KOREAN_LOTTO_PALETTE)
    st.caption(t("lab.decode.ball_caption"))
    st.divider()
    st.info(t("lab.summary"))


# ── Public entry point ──────────────────────────────────────────────────────────
def render_lab() -> None:
    st.title(t("lab.title"))
    st.caption(t("lab.subtitle"))
    st.write(t("lab.intro"))
    st.divider()

    # ── Controls ────────────────────────────────────────────────────────────────
    bits = st.slider(t("lab.controls.bits"), min_value=1, max_value=MAX_LAB_BITS, value=3)
    c1, c2 = st.columns(2)
    phase_demo = c1.toggle(
        t("lab.controls.phase"), value=False, help=t("lab.controls.phase_help")
    )
    entangle = c2.toggle(
        t("lab.controls.entangle"),
        value=False,
        help=t("lab.controls.entangle_help"),
        disabled=(bits < 2),
    )

    birthday = None
    if entangle and bits >= 2:
        d1, d2 = st.columns(2)
        month = d1.number_input(t("lab.controls.month"), min_value=1, max_value=12, value=8)
        day = d2.number_input(t("lab.controls.day"), min_value=1, max_value=31, value=30)
        birthday = (int(month), int(day))

    max_cap = max(1, 2 ** bits - 1)
    max_num = st.number_input(
        t("lab.controls.maxnum"),
        min_value=1,
        max_value=max_cap,
        value=min(45, max_cap),
        help=t("lab.controls.maxnum_help"),
    )

    stages = circuit_stages(bits, birthday=birthday, phase_demo=phase_demo)
    stage_keys = [s.key for s in stages]
    view_keys = stage_keys + ["measure", "decode"]
    n_views = len(view_keys)

    # Reset progress + measurement whenever the experiment configuration changes.
    sig = (bits, phase_demo, birthday)
    if st.session_state.get("lab_sig") != sig:
        st.session_state["lab_sig"] = sig
        st.session_state["lab_step"] = 0
        st.session_state["lab_measured"] = None
    step = min(int(st.session_state.get("lab_step", 0)), n_views - 1)

    # ── Stepper navigation ──────────────────────────────────────────────────────
    st.divider()
    prev_col, mid_col, next_col = st.columns([1, 2, 1])
    if prev_col.button(t("lab.nav.prev"), disabled=(step == 0), width="stretch"):
        st.session_state["lab_step"] = step - 1
        st.rerun()
    if next_col.button(
        t("lab.nav.next"),
        disabled=(step == n_views - 1),
        width="stretch",
        type="primary",
    ):
        st.session_state["lab_step"] = step + 1
        st.rerun()
    current_key = view_keys[step]
    mid_col.markdown(
        f"<div style='text-align:center;padding-top:6px;color:#6B7280'>"
        f"{step + 1} / {n_views} · {t('lab.stage.' + current_key)}</div>",
        unsafe_allow_html=True,
    )
    st.progress((step + 1) / n_views)
    st.divider()

    # ── Current view ────────────────────────────────────────────────────────────
    if current_key in stage_keys:
        _render_stage(stages[stage_keys.index(current_key)])
    elif current_key == "measure":
        _render_measure(stages[-1])
    else:
        _render_decode(stages[-1], max_num=int(max_num))
