import streamlit as st
from google import genai
from google.genai import errors

# पेज के सेटअप
st.set_page_config(page_title="हमर AI", page_icon="🤖")
st.title("🤖 हमर पर्सनल AI चैटबॉट")

# एपीआई की (API Key) इनपुट
api_key = st.secrets.get("GEMINI_API_KEY")

# चैट हिस्ट्री खातिर मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरान मैसेज स्क्रीन पर देखावे खातिर
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# यूज़र इनपुट बॉक्स
user_prompt = st.chat_input("कुछू पूछीं...")

if user_prompt:
# यूज़र के सवाल स्क्रीन पर देखावे खातिर
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        # AI से जवाब लेवे खातिर (कबहूँ ना रुके वाला सेफ ब्लॉक)
        with st.chat_message("assistant"):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                )
                bot_reply = response.text
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except errors.APIError as e:
                st.error("API सीमा भा नेटवर्क एरर आइल बा, कुछ देर बाद दोबारा कोशिश करीं।")
            except Exception as e:
                st.error(f"कवनो अनजान समस्या आइल: {e}")
