import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from database import get_customer_info
from support_agent import get_agent_response

# Load environment variables for local development
load_dotenv()

st.set_page_config(
    page_title="AI Customer Support Agent", page_icon="🤖", layout="wide"
)

st.title("🤖 AI Customer Support Agent")
st.caption("Powered by Groq (`openai/gpt-oss-120b`) & Streamlit")

# Sidebar - Customer Authentication / Lookup
st.sidebar.header("🔑 Customer Verification")
customer_id = st.sidebar.text_input(
    "Enter Customer ID", value="CUST-1001", help="Try CUST-1001 or CUST-1002"
)

customer_data = get_customer_info(customer_id) if customer_id else None

if customer_data:
    st.sidebar.success(f"Verified: {customer_data['name']}")

    # Display Customer Info in Sidebar
    with st.sidebar.expander("👤 Profile & Address Details", expanded=True):
        st.write(f"**Name:** {customer_data['name']}")
        st.write(f"**Email:** {customer_data['email']}")
        st.write(f"**Phone:** {customer_data['phone']}")
        st.write(f"**Shipping Address:** {customer_data['address']}")

    # Main Area Layout
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📦 Order History & Data")
        orders_df = pd.DataFrame(customer_data["orders"])
        st.dataframe(orders_df, use_container_width=True)

        st.info(
            "💡 You can ask the AI agent about order status, delivery dates, or address details."
        )

    with col2:
        st.subheader("💬 Support Chatbot")

        # Session state for chat history tied to current customer
        session_key = f"messages_{customer_id}"
        if session_key not in st.session_state:
            st.session_state[session_key] = [
                {
                    "role": "assistant",
                    "content": f"Hello {customer_data['name']}! How can I assist you with your orders or account today?",
                }
            ]

        # Display Chat History
        for msg in st.session_state[session_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # User Input
        if user_prompt := st.chat_input(
            "Type your query (e.g., 'Where is my order ORD-9921?')..."
        ):
            # Display user message
            st.session_state[session_key].append(
                {"role": "user", "content": user_prompt}
            )
            with st.chat_message("user"):
                st.markdown(user_prompt)

            # Generate Agent Response
            with st.chat_message("assistant"):
                with st.spinner("AI Agent is checking details..."):
                    response = get_agent_response(
                        customer_id,
                        customer_data,
                        st.session_state[session_key],
                    )
                    st.markdown(response)

            st.session_state[session_key].append(
                {"role": "assistant", "content": response}
            )

else:
    st.warning(
        "Please enter a valid Customer ID in the sidebar to load customer details and start support chat."
    )
    st.markdown("""
    **Available Demo Customer IDs:**
    - `CUST-1001`
    - `CUST-1002`
    """)
