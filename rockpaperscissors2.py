import streamlit as st
import numpy as np

st.title("🎮 Rock - Paper - Scissors Multiplayer Game")

st.header("Game Setup")

# --- Player Count ---
numOfPlayers = st.number_input(
    "How many players are going to be playing?",
    min_value=1, step=1
)

# --- Round Count ---
numOfRounds = st.number_input(
    "How many rounds do you want to play? (Minimum is 3)",
    min_value=3, step=1
)

# --- Enter Player Names ---
players = []
st.subheader("Enter Player Names")
for i in range(numOfPlayers):
    name = st.text_input(f"Name of Player {i+1}", key=f"player_{i}")
    if name:
        players.append(name)

def win(computerChoice, userChoice):
    if (
        (userChoice == "Rock" and computerChoice == "Scissors") or
        (userChoice == "Scissors" and computerChoice == "Paper") or
        (userChoice == "Paper" and computerChoice == "Rock")
    ):
        return True
    return False


# --- Start Button ---
if st.button("Start Game"):
    if len(players) != numOfPlayers:
        st.error("Please fill in all player names before starting the game.")
    else:
        st.success("Game Started! Scroll down to play each round.")
        st.session_state["players"] = players
        st.session_state["rounds"] = numOfRounds
        st.session_state["scoreboard"] = {p: 0 for p in players}


# --- Actual Gameplay ---
if "players" in st.session_state:
    st.header("Play Game")

    for player in st.session_state["players"]:
        st.subheader(f"{player}'s Turn")

        for round_num in range(st.session_state["rounds"]):
            st.write(f"### Round {round_num + 1}")

            user_choice = st.radio(
                f"{player}, choose:",
                ["Rock", "Paper", "Scissors"],
                key=f"{player}_round_{round_num}"
            )

            if st.button(f"Submit choice for {player} Round {round_num+1}",
                         key=f"btn_{player}_{round_num}"):
                computerChoice = np.random.choice(["Rock", "Paper", "Scissors"])

                st.write(f"Computer chose **{computerChoice}**")

                if win(computerChoice, user_choice):
                    st.success("You won this round!")
                    st.session_state["scoreboard"][player] += 1
                else:
                    st.error("You lost this round!")


# --- Display Scores ---
if "scoreboard" in st.session_state:
    st.header("📊 Scoreboard")
    st.write(st.session_state["scoreboard"])

    # Determine winners & losers
    scores = st.session_state["scoreboard"]
    playerwithmax = max(scores, key=scores.get)
    playerwithmin = min(scores, key=scores.get)

    st.success(f"🏆 **Highest Scoring Player:** {playerwithmax} with {scores[playerwithmax]} points")
    st.warning(f"😞 **Lowest Scoring Player:** {playerwithmin} with {scores[playerwithmin]} points")
