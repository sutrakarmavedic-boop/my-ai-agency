import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- APP UI SETUP ---
st.set_page_config(page_title="AI Business Empire", layout="wide")
st.title("🚀 My 8-Employee AI Business App")
st.markdown("### CEO Dashboard: Marketing -> Approval -> Sales")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_key = st.text_input("Enter Groq API Key:", type="password", value="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")
    st.info("Your 8 Employees are Online 🟢")
    
    # कर्मचारी लिस्ट (Status)
    st.subheader("👥 Departments")
    st.write("- CEO Agent")
    st.write("- Marketing Dept")
    st.write("- Sales Dept")
    st.write("- HR, Finance, Dev")
    st.write("- Ops & Content")

# --- APP LOGIC ---
if groq_key:
    os.environ["OPENAI_API_KEY"] = groq_key
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    os.environ["OPENAI_MODEL_NAME"] = "llama-3.3-70b-versatile"

    # LLM Setup
    llm = ChatOpenAI(
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=groq_key,
        model_name="llama-3.3-70b-versatile"
    )

    # --- 1. AGENTS ---
    ceo = Agent(role='CEO', goal='Strategy & Approval', backstory='Business Lead', llm=llm)
    marketing = Agent(role='Marketing', goal='Viral Reels Research', backstory='Trends Expert', llm=llm)
    sales = Agent(role='Sales', goal='Lead Gen & Outreach', backstory='Conversion Expert', llm=llm)
    # बाकी एम्पलाइज बैकग्राउंड सपोर्ट के तौर पर
    ops = Agent(role='Operations', goal='Workflow Smoothness', backstory='Process Expert', llm=llm)

    # --- INPUT AREA ---
    topic = st.text_input("What is your Business Topic or Instagram Link?", placeholder="e.g. AI Automation Agency for Real Estate")

    if st.button("Start Marketing Phase"):
        if topic:
            with st.status("Marketing Specialist is analyzing Reels...", expanded=True) as status:
                # Task 1: Marketing
                t1 = Task(description=f"Analyze Instagram trends for: {topic}. Give 3 viral ideas.", expected_output="3 Viral Ideas.", agent=marketing)
                crew = Crew(agents=[marketing], tasks=[t1], verbose=True)
                marketing_result = crew.kickoff()
                
                st.session_state['marketing_output'] = marketing_result
                status.update(label="Marketing Phase Complete!", state="complete")
        else:
            st.warning("Please enter a topic first!")

    # --- 2. APPROVAL PHASE ---
    if 'marketing_output' in st.session_state:
        st.subheader("📬 Pending Approval: Marketing Ideas")
        st.info(st.session_state['marketing_output'])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve & Send to Sales"):
                with st.status("Sales Lead is drafting outreach emails...", expanded=True) as status:
                    # Task: Sales
                    t2 = Task(description=f"Draft outreach email based on: {st.session_state['marketing_output']}", expected_output="Final Email Draft.", agent=sales)
                    crew_sales = Crew(agents=[sales], tasks=[t2], verbose=True)
                    sales_result = crew_sales.kickoff()
                    
                    st.session_state['sales_output'] = sales_result
                    status.update(label="Sales Outreach Ready!", state="complete")
        with col2:
            if st.button("❌ Reject Ideas"):
                del st.session_state['marketing_output']
                st.experimental_rerun()

    # --- 3. FINAL OUTPUT ---
    if 'sales_output' in st.session_state:
        st.subheader("📧 Final Sales Outreach Email")
        st.success("The email is ready to be sent to your leads!")
        st.text_area("Copy your Email:", value=st.session_state['sales_output'], height=300)
        
        if st.button("Reset App"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
else:
    st.error("Please enter your API Key in the sidebar to start.")