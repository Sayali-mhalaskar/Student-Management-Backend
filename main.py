from fastapi import FastAPI, HTTPException
import psycopg2



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

def get_single_student(id: int):
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

