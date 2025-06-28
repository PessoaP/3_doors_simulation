import time

elif st.session_state.phase == "switch":
    st.subheader("🎬 Game Summary")
    choice = st.session_state.choice
    monty_opens = st.session_state.monty_opens
    doors = st.session_state.doors

    st.write(f"You picked **Door {choice + 1}**.")
    st.write(f"The host opened **Door {monty_opens + 1}**, revealing a goat.")

    # Show door states before reveal
    door_display = ["🚪"] * 3
    door_display[monty_opens] = "🐐"
    st.write(" ".join(door_display))

    trade = st.radio("Do you want to switch your choice?", ["Yes", "No"]) == "Yes"

    if st.button("Final Choice"):
        if trade:
            final_choice = [i for i in range(3)
                            if i != choice and i != monty_opens][0]
        else:
            final_choice = choice

        prize = doors[final_choice]

        # Animate reveal
        st.write("Revealing your door...")
        time.sleep(.5)

        # Final display
        final_doors = ["🚪"] * 3
        final_doors[monty_opens] = "🐐"
        final_doors[final_choice] = "🚗" if prize == 'car' else "🐐"
        st.write(" ".join(final_doors))

        if trade:
            st.write(f"You switched to **Door {final_choice + 1}**.")
        else:
            st.write(f"You stayed with your original choice.")

        st.write(f"Behind Door {final_choice + 1} was a **{prize.upper()}**.")

        if prize == 'car':
            st.success("🎉 You WON the car!")
        else:
            st.error("😢 You got a goat.")

        if st.button("🔁 Play Again"):
            st.session_state.phase = "pick"
            st.session_state.doors = None
            st.session_state.choice = None
            st.session_state.monty_opens = None
            st.rerun()
