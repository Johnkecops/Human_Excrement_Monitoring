#!/usr/bin/env python3
"""
POE.LOG — Water Intake Applet Based on Human Excrement
Streamlit frontend

Based on: Swastika N. et al. (2021). Jurnal Riset Informatika, 3(2), 109–118.
Run: streamlit run app.py
"""

import streamlit as st

from water_intake_logic import (
    URINE_COLORS,
    STOOL_TYPES,
    get_urine_result,
    get_stool_result,
    append_to_history,
    read_history,
    clear_history,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="POE.LOG — Water Intake Tracker",
    page_icon="💧",
    layout="centered",
)

# ── Global CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    /* Brand title */
    .brand {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-align: center;
        background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.4rem 0 0.2rem;
    }
    .brand-sub {
        text-align: center;
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1.6rem;
    }
    /* Color swatch */
    .color-swatch {
        height: 72px;
        border-radius: 10px;
        border: 2px solid #d1d5db;
        margin-bottom: 0.35rem;
        transition: transform 0.1s;
    }
    /* Result card */
    .result-card {
        border-radius: 14px;
        padding: 1.8rem 1.4rem;
        text-align: center;
        margin: 1rem 0 1.4rem;
    }
    .result-emoji { font-size: 2.8rem; }
    .result-msg {
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0.6rem 0 0.3rem;
    }
    .result-advice { font-size: 1rem; color: #374151; }
    /* History row */
    .hist-row {
        font-family: monospace;
        font-size: 0.82rem;
        background: #f3f4f6;
        padding: 0.38rem 0.75rem;
        border-radius: 6px;
        margin: 0.18rem 0;
        border-left: 3px solid #93c5fd;
    }
    /* Bristol table */
    .bristol-chip {
        display: inline-block;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 6px;
        padding: 0.25rem 0.6rem;
        font-size: 0.78rem;
        margin-bottom: 0.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state bootstrap ───────────────────────────────────────────────────

defaults = {
    "page": "menu",
    "pee_color": None,
    "pee_result": None,
    "stool_type": None,
    "stool_result": None,
    "notif_pee": True,
    "notif_poo": True,
    "sleep_start": None,
    "sleep_end": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def nav(page: str) -> None:
    st.session_state.page = page


# ── Helper: result card ───────────────────────────────────────────────────────

def render_result_card(result: dict) -> None:
    st.markdown(
        f"""
        <div class="result-card" style="background:{result['color']};">
            <div class="result-emoji">{result['emoji']}</div>
            <div class="result-msg">{result['message']}</div>
            <div class="result-advice">{result['advice']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MENU
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.page == "menu":
    st.markdown('<div class="brand">POE.LOG</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-sub">Water Intake Tracker — hydration insights from your excrement</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💧 Pee Log", use_container_width=True, type="primary"):
            nav("pee_log")
            st.rerun()
    with c2:
        if st.button("💩 Poo Log", use_container_width=True, type="primary"):
            nav("poo_log")
            st.rerun()
    with c3:
        if st.button("⚙️ Settings", use_container_width=True):
            nav("settings")
            st.rerun()

    st.write("")
    if st.button("📋 View History", use_container_width=True):
        nav("history")
        st.rerun()

    st.markdown("---")
    st.caption(
        "Based on: Swastika N. et al. (2021). *Water Intake Applet Based on Human Excrement*. "
        "Jurnal Riset Informatika, 3(2), 109–118."
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PEE LOG
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "pee_log":
    st.subheader("💧 Pee Log")
    st.write("Select the color that best matches your urine.")
    st.caption(
        "Colors 1–3: well hydrated · Color 4: mild dehydration · "
        "Color 5: dehydrated · Color 6: severely dehydrated"
    )
    st.write("")

    # 2 rows × 3 columns
    rows = [st.columns(3), st.columns(3)]
    flat_cols = rows[0] + rows[1]

    for idx, (color, col) in enumerate(zip(URINE_COLORS, flat_cols)):
        with col:
            st.markdown(
                f'<div class="color-swatch" style="background:{color["hex"]};"></div>',
                unsafe_allow_html=True,
            )
            if st.button(
                f"Color {idx + 1}",
                key=f"pee_btn_{idx}",
                help=color["label"],
                use_container_width=True,
            ):
                st.session_state.pee_color = idx
                st.session_state.pee_result = get_urine_result(idx)
                nav("pee_result")
                st.rerun()
            st.caption(color["label"])

    st.write("")
    if st.button("← Back to Menu"):
        nav("menu")
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PEE RESULT
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "pee_result":
    if st.session_state.pee_result is None:
        nav("pee_log")
        st.rerun()

    result = st.session_state.pee_result
    color_idx = st.session_state.pee_color
    selected_color = URINE_COLORS[color_idx]

    st.subheader("💧 Pee Result")

    # Show selected swatch
    st.markdown(
        f'<div style="background:{selected_color["hex"]}; height:36px; '
        f'border-radius:8px; border:1px solid #d1d5db; margin-bottom:0.6rem;">'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Selected: Color {color_idx + 1} — {selected_color['label']}")

    render_result_card(result)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Back", use_container_width=True):
            nav("pee_log")
            st.rerun()
    with c2:
        if st.button("Submit ✓", use_container_width=True, type="primary"):
            append_to_history("Pee", result["log_label"])
            st.success("Entry saved to history log.")
            nav("menu")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: POO LOG
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "poo_log":
    st.subheader("💩 Poo Log")
    st.write("Select the type that best describes your stool consistency.")

    st.info(
        "**Bristol Stool Chart** — Types 3 and 4 are normal. "
        "Types 1–2 suggest constipation. Types 5–7 suggest looser stools.",
        icon="ℹ️",
    )
    st.write("")

    # Emoji stand-ins for stool textures
    stool_emojis = {1: "⚫⚫⚫", 2: "🟤🟤", 3: "🟤", 4: "🟤", 5: "💧🟤", 6: "💧💧", 7: "💧"}

    for stool in STOOL_TYPES:
        t = stool["type"]
        label = f"**Type {t}** — {stool['label']}"
        c1, c2 = st.columns([1, 6])
        with c1:
            st.write(stool_emojis[t])
        with c2:
            if st.button(label, key=f"stool_btn_{t}", use_container_width=True):
                st.session_state.stool_type = t
                st.session_state.stool_result = get_stool_result(t)
                nav("poo_result")
                st.rerun()

    st.write("")
    if st.button("← Back to Menu"):
        nav("menu")
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: POO RESULT
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "poo_result":
    if st.session_state.stool_result is None:
        nav("poo_log")
        st.rerun()

    result = st.session_state.stool_result
    stool_type = st.session_state.stool_type
    stool_info = next(s for s in STOOL_TYPES if s["type"] == stool_type)

    st.subheader("💩 Poo Result")
    st.caption(f"Selected: Type {stool_type} — {stool_info['label']}")

    render_result_card(result)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Back", use_container_width=True):
            nav("poo_log")
            st.rerun()
    with c2:
        if st.button("Submit ✓", use_container_width=True, type="primary"):
            append_to_history("Stool", result["log_label"])
            st.success("Entry saved to history log.")
            nav("menu")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HISTORY
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "history":
    st.subheader("📋 History Log")

    entries = read_history()

    if not entries:
        st.info("No entries logged yet. Start by submitting a Pee or Poo log entry.")
    else:
        st.caption(f"{len(entries)} entries — newest first")
        for entry in entries:
            st.markdown(
                f'<div class="hist-row">{entry}</div>',
                unsafe_allow_html=True,
            )

        st.write("")
        if st.button("🗑️ Clear All History", type="secondary"):
            clear_history()
            st.success("History cleared.")
            st.rerun()

    st.write("")
    if st.button("← Back to Menu"):
        nav("menu")
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.page == "settings":
    st.subheader("⚙️ Settings")
    st.write("")

    st.markdown("**Notifications**")
    notif_pee = st.toggle(
        "Pee Input notifications",
        value=st.session_state.notif_pee,
        help="Send a reminder if no pee log is detected after 2 hours.",
    )
    notif_poo = st.toggle(
        "Poo Input notifications",
        value=st.session_state.notif_poo,
        help="Send a reminder if no poo log is detected after 1 week.",
    )

    st.write("")
    st.markdown("**Set Sleep Time**")
    st.caption("Notifications are suppressed during sleep hours.")

    c1, c2 = st.columns(2)
    with c1:
        sleep_start = st.time_input("Bedtime", value=st.session_state.sleep_start)
    with c2:
        sleep_end = st.time_input("Wake-up time", value=st.session_state.sleep_end)

    st.write("")
    if st.button("Save Settings", type="primary", use_container_width=True):
        st.session_state.notif_pee = notif_pee
        st.session_state.notif_poo = notif_poo
        st.session_state.sleep_start = sleep_start
        st.session_state.sleep_end = sleep_end
        st.success(
            f"Settings saved. Sleep window: {sleep_start} → {sleep_end}. "
            f"Pee notifications: {'ON' if notif_pee else 'OFF'}. "
            f"Poo notifications: {'ON' if notif_poo else 'OFF'}."
        )

    st.write("")
    if st.button("← Back to Menu"):
        nav("menu")
        st.rerun()
