import streamlit as st
import requests
import os
from typing import Optional

# Get backend URL from environment variable
BACKEND_URL = os.getenv('BACKEND_URL', 'https://newsletter-backend-162421115459.us-central1.run.app')

class NewsletterGenUI:
    def generate_newsletter(self, topic: str, personal_message: str) -> Optional[str]:
        """Send request to backend service to generate newsletter"""
        try:
            response = requests.post(
                f"{BACKEND_URL}/generate",
                json={
                    "topic": topic,
                    "personal_message": personal_message
                },
                headers={"Content-Type": "application/json"},
                timeout=300  # 5-minute timeout for long-running generations
            )
            
            if response.status_code == 200:
                return response.json().get("result")
            else:
                error_message = response.json().get('error', 'Unknown error occurred')
                st.error(f"Error: {error_message}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend service: {str(e)}")
            return None

    def check_backend_health(self) -> bool:
        """Check if backend service is healthy"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def newsletter_generation(self):
        if st.session_state.generating:
            with st.spinner("Generating newsletter... This may take a few minutes."):
                st.session_state.newsletter = self.generate_newsletter(
                    st.session_state.topic, st.session_state.personal_message
                )

        if st.session_state.newsletter and st.session_state.newsletter != "":
            with st.container():
                st.success("Newsletter generated successfully!")
                st.download_button(
                    label="Download HTML file",
                    data=st.session_state.newsletter,
                    file_name="newsletter.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("Newsletter Generator")

            # Add backend status indicator
            backend_status = self.check_backend_health()
            status_container = st.empty()
            if backend_status:
                status_container.success("Backend service is connected")
            else:
                status_container.error("Backend service is unavailable")

            st.write(
                """
                To generate a newsletter, enter a topic and a personal message. \n
                Your team of AI agents will generate a newsletter for you!
                """
            )

            st.text_input("Topic", key="topic", placeholder="USA Stock Market")

            st.text_area(
                "Your personal message (to include at the top of the newsletter)",
                key="personal_message",
                placeholder="Dear readers, welcome to the newsletter!",
            )

            generate_button = st.button(
                "Generate Newsletter",
                disabled=not backend_status
            )
            
            if generate_button:
                if not st.session_state.topic or not st.session_state.personal_message:
                    st.warning("Please fill in both the topic and personal message fields.")
                else:
                    st.session_state.generating = True

    def render(self):
        st.set_page_config(
            page_title="Newsletter Generation",
            page_icon="📧",
            layout="wide"
        )

        # Initialize session state variables
        for key in ["topic", "personal_message", "newsletter", "generating"]:
            if key not in st.session_state:
                st.session_state[key] = "" if key != "generating" else False

        self.sidebar()
        self.newsletter_generation()


if __name__ == "__main__":
    NewsletterGenUI().render()