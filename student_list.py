import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Student Progress Tracking",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for exact matching
st.markdown("""
    <style>
    /* Reset and base styles */
    .main {
        padding: 0 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: white !important;
        padding: 2rem 1rem !important;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 1rem;
    }
    
    .logo-hex {
        background-color: #6B4EFF;
        width: 45px;
        height: 45px;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Navigation styling */
    .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 4px;
        cursor: pointer;
        color: #666;
    }
    
    .nav-item.active {
        background-color: #F0F0FF;
        color: #6B4EFF;
        font-weight: 500;
    }
    
    /* Student card styling */
    .student-card {
        background-color: #E8F5F5;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .student-card.selected {
        background-color: #F0F0FF;
    }
    
    .student-info {
        flex-grow: 1;
    }
    
    .close-button {
        color: #666;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0.2rem 0.5rem;
    }
    
    /* Timeline styling */
    .timeline-container {
        margin: 2rem 0;
        padding: 1rem;
        position: relative;
    }
    
    .timeline {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin: 2rem 0;
    }
    
    .milestone {
        text-align: center;
        position: relative;
        z-index: 2;
    }
    
    .milestone-dot {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        margin: 0 auto 0.5rem;
    }
    
    .milestone-dot.complete {
        background-color: #92E3A9;
    }
    
    .milestone-dot.incomplete {
        background-color: #FFB4B4;
    }
    
    .milestone-line {
        position: absolute;
        top: 12px;
        left: 10%;
        right: 10%;
        height: 2px;
        background-color: #E0E0E0;
        z-index: 1;
    }
    
    /* Commit history styling */
    .commit-container {
        margin-top: 2rem;
    }
    
    .commit-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .commit-dot {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: #FF9966;
        flex-shrink: 0;
        margin-top: 0.25rem;
    }
    
    .commit-empty {
        background-color: transparent;
        border: 2px solid #FF9966;
    }
    
    /* Header styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        border-bottom: 1px solid #E0E0E0;
    }
    
    .profile-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .profile-image {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo and app name
    st.markdown("""
        <div class="logo-container">
            <div class="logo-hex"></div>
            <span>Application<br>Name</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    menu_items = ["Home", "Milestones", "Students", "Github History"]
    active_index = 2
    
    for i, item in enumerate(menu_items):
        active_class = "active" if i == active_index else ""
        st.markdown(f"""
            <div class="nav-item {active_class}">
                {item}
            </div>
        """, unsafe_allow_html=True)

# Main content area
# Header with add student and profile
st.markdown("""
    <div class="header-container">
        <button style="background-color: transparent; border: none; color: #6B4EFF; font-size: 1rem; cursor: pointer;">
            <span style="font-size: 1.2rem;">+</span> Add Student
        </button>
        <div class="profile-section">
            <div style="text-align: right">
                <div>Instructor Name</div>
                <div style="color: #666;">Instructor ID</div>
            </div>
            <div class="profile-image"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main content columns
col1, col2 = st.columns([4, 6])

# Student list column
with col1:
    students = [
        {"name": "Student Name 1", "email": "Student Email", "selected": True},
        {"name": "Student Name", "email": "Student Email", "selected": False},
        {"name": "Student Name", "email": "Student Email", "selected": False},
        {"name": "Student Name", "email": "Student Email", "selected": False},
        {"name": "Student Name", "email": "Student Email", "selected": False},
    ]
    
    for student in students:
        selected_class = "selected" if student["selected"] else ""
        st.markdown(f"""
            <div class="student-card {selected_class}">
                <div class="student-info">
                    <div style="font-weight: 500;">{student["name"]}</div>
                    <div style="color: #666;">{student["email"]}</div>
                </div>
                <div class="close-button">×</div>
            </div>
        """, unsafe_allow_html=True)

# Student details column
with col2:
    st.markdown("<h2 style='margin-top: 1rem;'>Student Name 1</h2>", unsafe_allow_html=True)
    
    # Timeline
    milestones = [
        {"name": "Milestone 1", "date": "Date", "complete": True},
        {"name": "Milestone 2", "date": "Date", "complete": True},
        {"name": "Milestone 3", "date": "Date", "complete": True},
        {"name": "Milestone 4", "date": "Date", "complete": False},
        {"name": "Milestone 5", "date": "Date", "complete": False}
    ]
    
    st.markdown("""
        <div class="timeline-container">
            <div class="timeline">
                <div class="milestone-line"></div>
    """, unsafe_allow_html=True)
    
    for milestone in milestones:
        status = "complete" if milestone["complete"] else "incomplete"
        st.markdown(f"""
            <div class="milestone">
                <div class="milestone-dot {status}"></div>
                <div>{milestone["name"]}</div>
                <div style="color: #666;">{milestone["date"]}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Commit history
    st.markdown("<h3>Commit History</h3>", unsafe_allow_html=True)
    
    commits = [
        {"number": 5, "time": "08:36 am 22/08/2024", "filled": True},
        {"number": 4, "time": "08:36 am 22/08/2024", "filled": False},
        {"number": 3, "time": "08:36 am 22/08/2024", "filled": False}
    ]
    
    for commit in commits:
        empty_class = "" if commit["filled"] else "commit-empty"
        st.markdown(f"""
            <div class="commit-item">
                <div class="commit-dot {empty_class}"></div>
                <div>
                    <div style="font-weight: 500;">Commit {commit["number"]}</div>
                    <div style="color: #666;">Time stamp: {commit["time"]}</div>
                    <a href="#" style="color: #6B4EFF; text-decoration: none;">Github link</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Insights link
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <a href="#" style="color: #6B4EFF; text-decoration: none;">
                Would you like to get more insights?
            </a>
        </div>
    """, unsafe_allow_html=True)