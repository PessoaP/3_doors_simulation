import streamlit as st

st.title("🚪🚪🚪 The Monty Hall (or 3 doors) problem ")

if "step" not in st.session_state:
    st.session_state.step = 0

descriptions = [
    "You are in a game show. The host gives you the choice of **three doors**.",
    "Behind **one** door is a brand-new **car**, behind the others are **goats**.",
    "You pick a door.",
    "The host (who knows what's behind each door) opens **another** door, revealing a **goat**.",
    "The host then asks you: _Do you want to switch?_",
]

# Display text step-by-step
for i in range(st.session_state.step + 1):
    st.markdown(f"- {descriptions[i]}")

if st.session_state.step < len(descriptions) - 1:
    if st.button("▶ Next"):
        st.session_state.step += 1
        st.rerun()
else:
    st.success("Ready to play? Scroll down to try the simulator!")

st.title("🎲 Monty Hall Problem Simulation")

st.write("""
Pick a door. 
""")

# Initialize session state for game data
if "doors" not in st.session_state:
    st.session_state.doors = None
    st.session_state.choice = None
    st.session_state.monty_opens = None
    st.session_state.phase = "pick"

if st.session_state.phase == "pick":
    # Step 1: User picks a door
    choice = st.radio("Pick a door:", [1, 2, 3]) - 1
    if st.button("Let the host revel another door"):
        # Start game
        doors = ['goat', 'goat', 'car']
        random.shuffle(doors)

        # Monty reveals a goat behind a different door
        possible = [i for i in range(3) if i != choice and doors[i] == 'goat']
        monty_opens = random.choice(possible)

        # Save game state
        st.session_state.doors = doors
        st.session_state.choice = choice
        st.session_state.monty_opens = monty_opens
        st.session_state.phase = "switch"

        st.rerun()

elif st.session_state.phase == "switch":
    # Step 2: Reveal Monty's choice and ask user if they want to switch
    st.subheader("🎬 Game Summary")
    st.write(f"You picked **Door {st.session_state.choice + 1}**.")
    st.write(f"The host opened **Door {st.session_state.monty_opens + 1}**, revealing a goat.")

    trade = st.radio("Do you want to switch your choice?", ["Yes", "No"]) == "Yes"
    if st.button("Final Choice"):
        if trade:
            final_choice = [i for i in range(3)
                            if i != st.session_state.choice and i != st.session_state.monty_opens][0]
        else:
            final_choice = st.session_state.choice

        prize = st.session_state.doors[final_choice]

        if trade:
            st.write(f"You switched to **Door {final_choice + 1}**.")
        else:
            st.write(f"You stayed with your original choice.")

        st.write(f"Behind Door {final_choice + 1} was a **{prize.upper()}**.")
        if prize == 'car':
            st.success("🎉 You WON the car!")
        else:
            st.error("😢 You got a goat.")

        # Reset phase so you can play again
        st.session_state.phase = "pick"
