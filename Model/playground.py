import streamlit as st

# Use session state to control the display
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# Check if the button has been clicked
if st.session_state.button_clicked:
    # After the button is clicked, display only "Hello World"
    st.write("Hello World")
else:
    # Display the button
    if st.button("Click me"):
        st.session_state.button_clicked = True
        # Re-render immediately by forcing a page refresh or moving all other code within the else block
        st.rerun()  # or leave it to Streamlit to handle rerun naturally
