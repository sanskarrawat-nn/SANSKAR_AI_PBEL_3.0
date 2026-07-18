import streamlit as st
import requests
import re
import os

# 1. PAGE SETUP & CONFIG
st.set_page_config(
    page_title="NEURAL LEARN | Deep progression lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_URL = "http://localhost:8000"

# Helper to extract YouTube video ID and start timestamp for embed URLs
def get_youtube_embed_url(url: str) -> str:
    # Extract 11-character video ID
    video_id_match = re.search(r'(?:v=|be/|embed/|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    if not video_id_match:
        return "https://www.youtube.com/embed/"
        
    video_id = video_id_match.group(1)
    
    # Extract timestamp start time (in seconds)
    t_match = re.search(r'(?:\?|&)(?:t|start)=(\d+)', url)
    start_time = t_match.group(1) if t_match else None
    
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    if start_time:
        embed_url += f"?start={start_time}"
    return embed_url

# Styling Injection for IBM Carbon inspired modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;800&display=swap');
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title banner gradient */
    .title-banner {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: radial-gradient(circle at top, rgba(30, 58, 138, 0.4) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
    }
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #6366f1 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Custom Card */
    .custom-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Code box styling */
    .code-box {
        background-color: #030712;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', Courier, monospace;
        color: #38bdf8;
        font-size: 1rem;
        margin: 1rem 0;
    }
    
    /* Custom badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    .badge-beginner {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-intermediate {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-advanced {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-cs {
        background-color: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    /* Module Node states */
    .node-container {
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .node-completed {
        background: rgba(6, 78, 59, 0.25);
        border: 2px solid #059669;
        box-shadow: 0 0 15px rgba(5, 150, 105, 0.15);
    }
    .node-active {
        background: rgba(30, 58, 138, 0.3);
        border: 2px solid #2563eb;
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.3);
        animation: pulse 2.0s infinite alternate;
    }
    .node-locked {
        background: rgba(31, 41, 55, 0.4);
        border: 2px dashed #4b5563;
        opacity: 0.6;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 10px rgba(37, 99, 235, 0.2); }
        100% { box-shadow: 0 0 25px rgba(37, 99, 235, 0.5); }
    }
</style>
""", unsafe_allow_html=True)

# Helper function to fetch from API safely
def get_api(path):
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=4)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"⚠️ API Error ({r.status_code}): {r.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Backend Connection Offline: Please make sure the FastAPI server is running on port 8000.")
        return None

# 2. STATE INITIALIZATION
if "selected_course_id" not in st.session_state:
    st.session_state.selected_course_id = "1"
if "active_module_id" not in st.session_state:
    st.session_state.active_module_id = None
if "verification_status" not in st.session_state:
    st.session_state.verification_status = None
if "verification_message" not in st.session_state:
    st.session_state.verification_message = ""
if "trigger_balloons" not in st.session_state:
    st.session_state.trigger_balloons = False

# Run balloons if flag set
if st.session_state.trigger_balloons:
    st.balloons()
    st.session_state.trigger_balloons = False

# Sidebar logo and info
st.sidebar.markdown("<h2 style='text-align: center; color: #38bdf8; font-family: Outfit;'>🧠 IBM Skill Tree</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Fetch Courses
courses = get_api("/api/v1/courses")

if courses:
    course_titles = {c["Course_ID"]: f"{c['Title']} ({c['Difficulty']})" for c in courses}
    course_list = list(course_titles.keys())
    
    # Sidebar Course Selection
    selected_cid = st.sidebar.radio(
        "Select Learning Track:",
        course_list,
        format_func=lambda x: course_titles[x],
        index=course_list.index(st.session_state.selected_course_id) if st.session_state.selected_course_id in course_list else 0
    )
    
    if selected_cid != st.session_state.selected_course_id:
        st.session_state.selected_course_id = selected_cid
        st.session_state.active_module_id = None
        st.session_state.verification_status = None
        st.session_state.verification_message = ""
        st.rerun()
else:
    st.stop()

# Load specific course details
course_data = get_api(f"/api/v1/course/{st.session_state.selected_course_id}")

if not course_data:
    st.stop()

# Reset progression handler
def handle_reset():
    try:
        res = requests.post(f"{BASE_URL}/api/v1/progress/reset", timeout=4)
        if res.status_code == 200:
            st.session_state.active_module_id = None
            st.session_state.verification_status = None
            st.session_state.verification_message = ""
            st.toast("🔄 Progression reset back to Module 1!", icon="🔄")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Connection Error: Failed to reset progression.")

st.sidebar.markdown("---")
st.sidebar.button("🔄 Reset All Progression", on_click=handle_reset, use_container_width=True)
st.sidebar.markdown(
    """
    <div style="background-color: rgba(30, 41, 59, 0.4); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; color: #94a3b8; margin-top: 1rem;">
        <strong>How to Progress:</strong><br>
        1. Click on unlocked (colored) modules in the Skill Tree.<br>
        2. Watch the video tutorial.<br>
        3. Solve the coding puzzle at the bottom.<br>
        4. Submit a correct answer to unlock the next level!
    </div>
    """,
    unsafe_allow_html=True
)

# Header Banner
difficulty_class = f"badge-{course_data['Difficulty'].lower()}"
st.markdown(
    f"""
    <div class="title-banner">
        <div class="main-title">IBM Learning & Skill Labs</div>
        <div class="sub-title">Interactive progression map based on structural skill trees</div>
        <div style="margin-top: 1rem;">
            <span class="badge {difficulty_class}">{course_data['Difficulty']}</span>
            <span class="badge badge-cs">{course_data['Category']}</span>
            <span style="color: #fbbf24; font-weight: 600; font-size: 0.95rem;">★ {course_data['Avg_Rating']} Rating</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Render course description title
st.markdown(f"## 🗺️ Skill Tree Map: *{course_data['Title']}*")

# Find module states
modules = course_data.get("modules", [])

# Determine natural default active module if none selected
if st.session_state.active_module_id is None:
    # Default to the first unlocked, uncompleted module, or the last module if all completed
    unlocked_modules = [m for m in modules if not m["is_locked"]]
    if unlocked_modules:
        st.session_state.active_module_id = unlocked_modules[-1]["Module_ID"] # Highest unlocked module
    elif modules:
        st.session_state.active_module_id = modules[0]["Module_ID"]

# Render the modules columns (Horizontal Timeline with custom Emojis)
cols = st.columns(len(modules))

for idx, mod in enumerate(modules):
    with cols[idx]:
        is_locked = mod["is_locked"]
        module_id = mod["Module_ID"]
        order = mod["Module_Order"]
        
        # Determine status and visual emojis
        if is_locked:
            status_style = "node-locked"
            status_text = "Locked"
            emoji = "🔒"
        else:
            progress_map = get_api("/api/v1/progress")
            c_progress = progress_map.get(st.session_state.selected_course_id, 1) if progress_map else 1
            
            if order < c_progress:
                status_style = "node-completed"
                status_text = "Completed"
                emoji = "✅"
            else:
                status_style = "node-active"
                status_text = "Active Level"
                emoji = "🎯"
                
        st.markdown(
            f"""
            <div class="node-container {status_style}">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">{emoji}</div>
                <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; font-weight: 500;">Module {order}</div>
                <div style="font-size: 1.05rem; font-weight: 700; margin: 0.25rem 0 0.5rem 0; height: 2.8rem; line-height: 1.3; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{mod['Title']}</div>
                <div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 0.75rem;">{status_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Action button or flat disabled text
        if is_locked:
            # Strictly flat disabled text preventing forward clicking
            st.markdown(
                """
                <div style="text-align: center; color: #6b7280; font-size: 0.9rem; padding: 0.5rem; background-color: rgba(31, 41, 55, 0.4); border-radius: 6px; border: 1px dashed rgba(255,255,255,0.05); font-weight: 500;">
                    🔒 Stage Locked
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            btn_label = "Review Video" if "Completed" in status_text else "Enter Module"
            if st.button(btn_label, key=f"btn_{module_id}", use_container_width=True):
                st.session_state.active_module_id = module_id
                st.session_state.verification_status = None
                st.session_state.verification_message = ""
                st.rerun()

st.markdown("---")

# Find selected module details
active_mod = None
for m in modules:
    if m["Module_ID"] == st.session_state.active_module_id:
        active_mod = m
        break

if active_mod:
    st.markdown(f"## 📖 Active Lesson: {active_mod['Title']}")
    
    col_video, col_quiz = st.columns([3, 2])
    
    with col_video:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### 📺 Tutorial Video")
        
        # Extract embed URL defensively
        embed_url = get_youtube_embed_url(active_mod["URL"])
        
        # Fluid Player Fallback check
        if "list=" in active_mod["URL"]:
            # Render using custom HTML component if playlist is present
            st.components.v1.html(
                f"<iframe width='100%' height='400' src='{embed_url}' frameborder='0' allowfullscreen></iframe>", 
                height=420
            )
        else:
            try:
                # Attempt native streamlit video rendering
                st.video(active_mod["URL"])
            except Exception:
                # Fallback to beautifully proportioned YouTube responsive frame
                st.components.v1.html(
                    f"<iframe width='100%' height='400' src='{embed_url}' frameborder='0' allowfullscreen></iframe>", 
                    height=420
                )
                
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_quiz:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### 👾 Coding Syntax Repair")
        
        # Display puzzle
        st.markdown(f"**Instructions:**\n{active_mod['Puzzle_Question']}")
        st.markdown(f"<div class='code-box'>{active_mod['Puzzle_Question']}</div>", unsafe_allow_html=True)
        
        # Display hint
        with st.expander("💡 Need a hint?"):
            st.info(active_mod["Puzzle_Hint"])
            
        progress_map = get_api("/api/v1/progress")
        c_progress = progress_map.get(st.session_state.selected_course_id, 1) if progress_map else 1
        
        # If already completed
        if active_mod["Module_Order"] < c_progress:
            st.success("🎉 You have already completed this level! Keep pushing forward.")
        else:
            # Inline answer submission callback
            def submit_solution():
                ans = st.session_state.user_ans_raw.strip()
                if not ans:
                    st.session_state.verification_status = "error"
                    st.session_state.verification_message = "⚠️ Please write your code answer."
                    return
                try:
                    res = requests.post(
                        f"{BASE_URL}/api/v1/module/verify",
                        json={
                            "course_id": st.session_state.selected_course_id,
                            "module_id": st.session_state.active_module_id,
                            "user_answer": ans
                        },
                        timeout=4
                    )
                    if res.status_code == 200:
                        data = res.json()
                        if data.get("success"):
                            st.session_state.verification_status = "success"
                            st.session_state.verification_message = data.get("message", "Correct!")
                            st.session_state.trigger_balloons = True
                            st.session_state.user_ans_raw = "" # Reset input box value
                        else:
                            st.session_state.verification_status = "warning"
                            st.session_state.verification_message = data.get("message", "Incorrect syntax.")
                    else:
                        st.session_state.verification_status = "error"
                        st.session_state.verification_message = f"⚠️ Server Error ({res.status_code})"
                except requests.exceptions.ConnectionError:
                    st.session_state.verification_status = "error"
                    st.session_state.verification_message = "⚠️ Backend Offline."

            st.text_input("Enter your solution:", key="user_ans_raw", placeholder="Type correct code syntax here...")
            st.button("Submit Answer", on_click=submit_solution, use_container_width=True)
            
            # Show status messages
            if st.session_state.verification_status == "success":
                st.success(st.session_state.verification_message)
            elif st.session_state.verification_status == "warning":
                st.warning(st.session_state.verification_message)
            elif st.session_state.verification_status == "error":
                st.error(st.session_state.verification_message)
                
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("💡 Select an unlocked module from the Skill Tree map above to begin learning!")
