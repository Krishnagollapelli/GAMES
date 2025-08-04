
import streamlit as st
import random
import ascii_art

# Word pool
words_list = ["KRISHNA", "ASHA", "HEMA", "HARIKA"]

# Game initializer
def init_game():
    st.session_state.secret_word = random.choice(words_list)
    st.session_state.blank = ["_" for _ in st.session_state.secret_word]
    st.session_state.guessed_letters = []
    st.session_state.lives = 6
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.win = False

# Initialize session
if "secret_word" not in st.session_state:
    init_game()

# UI
st.title("🕹️ Hangman Game")
st.text(ascii_art.hangman_logo)

# Game Board
st.markdown(f"### Word: {' '.join(st.session_state.blank)}")
st.markdown(ascii_art.hangman_stages[6 - st.session_state.lives])
st.markdown(f"**Lives Remaining:** {st.session_state.lives}")
st.markdown(f"**Guessed Letters:** {', '.join(st.session_state.guessed_letters)}")
st.write(st.session_state.message)

# Player Input
if not st.session_state.game_over:
    guess = st.text_input("Enter a letter:", max_chars=1).upper()

    if guess and guess.isalpha():
        if guess in st.session_state.guessed_letters:
            st.session_state.message = "⚠️ You've already guessed this letter."
        else:
            st.session_state.guessed_letters.append(guess)
            if guess in st.session_state.secret_word:
                for i, letter in enumerate(st.session_state.secret_word):
                    if letter == guess:
                        st.session_state.blank[i] = letter
                st.session_state.message = "✅ Correct guess!"
            else:
                st.session_state.lives -= 1
                st.session_state.message = "❌ Wrong guess."

        # Win/Loss Check
        if "_" not in st.session_state.blank:
            st.session_state.game_over = True
            st.session_state.win = True
            st.balloons()
        elif st.session_state.lives == 0:
            st.session_state.game_over = True
            st.session_state.win = False

# Result
if st.session_state.game_over:
    if st.session_state.win:
        st.success("🎉 You win!")
    else:
        st.error("💀 You lose!")
        st.info(f"The word was: **{st.session_state.secret_word}**")

    if st.button("🔁 Play Again"):
        init_game()
