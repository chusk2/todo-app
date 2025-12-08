from datetime import datetime
import streamlit as st

# Initialize debug mode toggle state
if 'debug_mode' not in st.session_state:
    st.session_state['debug_mode'] = False

# Initialize a list in session state to store debug messages
if 'debug_messages' not in st.session_state:
    st.session_state['debug_messages'] = []

### function to generate a debug message with current timestamp
def add_debug_message(message):
    if st.session_state.debug_mode:
        st.session_state['debug_messages'] \
        .append(f"{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')} - {message}")

def show_debug_messages():
    # Debugging messages expander
    if st.session_state.debug_mode:
        with st.expander("Debug Messages"):
            for msg in st.session_state['debug_messages']:
                st.info(msg)
            st.session_state['debug_messages'] = [] # Clear messages after displaying