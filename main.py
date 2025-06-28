import random
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Monty Hall Simulator", page_icon="🚪")
st.cache_data.clear()

# -------------------------------
# Introductory Explanation
# -------------------------------
st.title("🚪🚪🚪 The Monty Hall (or 3 doors) Problem")

st.markdown("""
- You are in a game show. The host gives you the choice of **three doors**.  
- Behind **one** door is a brand-new **car**, behind the others are **goats**.  
- You pick a door.  
- The host (who knows what's behind each door) opens **another** door, revealing a **goat**.  
- The host then asks you: _Do you want to switch?_  
""")

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button("🎮 Start Game"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# -------------------------------
# Game Simulation
# -------------------------------
st.header("🎲 Monty Hall Problem Simulation")
st.markdown("<p style='font-size:18px;'>Pick a door:</p>", unsafe_allow_html=True)
st.write("🚪  🚪  🚪")

# Initialize game state
if "doors" not in st.session_state:
    st.session_state.doors = None
    st.session_state.choice = None
    st.session_state.monty_opens = None
    st.session_state.phase = "pick"

if st.session_state.phase == "pick":
    choice = st.radio("Which door do you choose?", [1, 2, 3]) - 1
    if st.button("Let the host reveal another door"):
        doors = ['goat', 'goat', 'car']
        random.shuffle(doors)

        possible = [i for i in range(3) if i != choice and doors[i] == 'goat']
        monty_opens = random.choice(possible)

        st.session_state.doors = doors
        st.session_state.choice = choice
        st.session_state.monty_opens = monty_opens
        st.session_state.phase = "switch"
        st.rerun()

elif st.session_state.phase == "switch":
    choice = st.session_state.choice
    monty_opens = st.session_state.monty_opens
    doors = st.session_state.doors

    st.subheader("🎬 Game Summary")
    st.markdown(f"<p style='font-size:18px;'>You picked <strong>Door {choice + 1}</strong>.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:18px;'>The host opened <strong>Door {monty_opens + 1}</strong>, revealing a 🐐.</p>", unsafe_allow_html=True)

    # Display current door state with Monty’s door revealed
    door_display = ["🚪"] * 3
    door_display[monty_opens] = "🐐"
    st.markdown("<p style='font-size:24px;'>" + "  ".join(door_display) + "</p>", unsafe_allow_html=True)

    trade = st.radio("Do you want to switch your choice?", ["Yes", "No"]) == "Yes"

    if st.button("Final Choice"):
        if trade:
            final_choice = [i for i in range(3) if i != choice and i != monty_opens][0]
        else:
            final_choice = choice

        prize = doors[final_choice]

        st.markdown("<p style='font-size:18px;'>Revealing your door...</p>", unsafe_allow_html=True)
        time.sleep(1.5)

        # Update door display
        final_doors = ["🚪"] * 3
        final_doors[monty_opens] = "🐐"
        final_doors[final_choice] = "🚗" if prize == 'car' else "🐐"
        st.markdown("<p style='font-size:28px;'>" + "  ".join(final_doors) + "</p>", unsafe_allow_html=True)

        # Final message
        if trade:
            st.markdown(f"<p style='font-size:20px;'>You switched to <strong>Door {final_choice + 1}</strong>.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-size:20px;'>You stayed with your original choice.</p>", unsafe_allow_html=True)

        st.markdown(f"<p style='font-size:20px;'>Behind Door {final_choice + 1} was a <strong>{prize.upper()}</strong>.</p>", unsafe_allow_html=True)

        if prize == 'car':
            st.success("🎉 You WON the car!")
        else:
            st.error("😢 You got a goat.")
