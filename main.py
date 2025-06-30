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
<div style='font-size:24px'>
<ul>
<li>You are in a game show. The host gives you the choice of <strong>three doors</strong>.</li>
<li>Behind <strong>one</strong> door is a brand-new <strong>car</strong>, behind the others are <strong>goats</strong>.</li>
<li>You pick a door.</li>
<li>The host (who knows what's behind each door) opens <strong>another</strong> door, revealing a <strong>goat</strong>.</li>
<li>The host then asks you: <em>Do you want to switch?</em></li>
</ul>
</div>
""", unsafe_allow_html=True)


if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    if st.button("🎮 Start Game 🎮"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# -------------------------------
# Game Simulation
# -------------------------------
st.header("Monty Hall Problem Simulation")
st.markdown("<p style='font-size:24px;'>Pick a door:</p>", unsafe_allow_html=True)
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
    st.markdown(f"<p style='font-size:24px;'>You picked <strong>Door {choice + 1}</strong>.</p>", unsafe_allow_html=True)
    
    st.markdown(f"<p style='font-size:24px;'>The host opened <strong>Door {monty_opens + 1}</strong>, revealing a 🐐.</p>", unsafe_allow_html=True)

    # Display current door state with Monty’s door revealed
    door_display = ["🚪"] * 3
    door_display[monty_opens] = "🐐"
    st.markdown("<p style='font-size:40px;'>" + "  ".join(door_display) + "</p>", unsafe_allow_html=True)

    trade = st.radio("Do you want to switch your choice?", ["Yes", "No"]) == "Yes"

    if st.button("Final Choice"):
        if trade:
            final_choice = [i for i in range(3) if i != choice and i != monty_opens][0]
        else:
            final_choice = choice

        prize = doors[final_choice]

        st.markdown("<p style='font-size:24px;'>Revealing your door...</p>", unsafe_allow_html=True)
        time.sleep(.9)

        # Update door display
        final_doors = ["🚪"] * 3
        final_doors[monty_opens] = "🐐"
        final_doors[final_choice] = "🚗" if prize == 'car' else "🐐"
        st.markdown("<p style='font-size:40px;'>" + "  ".join(final_doors) + "</p>", unsafe_allow_html=True)

        # Final message
        if trade:
            st.markdown(f"<p style='font-size:24px;'>You switched to <strong>Door {final_choice + 1}</strong>.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='font-size:24px;'>You stayed with your original choice.</p>", unsafe_allow_html=True)

        st.markdown(f"<p style='font-size:24px;'>Behind Door {final_choice + 1} was a <strong>{prize.upper()}</strong>.</p>", unsafe_allow_html=True)

        if prize == 'car':
            st.success("🎉🎉🎉 You WON the car! 🎉🎉🎉")
            if trade:
                st.markdown("<p style='font-size:24px;'>Congratulations, switching paid off — that’s the best strategy!</p>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<p style='font-size:24px;'>Congratulations — but just know you were lucky. "
                    "You didn’t switch, but still got the car. That was not the best strategy, even if it worked this time.</p>",
                    unsafe_allow_html=True
                )
        else:
            st.error("😢 You got a goat. 😢")
            if trade:
                st.markdown("<p style='font-size:24px;'>Don’t feel bad — switching is still the better strategy!!! </p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:24px;'>Sorry! If you had switched, you'd have had a better chance.</p>", unsafe_allow_html=True)

        # 💡 Follow-up with blog link
        st.markdown(
            """
            <hr>
            <p style='font-size:24px;'> For a detailed explanation of why switching is definitely the best strategy (and also how I made this game) check out my 
            <a href='https://github.com/PessoaP/blog/blob/master/3doors/3doors.ipynb' target='_blank'>blog post</a>.</p>
            """,
            unsafe_allow_html=True
        )
