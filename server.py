from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import uvicorn

app = FastAPI()

# تحميل الداتا
courses = pd.read_csv("udemy_courses_dataset.csv")
courses.fillna('', inplace=True)

# شكل البيانات اللي هيبعتها المستخدم
class Answers(BaseModel):
    webDevelopment: bool
    databases: bool
    mobileDevelopment: bool
    algorithms: bool

@app.post("/recommendations")
def recommend_courses(answers: Answers):
    recommendations = []

    for idx, course in courses.iterrows():
        score = 0
        title = str(course['course_title']).lower()

        
        if answers.webDevelopment and ("web" in title or "frontend" in title or "react" in title or "javascript" in title):
            score += 1
        if answers.databases and ("database" in title or "sql" in title or "mongodb" in title or "mysql" in title):
            score += 1
        if answers.mobileDevelopment and ("android" in title or "ios" in title or "flutter" in title or "mobile" in title):
            score += 1
        if answers.algorithms and ("algorithm" in title or "data structure" in title or "algorithms" in title):
            score += 1

        if score > 0:
            recommendations.append({
                "course_title": course['course_title'],
                "url": course['url'],
                "score": score
            })

    # ترتيب حسب السكور
    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)

    return recommendations[:10]  # نرجع أفضل 10 كورسات

@app.get("/")
def read_root():
    return {"message": "Course Recommendation API is Live 🚀"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
