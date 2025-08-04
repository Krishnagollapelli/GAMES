import streamlit as st
import random

# Constants
tile_types = (0, 1, 2, 3, 4, 5)
colors_map = {
    0: "#FF4B4B",   # red
    1: "#1DB954",   # green
    2: "#3B82F6",   # blue
    3: "#FFD700",   # yellow
    4: "#00CED1",   # cyan
    5: "#A020F0",   # purple
}

board_width = 20
board_height = 12
moves_per_game = 20

# Functions
def get_new_board():
    board = {}
    for x in range(board_width):
        for y in range(board_height):
            board[(x, y)] = random.choice(tile_types)
    for _ in range(board_width * board_height):
        x = random.randint(0, board_width - 2)
        y = random.randint(0, board_height - 1)
        board[(x + 1, y)] = board[(x, y)]
    return board

def change_tile(tile_color, board, x, y, color_to_change=None):
    if color_to_change is None:
        color_to_change = board[(x, y)]
        if tile_color == color_to_change:
            return
    board[(x, y)] = tile_color

    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < board_width and 0 <= ny < board_height:
            if board[(nx, ny)] == color_to_change:
                change_tile(tile_color, board, nx, ny, color_to_change)

def has_won(board):
    target = board[(0, 0)]
    return all(board[(x, y)] == target for x in range(board_width) for y in range(board_height))

def display_board(board):
    grid_html = '<div style="display: grid; grid-template-columns: repeat({}, 20px); gap: 1px;">'.format(board_width)
    for y in range(board_height):
        for x in range(board_width):
            color = colors_map[board[(x, y)]]
            grid_html += f'<div style="width: 20px; height: 20px; background-color: {color}; border-radius: 3px;"></div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

# Initialize Streamlit Session
if "board" not in st.session_state:
    st.session_state.board = get_new_board()
    st.session_state.moves_left = moves_per_game
    st.session_state.game_over = False

# Title
st.title("🎮 Flooder Game")
st.markdown("Fill the board with a single color within limited moves!")

# Game Status
display_board(st.session_state.board)
st.write("🎯 Moves left:", st.session_state.moves_left)

# Game Controls
if not st.session_state.game_over:
    col1, col2 = st.columns(2)
    with col1:
        color_choice = st.radio("Pick a color:", options=list(colors_map.keys()),
            format_func=lambda x: list(colors_map.keys())[x], horizontal=True,
            captions=["Red", "Green", "Blue", "Yellow", "Cyan", "Purple"]
        )
        if st.button("Flood"):
            change_tile(color_choice, st.session_state.board, 0, 0)
            st.session_state.moves_left -= 1

            if has_won(st.session_state.board):
                st.success("🎉 You have won the game!")
                st.session_state.game_over = True
            elif st.session_state.moves_left == 0:
                st.error("❌ You have run out of moves!")
                st.session_state.game_over = True

    with col2:
        st.markdown("### 🛠 Reset Game")
        if st.button("Restart"):
            st.session_state.board = get_new_board()
            st.session_state.moves_left = moves_per_game
            st.session_state.game_over = False

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
