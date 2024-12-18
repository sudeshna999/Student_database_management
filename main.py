from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional

app = FastAPI()

# MongoDB connection
client = MongoClient("your_mongodb_connection_string")  # Replace with your actual MongoDB connection string
db = client.student_management
students_collection = db.students

# Pydantic model for the Student
class Student(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    age: int
    email: str
    enrolled_courses: List[str] = []

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Sudeshna Dey",
                "age": 23,
                "email": "sudeshnadey@example.com",
                "enrolled_courses": ["Math", "Science"]
            }
        }

# Create a new student
@app.post("/students", response_model=Student, status_code=201)
async def create_student(student: Student):
    student_dict = student.dict(exclude_unset=True)
    result = students_collection.insert_one(student_dict)
    student.id = str(result.inserted_id)
    return student

# Get all students
@app.get("/students", response_model=List[Student])
async def get_students():
    students = []
    for student in students_collection.find():
        student['id'] = str(student['_id'])
        students.append(Student(**student))
    return students

# Get a student by ID
@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    student['id'] = str(student['_id'])
    return Student(**student)

# Update a student by ID
@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student: Student):
    student_dict = student.dict(exclude_unset=True)
    result = students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": student_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    student.id = student_id
    return student

# Delete a student by ID
@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: str):
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Management API"}