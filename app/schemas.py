from pydantic import BaseModel, Field
from typing import List, Optional

class CourseResponse(BaseModel):
    course_id: str = Field(..., alias="Course_ID", description="Unique course identifier")
    title: str = Field(..., alias="Title", description="Title of the course")
    category: str = Field(..., alias="Category", description="Category classification")
    difficulty: str = Field(..., alias="Difficulty", description="Course difficulty level")
    avg_rating: float = Field(..., alias="Avg_Rating", description="Average user rating out of 5.0")

    class Config:
        populate_by_name = True

class ModuleResponse(BaseModel):
    course_id: str = Field(..., alias="Course_ID", description="Associated course identifier")
    module_id: str = Field(..., alias="Module_ID", description="Unique module identifier")
    title: str = Field(..., alias="Title", description="Title of the module")
    url: str = Field(..., alias="URL", description="YouTube video URL")
    module_order: int = Field(..., alias="Module_Order", description="Logical order of module")
    puzzle_question: str = Field(..., alias="Puzzle_Question", description="Puzzle question syntax repairing")
    puzzle_hint: str = Field(..., alias="Puzzle_Hint", description="Helpful hint for the puzzle")
    is_locked: bool = Field(..., description="Flag indicating if the module is locked for the student")

    class Config:
        populate_by_name = True

class CourseDetailsResponse(BaseModel):
    course_id: str = Field(..., alias="Course_ID")
    title: str = Field(..., alias="Title")
    category: str = Field(..., alias="Category")
    difficulty: str = Field(..., alias="Difficulty")
    avg_rating: float = Field(..., alias="Avg_Rating")
    modules: List[ModuleResponse] = Field([], description="List of modules in progression sequence")

    class Config:
        populate_by_name = True

class ModuleVerifyRequest(BaseModel):
    course_id: str = Field(..., description="Unique course ID")
    module_id: str = Field(..., description="Unique module ID")
    user_answer: str = Field(..., description="User's answer to the module's coding puzzle")

class ModuleVerifyResponse(BaseModel):
    success: bool = Field(..., description="True if answer is correct")
    message: str = Field(..., description="Feedback message for correct/incorrect answer")
    unlocked_next: bool = Field(..., description="True if next module is newly unlocked")
