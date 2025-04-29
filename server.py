from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# تفعيل الـ CORS لو بتتعامل مع Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تحميل الداتا
courses = pd.read_csv("udemy_courses_dataset.csv")
courses.fillna('', inplace=True)

feedback_store = []

class Answers(BaseModel):
    webDevelopment: bool
    databases: bool
    mobileDevelopment: bool
    algorithms: bool

class Feedback(BaseModel):
    course_title: str
    useful: bool

@app.get("/")
def read_root():
    return {"message": "Course Recommendation API is Live 🚀"}

@app.post("/recommendations")
def recommend_courses(answers: Answers):
    recommendations = []

    for idx, course in courses.iterrows():
        score = 0
        title = str(course['course_title']).lower()

        if answers.webDevelopment and any(keyword in title for keyword in ["web", "frontend", "react", "javascript"]):
            score += 1
        if answers.databases and any(keyword in title for keyword in ["database", "sql", "mongodb", "mysql"]):
            score += 1
        if answers.mobileDevelopment and any(keyword in title for keyword in ["android", "ios", "flutter", "mobile"]):
            score += 1
        if answers.algorithms and any(keyword in title for keyword in ["algorithm", "data structure", "algorithms"]):
            score += 1

        if score > 0:
            recommendations.append({
                "course_title": course['course_title'],
                "url": course['url'],
                "score": score
            })

    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
    return recommendations[:10]

@app.post("/feedback")
def receive_feedback(feedback: Feedback):
    feedback_store.append(feedback.dict())
    print("Feedback received:", feedback.dict())
    return {"message": "Feedback recorded!"}
