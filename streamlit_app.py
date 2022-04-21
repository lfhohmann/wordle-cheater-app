import streamlit as st
import pandas as pd


INTRO_TEXT = """
# Wordle Cheater

#### This is a **Cheating App** for the [**Wordle**](https://www.nytimes.com/games/wordle/index.html) game.

In order to use it, you will type, in the Wordle game, the *'suggested'* word shown on the left column. 
The game will output the *'hits'* and *'misses'* pattern of each character by color coding them.
On the right column text fields, you will type the *'hits'* and *'misses'* pattern of the word, following the pattern below:

+ ⬛ **B** (Black)
+ 🟨 **Y** (Yellow)
+ 🟩 **G** (Green)

For example, if, after typing the *'suggested'* word, the Wordle game outputs: ⬛🟨⬛⬛🟩, you will type **BYBBG**.
After entering the pattern, the app will show you the next *'suggested'* word.

The whole credit for the optimal words sequence data, goes to [**Alex Selby**](https://sonorouschocolate.com/notes/index.php?title=The_best_strategies_for_Wordle,_part_2#Using_larger_hidden_word_lists).
This app merely uses his data to help you cheat ; ).

+ On the **Data Table** you can visualize all the possible remaining patterns.
"""

# Defining constants
DIRPATH = "./data/output/"

WORD_LENGHT = 5
ATTEMPTS_NUMBER = 6

COLS_WIDTHS = (5, 20)


def reset_session():
    """Resets the session to a clean one"""

    # Reset all the 'text_input' values
    for i in range(ATTEMPTS_NUMBER):
        st.session_state[f"word_{i}"] = ""


def main():
    """Main function"""

    # Page configuration
    st.set_page_config(
        page_title="Wordle Cheater",
        page_icon="🎱",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Init mode selector and load data
    mode = st.sidebar.selectbox("Mode", ["Normal", "Hard"], key="mode_selector")
    data = pd.read_csv(f"{DIRPATH}{mode.lower()}.csv")

    # Create sidebar widgets
    st.sidebar.button("RESET GAME", on_click=reset_session)

    st.sidebar.title("Author")
    st.sidebar.markdown("[Lucas Hohmann](https://github.com/lfhohmann)")

    # Intro text
    st.markdown(INTRO_TEXT)

    # Init variables
    words = [data[f"word_0"].iloc[0]] + ["" for _ in range(ATTEMPTS_NUMBER - 1)]
    hits = ["" for _ in range(ATTEMPTS_NUMBER)]

    # Create layout columns
    col_word, col_hits = st.columns(COLS_WIDTHS)

    # Iterate over each attempt
    for i in range(ATTEMPTS_NUMBER):
        with col_hits:

            # Print suggested words
            hits[i] = st.text_input("", "", key=f"word_{i}").upper()

            # Check if the 'hits' are valid
            if hits[i] != "":

                # Filter DataFrame
                data = data[data[f"hits_{i}"] == f"{hits[i]}"]

                # Check if the 'hits' are valid
                if len(data) == 0:
                    st.error("Invalid input")
                    st.stop()

                # Insert suggested word in the list
                words[i + 1] = data[f"word_{i + 1}"].iloc[0]

            # Print the words
            with col_word:
                st.title(words[i].upper())

            # If no more 'hits' are given, stop the loop
            if hits[i] == "":
                break

    # Show the entire DataFrame inside an expander
    with st.expander("Data Table"):
        st.dataframe(data, height=600)


if __name__ == "__main__":
    main()
