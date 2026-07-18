import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from app.schemas import CourseResponse, ModuleResponse, CourseDetailsResponse, ModuleVerifyRequest, ModuleVerifyResponse

app = FastAPI(
    title="Neural Learn API - Deep Course Progression",
    description="Production-ready FastAPI backend for E-Learning Content Recommendation & Progression.",
    version="2.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COURSES_CSV = "data/courses.csv"
MODULES_CSV = "data/modules.csv"

# Global database states
courses_db = {}
modules_db = []
user_progress = {}

def load_data():
    global courses_db, modules_db, user_progress
    
    # Generate data files automatically if missing
    if not os.path.exists(COURSES_CSV) or not os.path.exists(MODULES_CSV):
        from scripts.generate_data import generate_all
        generate_all()
        
    # Read Courses from CSV
    df_courses = pd.read_csv(COURSES_CSV)
    courses_db = {}
    for _, row in df_courses.iterrows():
        c_id = str(row["Course_ID"]).strip()
        courses_db[c_id] = {
            "Course_ID": c_id,
            "Title": str(row["Title"]).strip(),
            "Category": str(row["Category"]).strip(),
            "Difficulty": str(row["Difficulty"]).strip(),
            "Avg_Rating": float(row["Avg_Rating"])
        }
        # Initialize progression: max unlocked module order is 1 by default
        if c_id not in user_progress:
            user_progress[c_id] = 1

    # Read Modules from CSV
    df_modules = pd.read_csv(MODULES_CSV)
    modules_db = []
    for _, row in df_modules.iterrows():
        modules_db.append({
            "Course_ID": str(row["Course_ID"]).strip(),
            "Module_ID": str(row["Module_ID"]).strip(),
            "Title": str(row["Title"]).strip(),
            "URL": str(row["URL"]).strip(),
            "Module_Order": int(row["Module_Order"]),
            "Puzzle_Question": str(row["Puzzle_Question"]).strip(),
            "Puzzle_Hint": str(row["Puzzle_Hint"]).strip(),
            "Puzzle_Answer": str(row["Puzzle_Answer"]).strip()
        })

# Load CSV files on startup
load_data()

@app.get("/api/v1/courses", response_model=List[CourseResponse])
def get_all_courses():
    """
    Get all courses available in the system.
    """
    sorted_courses = sorted(courses_db.values(), key=lambda x: int(x["Course_ID"]))
    return [CourseResponse(**c) for c in sorted_courses]

@app.get("/api/v1/course/{course_id}", response_model=CourseDetailsResponse)
def get_course_details(course_id: str):
    """
    Get course details along with list of sequence-ordered modules,
    injecting the is_locked flag dynamically according to the student's progress.
    """
    c_id = str(course_id).strip()
    if c_id not in courses_db:
        raise HTTPException(status_code=404, detail=f"Course ID '{c_id}' not found.")
        
    course = courses_db[c_id]
    current_unlocked = user_progress.get(c_id, 1)
    
    course_modules = []
    for m in modules_db:
        if m["Course_ID"] == c_id:
            course_modules.append(ModuleResponse(
                Course_ID=m["Course_ID"],
                Module_ID=m["Module_ID"],
                Title=m["Title"],
                URL=m["URL"],
                Module_Order=m["Module_Order"],
                Puzzle_Question=m["Puzzle_Question"],
                Puzzle_Hint=m["Puzzle_Hint"],
                is_locked=m["Module_Order"] > current_unlocked
            ))
            
    # Order modules sequentially by Module_Order
    course_modules.sort(key=lambda x: x.module_order)
    
    return CourseDetailsResponse(
        Course_ID=course["Course_ID"],
        Title=course["Title"],
        Category=course["Category"],
        Difficulty=course["Difficulty"],
        Avg_Rating=course["Avg_Rating"],
        modules=course_modules
    )

@app.post("/api/v1/module/verify", response_model=ModuleVerifyResponse)
def verify_module(request: ModuleVerifyRequest):
    """
    Submit an answer for a module's coding challenge.
    Defensively normalizes strings to ignore spacing and quotes.
    Increments user progress on correct match.
    """
    c_id = str(request.course_id).strip()
    m_id = str(request.module_id).strip()
    user_ans = str(request.user_answer)
    
    if c_id not in courses_db:
        raise HTTPException(status_code=404, detail=f"Course ID '{c_id}' not found.")
        
    target_module = None
    for m in modules_db:
        if m["Course_ID"] == c_id and m["Module_ID"] == m_id:
            target_module = m
            break
            
    if not target_module:
        raise HTTPException(status_code=404, detail=f"Module ID '{m_id}' not found in Course ID '{c_id}'.")
        
    order = target_module["Module_Order"]
    current_unlocked = user_progress.get(c_id, 1)
    
    # Defensive check: ensure they cannot submit for locked modules
    if order > current_unlocked:
        raise HTTPException(status_code=403, detail="Access denied: Module is currently locked.")
        
    # Helper to aggressively normalize strings
    def normalize(text: str) -> str:
        return text.strip().lower().replace(" ", "").replace('"', "'")
        
    norm_user = normalize(user_ans)
    norm_db = normalize(target_module["Puzzle_Answer"])
    
    if norm_user == norm_db:
        unlocked_next = False
        if order == current_unlocked:
            user_progress[c_id] = current_unlocked + 1
            unlocked_next = True
        return ModuleVerifyResponse(
            success=True,
            message="🎉 Correct! Your syntax mapping matches the requirements.",
            unlocked_next=unlocked_next
        )
    else:
        return ModuleVerifyResponse(
            success=False,
            message="❌ Incorrect syntax. Pay attention to semicolons, braces, or brackets.",
            unlocked_next=False
        )

@app.get("/api/v1/progress")
def get_user_progress():
    """
    Get user progress map for all courses.
    """
    return user_progress

@app.post("/api/v1/progress/reset")
def reset_progress():
    """
    Reset user progress for all courses to module order 1.
    """
    global user_progress
    for c_id in courses_db:
        user_progress[c_id] = 1
    return {"status": "success", "message": "All course progressions reset back to level 1.", "progress": user_progress}

# Serve static frontend files if directory exists
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
