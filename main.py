from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    course: str


app = FastAPI()

connection = psycopg2.connect(
    host="localhost",
    port="5433",
    database="postgres",
    user="postgres",
    password="1234"
)

cursor = connection.cursor()

@app.get("/students")

def get_all_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    # print(rows)

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "age": row[2],
        })

    return result

# Get single student by ID
@app.get("/students/{id}")

def get_single_student(id: int): #id: int: type hinting
    try:
        
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        row = cursor.fetchone()

        
        return {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            }
    except:
        raise HttpException(status_code=404, detail="Student not found")

#create student Record
@app.post("/students")

def create_student_record(student: Student):
    # print(student.id)
    # print(student.name)
    # print(student.course)
    try:
        cursor.execute("INSERT INTO students (id, name, course) VALUES (%s, %s, %s)", (student.id, student.name, student.course))
        connection.commit()
        raise HTTPException(status_code=201, detail="Student record created successfully")
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=400, detail="Student with this ID already exists")