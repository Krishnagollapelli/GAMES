# hangman_app.py

import streamlit as st
import random
import ascii_art

# Word list
words_list = ["KRISHNA", "ASHA", "HEMA", "HARIKA"]

# Initialize game
def init_game():
    st.session_state.secret_word = random.choice(words_list)
    st.session_state.blank = ["_" for _ in st.session_state.secret_word]
    st.session_state.guessed_letters = []
    st.session_state.lives = 6
    st.session_state.game_over = False
    st.session_state.win = False
    st.session_state.message = ""

# Setup session state
if "secret_word" not in st.session_state:
    init_game()

# Title and Logo
st.title("🕹️ Hangman Game")
st.code(ascii_art.hangman_logo)

# Display current game state
st.subheader(f"Word: {' '.join(st.session_state.blank)}")
st.code(ascii_art.hangman_stages[6 - st.session_state.lives])
st.markdown(f"**Lives Left:** {st.session_state.lives}")
st.markdown(f"**Guessed Letters:** {', '.join(st.session_state.guessed_letters)}")
st.markdown(st.session_state.message)

# Game input logic
if not st.session_state.game_over:
    guess = st.text_input("Enter a letter:", key="input").upper()

    if guess:
        if not guess.isalpha() or len(guess) != 1:
            st.session_state.message = "⚠️ Please enter a single alphabet letter."
        elif guess in st.session_state.guessed_letters:
            st.session_state.message = "⚠️ You've already guessed that letter!"
        else:
            st.session_state.guessed_letters.append(guess)
            if guess in st.session_state.secret_word:
                for i, char in enumerate(st.session_state.secret_word):
                    if char == guess:
                        st.session_state.blank[i] = guess
                st.session_state.message = "✅ Correct guess!"
            else:
                st.session_state.lives -= 1
                st.session_state.message = "❌ Wrong guess!"

        # Check win or lose
        if "_" not in st.session_state.blank:
            st.session_state.game_over = True
            st.session_state.win = True
            st.balloons()
        elif st.session_state.lives == 0:
            st.session_state.game_over = True
            st.session_state.win = False

# Show result if game over
if st.session_state.game_over:
    if st.session_state.win:
        st.success("🎉 Congratulations, you won!")
    else:
        st.error("💀 You lost! Better luck next time.")
        st.info(f"The correct word was: **{st.session_state.secret_word}**")

    if st.button("🔁 Play Again"):
        init_game()
