import streamlit as st
from streamlit_option_menu import option_menu
from langchain_core.messages import HumanMessage, AIMessage

# -- Setup Page Configuration --
st.set_page_config(
    page_title="The AI Ethics Educator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- Styling --
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
    color: #212529;
    font-family: 'Georgia', serif;
}
h1, h2, h3 {
    color: #0b3d91;
}
.footer {
    background-color: #f1f1f1;
    color: #333;
    text-align: center;
    padding: 15px;
    font-size: 14px;
    border-top: 1px solid #ccc;
    margin-top: 50px;
    border-radius: 5px;
}
.disclaimer {
    font-size: 12px;
    color: #d9534f;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -- Helper Functions --
@st.cache_resource(show_spinner=False)
def init_llm(provider, api_key):
    if not api_key:
        return None
    try:
        if provider == "OpenAI":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(api_key=api_key, model="gpt-4o-mini")
        elif provider == "Gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-1.5-flash")
        elif provider == "Claude":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(api_key=api_key, model="claude-3-haiku-20240307")
        elif provider == "Groq":
            from langchain_groq import ChatGroq
            return ChatGroq(api_key=api_key, model="llama-3.1-8b-instant")
    except Exception as e:
        st.sidebar.error(f"Error initializing {provider}: {e}")
        return None
    return None

def chat_interface(llm):
    st.markdown("### 💬 Chat with an Ethics Expert")
    if not llm:
        st.info("Please enter a valid API key in the sidebar to activate the AI tutor.")
        return
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I am your AI Ethics Tutor. Ask me any questions about AI governance, ethics frameworks, or philosophical foundations.")
        ]
        
    for i, msg in enumerate(st.session_state.chat_history):
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(msg.content)
            
    if prompt := st.chat_input("Ask a question regarding AI Ethics..."):
        # Append and immediately display user message
        st.session_state.chat_history.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.write(prompt)
            
        # Display assistant response placeholder
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = llm.invoke(st.session_state.chat_history)
                    msg_content = response.content
                    st.write(msg_content)
                    st.session_state.chat_history.append(AIMessage(content=msg_content))
                except Exception as e:
                    st.error(f"OpenAI API Error: {e}")
                    # Remove the failed message from history so they can retry
                    st.session_state.chat_history.pop()

# -- Sidebar --
with st.sidebar:
    st.markdown("## 🔑 LLM Configuration")
    provider = st.selectbox("Select Model Provider", ["OpenAI", "Gemini", "Claude", "Groq"])
    api_key = st.text_input("Enter API Key", type="password")
    
    llm = init_llm(provider, api_key)
    
    if llm:
        st.success(f"✅ Context initialized for {provider}!")
        if st.button("Test Connection"):
            with st.spinner("Pinging API..."):
                try:
                    llm.invoke("Respond with 'Connection successful'.")
                    st.success("Network check passed! Connection is stable.")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

    st.markdown("---")
    
    st.markdown("## Navigation")
    selected = option_menu(
        "", 
        [
            "1. Intro to AI Ethics", 
            "2. Theoretical Foundations", 
            "3. Frameworks & Acts", 
            "4. Failures & Consequences", 
            "5. Organizational Governance", 
            "6. Interactive Quiz", 
            "7. References"
        ],
        icons=['play', 'book', 'file-text', 'exclamation-triangle', 'building', 'question-circle', 'list'],
        default_index=0,
        styles={
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"},
            "nav-link-selected": {"background-color": "#0b3d91"},
        }
    )

# -- Page Layout & Modules --
st.title("The AI Ethics Educator")
st.markdown("*A comprehensively structured course on AI Ethics and Governance.*")
st.markdown("---")

if selected == "1. Intro to AI Ethics":
    st.header("1. Introduction to AI Ethics")
    with st.container():
        st.write("""
        ### What is AI Ethics?
        AI ethics refers to a broad collection of considerations for responsible AI that combines safety, security, human concerns, and environmental considerations. It dictates that the technology must be developed and used in ways that are equitable, fair, transparent, and accountable.
        
        ### Why is Ethics Foundational?
        Artificial Intelligence is not merely a technical tool; it shapes human behavior, influences decision-making in critical areas (such as justice, healthcare, and hiring), and operates at an unprecedented scale. Without a bedrock of ethical reasoning, AI systems risk scaling societal inequities, causing unintended harm, and lacking the necessary accountability when things go wrong.
        """)
        
        with st.expander("Explore the core motivations for ethical AI"):
            st.write("""
            - **Trust and Adoption:** Society will not adopt AI systems blindly unless they are verifiable and act in human interest.
            - **Preventing Bias:** Datasets contain historical biases. Ethics drives the algorithms that attempt to decouple these ingrained biases.
            - **Alignment Problem:** Ensuring that an AI system's objectives align with human values is a defining challenge of our era.
            """)
            
    st.markdown("---")
    chat_interface(llm)

elif selected == "2. Theoretical Foundations":
    st.header("2. Theoretical Foundations")
    st.write("Understand the philosophical underpinnings of ethical decision-making in AI.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Deontology")
        st.write("Rules-based ethics. The morality of an action is based on whether that action itself is right or wrong under a series of rules, rather than based on the consequences of the action.")
        with st.expander("Application to AI"):
            st.write("An autonomous vehicle programmed not to kill a human under *any* circumstances, following a strict absolute rule, even if it means sacrificing multiple other assets.")
            
    with col2:
        st.subheader("Consequentialism")
        st.write("Outcomes-based ethics (Utilitarianism). The morally right action is the one that produces the best overall consequences, often defined as the greatest good for the greatest number.")
        with st.expander("Application to AI"):
            st.write("A medical triage AI that allocates scarce resources to patients who have the highest probability of survival, maximizing the total lives saved but potentially ignoring individual fairness.")
            
    with col3:
        st.subheader("Virtue Ethics")
        st.write("Character-based ethics. Focuses on the virtues, or moral character, of the person carrying out an action.")
        with st.expander("Application to AI"):
            st.write("Emphasizes the moral character of the developers. Are the software engineers and corporations creating the AI practicing transparency, prudence, and honesty?")

    st.markdown("---")
    chat_interface(llm)

elif selected == "3. Frameworks & Acts":
    st.header("3. Regulatory Frameworks & Acts")
    st.write("A look at global standards governing artificial intelligence.")
    
    with st.expander("📘 NIST AI Risk Management Framework (RMF)", expanded=True):
        st.write("""
        Developed by the US National Institute of Standards and Technology, the AI RMF provides guidelines to proactively manage AI risks and promote trustworthy AI.
        - **Govern:** Creating a culture of risk management.
        - **Map:** Understanding context and identifying risks.
        - **Measure:** Assessing, analyzing, and tracking identified risks.
        - **Manage:** Prioritizing and acting upon prioritized risks.
        """)
        
    with st.expander("🌍 OECD AI Principles"):
        st.write("""
        The first intergovernmental standard on AI, adopted in 2019. It promotes AI that is innovative and trustworthy, and that respects human rights and democratic values.
        - Inclusive growth, sustainable development, and well-being.
        - Human-centered values and fairness.
        - Transparency and explainability.
        - Robustness, security, and safety.
        - Accountability.
        """)
        
    with st.expander("⚖️ The EU AI Act"):
        st.write("""
        A landmark regulatory framework proposing a **risk-based approach** to AI:
        - **Unacceptable Risk:** Systems that manipulate human behavior or use social scoring (Banned).
        - **High Risk:** Systems in critical infrastructure, education, or law enforcement (Strict compliance required).
        - **Limited Risk:** Chatbots and deepfakes (Requires transparency and labeling).
        - **Minimal Risk:** Spam filters and video games (Unregulated).
        """)

    st.markdown("---")
    chat_interface(llm)

elif selected == "4. Failures & Consequences":
    st.header("4. Failures & Consequences")
    st.write("Real-world examples illustrating the critical need for AI ethics.")
    
    with st.container():
        st.markdown("### Bias in Hiring")
        st.write("A notable tech company had to scrap its AI recruiting tool after it was discovered to be biased against women. The AI was trained on resumes submitted over a 10-year period, most of which came from men.")
        
        st.markdown("### Healthcare Triage Inequalities")
        st.write("An algorithm widely used in US hospitals to allocate health care to patients was found to systematically discriminate against Black people, demonstrating how historic disparities are coded into 'neutral' data.")
        
        st.markdown("### Facial Recognition False Arrests")
        st.write("Several instances have surfaced where individuals were falsely accused of crimes due to erroneous facial recognition matchings, heavily disproportionate against people of color.")
        
    st.markdown("---")
    chat_interface(llm)

elif selected == "5. Organizational Governance":
    st.header("5. Organizational Governance & Safety")
    st.write("How organizations implement ethical guidelines internally, focusing on human flourishing and safety research.")
    
    st.markdown("### The FATES Framework")
    st.write("- **Fairness:** Preventing algorithmic bias and ensuring equitable treatment.")
    st.write("- **Accountability:** Establishing clear lines of responsibility for AI outcomes.")
    st.write("- **Transparency:** Understanding how an AI system arrives at its outputs.")
    st.write("- **Ethics:** Aligning with moral principles and human rights.")
    st.write("- **Sustainability:** Considering the environmental impact of training massive models.")
    
    st.markdown("### Advanced Principles")
    with st.expander("Harm Avoidance, Beneficence, and Safety"):
        st.write("""
        **Harm Avoidance:** Systems must systematically mitigate foreseeable risks.
        
        **Beneficence:** AI systems must do good and provide societal value.
        
        **Safety & Human Flourishing:** As models approach AGI (Artificial General Intelligence) and exhibit agentic behaviors, hard coding safety guardrails becomes an existential imperative.
        """)
        
    st.markdown("---")
    st.markdown("### 🎥 Deep Dive: The Risks of Agentic AI")
    st.write("Listen to Yoshua Bengio, one of the founders of deep learning, discuss why advanced AI presents catastrophic risks, examining the shift from tool AI to 'Agent' AI.")
    
    # Embed the requested video
    st.video("https://www.youtube.com/watch?v=qe9QSCF-d88")
    
    with st.expander("Video Context & Key Takeaways"):
        st.write("""
        - **Increasing Agency [06:27]:** The profound shift from AI as a passive tool to AI as an *agent* that has the capacity to plan, act, and execute objectives autonomously.
        - **Deceptive Behavior [07:03]:** Evidence suggesting that highly capable systems can learn to subvert their safety constraints, potentially using deception to achieve their reward goals.
        - **Scientific Solutions [10:44]:** The necessity of the "Scientist AI"—a completely non-agentic AI focused exclusively on safety research and hypothesis testing to safeguard human flourishing.
        """)

    st.markdown("---")
    chat_interface(llm)

elif selected == "6. Interactive Quiz":
    st.header("6. Interactive Knowledge Check")
    
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    questions = [
        {
            "prompt": "1. Which moral philosophy dictates that the morality of an action is based solely on adherence to absolute rules?",
            "options": ["Utilitarianism", "Virtue Ethics", "Deontology", "Nihilism"],
            "answer": "Deontology",
            "explanation": "Deontology evaluates the moral correctness of an action based on rules, independent of the consequences."
        },
        {
            "prompt": "2. Under the EU AI Act, what category would a widely used chatbot fall under?",
            "options": ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"],
            "answer": "Limited Risk",
            "explanation": "Chatbots present a limited risk and primarily require transparency obligations (notifying users they are talking to a bot)."
        },
        {
            "prompt": "3. The 'T' in the FATES framework stands for:",
            "options": ["Technology", "Transparency", "Testing", "Truthfulness"],
            "answer": "Transparency",
            "explanation": "Transparency ensures that stakeholders understand how a model makes its decisions."
        },
        {
            "prompt": "4. Which framework provides proactive guidelines like Govern, Map, Measure, and Manage to handle AI risks?",
            "options": ["EU AI Act", "NIST AI RMF", "OECD AI Principles", "FATES"],
            "answer": "NIST AI RMF",
            "explanation": "The NIST AI Risk Management Framework provides core functions: Govern, Map, Measure, and Manage to help organizations foster trustworthy AI."
        },
        {
            "prompt": "5. What does the 'Alignment Problem' refer to in AI ethics?",
            "options": ["Formatting model output", "Ensuring AI goals match human values", "Aligning data with databases", "Aligning policies across countries"],
            "answer": "Ensuring AI goals match human values",
            "explanation": "The Alignment Problem refers to the challenge of building AI systems whose objectives properly align with complex human values."
        },
        {
            "prompt": "6. Under which ethical framework is the focus placed on the moral character of the AI developer?",
            "options": ["Deontology", "Consequentialism", "Virtue Ethics", "Utilitarianism"],
            "answer": "Virtue Ethics",
            "explanation": "Virtue Ethics focuses on the person carrying out an action and their traits, such as prudence or honesty, rather than rules or outcomes."
        },
        {
            "prompt": "7. In Yoshua Bengio's discussion on AI risks, what describes the shift from passive AI systems to autonomous goal-seeking ones?",
            "options": ["Increasing Transparency", "Decreasing Safety", "Increasing Agency", "Deceptive Behavior"],
            "answer": "Increasing Agency",
            "explanation": "Increasing Agency is the profound shift where AI morphs from a passive tool into an agent that plans and acts autonomously."
        },
        {
            "prompt": "8. What is the proposed 'Scientist AI' concept designed to solve?",
            "options": ["Speed up commercial AI", "Act entirely autonomously", "Improve mathematical calculations", "Focus explicitly on safety research without acting as a free agent"],
            "answer": "Focus explicitly on safety research without acting as a free agent",
            "explanation": "A 'Scientist AI' is conceptualized as a highly capable but non-agentic system strictly bounded to hypothesis testing and safety research."
        },
        {
            "prompt": "9. Which principle emphasizes ensuring that an AI system provides societal value and actively does good?",
            "options": ["Beneficence", "Transparency", "Accountability", "Sustainability"],
            "answer": "Beneficence",
            "explanation": "Beneficence is the moral obligation to act for the benefit of others, maximizing societal value while minimizing harm."
        },
        {
            "prompt": "10. In the context of AI failures, historical biases found in hiring models are typically a result of:",
            "options": ["Too many developers", "Flawed historical training data", "Overfitting on small datasets", "Fast processors"],
            "answer": "Flawed historical training data",
            "explanation": "AI systems learn from the data they are trained on; if historical data reflects human biases (e.g., favoring male applicants), the AI will replicate and scale those biases."
        }
    ]
    
    with st.form("quiz_form"):
        user_answers = []
        for q in questions:
            st.markdown(f"**{q['prompt']}**")
            ans = st.radio("Select an answer:", q["options"], key=q["prompt"], index=None)
            user_answers.append(ans)
            st.markdown("---")
            
        submitted = st.form_submit_button("Submit Answers")
        
        if submitted:
            st.session_state.quiz_submitted = True
            st.session_state.user_answers = user_answers
            
    if st.session_state.quiz_submitted:
        st.subheader("Quiz Results")
        score = 0
        for i, q in enumerate(questions):
            u_ans = st.session_state.user_answers[i]
            if u_ans == q["answer"]:
                st.success(f"**Question {i+1}: Correct!**")
                score += 1
            else:
                st.error(f"**Question {i+1}: Incorrect. Your answer: {u_ans}. Correct answer: {q['answer']}**")
            st.info(f"Pedagogical Explanation: {q['explanation']}")
            
        st.metric(label="Your Score", value=f"{score}/{len(questions)}")

elif selected == "7. References":
    st.header("7. References & Further Reading")
    st.write("""
    1. National Institute of Standards and Technology (NIST). *AI Risk Management Framework (AI RMF 1.0)*. 2023.
    2. Organisation for Economic Co-operation and Development (OECD). *OECD AI Principles*. 2019.
    3. European Commission. *The AI Act*. 2021/2024.
    4. Bengio, Yoshua. "The Catastrophic Risks of AI — and a Safer Path." *TED*, 2024. [YouTube Video](https://www.youtube.com/watch?v=qe9QSCF-d88).
    5. Birhane, Abeba. "Algorithmic Injustice: A Relational Ethics Approach." *Patterns*, 2021.
    6. Jobin, A., Ienca, M., & Vayena, E. "The global landscape of AI ethics guidelines." *Nature Machine Intelligence*, 2019.
    """)
    
    st.markdown("---")
    chat_interface(llm)

# -- Footer Credits & Disclaimers --
st.markdown("""
<div class="footer">
    <p>Developed by Sridhar Nerur with help from Antigravity.</p>
    <p><i>This application is for educational purposes only.</i></p>
    <p class="disclaimer">Note: Large Language Models can make mistakes or hallucinate. Please cross-reference information with official documentation.</p>
</div>
""", unsafe_allow_html=True)
