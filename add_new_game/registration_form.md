# Add a new Q-Lottery game

Want to add another country's lottery? Follow these three steps and send a PR.

## 1) Add the official logo

Drop the **official** logo (PNG/SVG) into the `src/` folder.

## 2) Register the game in `games.py`

```python
"YourGame(Country)": GameConfig(
    doc_fn=your_game_doc,
    ball_labels=["Num_1", "Num_2", ...],
    main_count=6,
    main_upper_bound=49,
    bonus_upper_bound=None,        # or e.g. 10 if your game has a bonus ball
    col_prefix="Q-yourgame",
    main_palette=PALETTES["rainbow"],   # any palette defined in ui.py
    bonus_palette=None,
),
```

## 3) Add a short doc in `game_doc.py`

```python
def your_game_doc():
    st.image("src/your_logo.png", width=300)
    st.title("YourGame Q-Lottery Game")
    st.write("Brief game rules and a link to the official site.")
```

That's it — open a PR. Thanks!
