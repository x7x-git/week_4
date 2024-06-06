from flask import g
from datetime import datetime

# 모든 질문 조회
def get_all_questions():
    cursor = g.db.cursor()
    cursor.execute("""
        SELECT q.id, q.title, q.time, COUNT(a.id) as answer_count
        FROM question q
        LEFT JOIN answer a ON q.id = a.question_id
        GROUP BY q.id
        ORDER BY q.time DESC
    """)
    questions = cursor.fetchall()
    return questions

# 페이지네이션 질문 조회
def get_paginated_questions(offset, limit):
    cursor = g.db.cursor()
    cursor.execute("""
        SELECT q.id, q.title, q.time, COUNT(a.id) as answer_count, p.username, q.user_id, q.password
        FROM question q
        LEFT JOIN answer a ON q.id = a.question_id
        LEFT JOIN passwd p ON q.user_id = p.id
        GROUP BY q.id, p.username, q.user_id
        ORDER BY q.time DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))
    questions = cursor.fetchall()
    return questions

# 총 질문 수 조회
def get_question_count():
    cursor = g.db.cursor()
    cursor.execute("SELECT COUNT(*) FROM question")
    count = cursor.fetchone()
    return count['COUNT(*)']

# 질문 삽입
def insert_question(title, content, user_id, password=None, file_path=None):
    cursor = g.db.cursor()
    cursor.execute("INSERT INTO question (title, content, user_id, password, file_path) VALUES (%s, %s, %s, %s, %s)", (title, content, user_id, password, file_path))
    g.db.commit()

# 특정 질문을 조회
def get_question_by_id(question_id):
    cursor = g.db.cursor()
    cursor.execute("""
        SELECT q.*, p.username
        FROM question q
        JOIN passwd p ON q.user_id = p.id
        WHERE q.id = %s
    """, (question_id,))
    question = cursor.fetchone()
    return question

# 답변 삽입
def insert_answer(question_id, content, user_id):
    cursor = g.db.cursor()
    cursor.execute("INSERT INTO answer (question_id, content, user_id) VALUES (%s, %s, %s)", (question_id, content, user_id))
    g.db.commit()

# 특정 질문 모든 답변 조회
def get_answers_by_question_id(question_id):
    cursor = g.db.cursor()
    cursor.execute("""
        SELECT a.*, p.username
        FROM answer a
        JOIN passwd p ON a.user_id = p.id
        WHERE a.question_id = %s
        ORDER BY a.time DESC
    """, (question_id,))
    answers = cursor.fetchall()
    return answers

# 특정 사용자 조회
def get_user_by_username(username):
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM passwd WHERE username = %s", (username,))
    user = cursor.fetchone()
    return user

# 특정 이메일 조회
def get_user_by_email(email):
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM passwd WHERE email = %s", (email,))
    user = cursor.fetchone()
    return user

# 사용자 삽입
def insert_user(username, password, email, name, school):
    cursor = g.db.cursor()
    cursor.execute("INSERT INTO passwd (username, password, email, name, school) VALUES (%s, %s, %s, %s, %s)", 
                   (username, password, email, name, school))
    g.db.commit()

# 사용자 ID로 사용자 조회
def get_user_by_id(user_id):
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM passwd WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return user

# 질문 수정
def update_question(question_id, title, content):
    cursor = g.db.cursor()
    cursor.execute("""
        UPDATE question
        SET title = %s, content = %s, modify_date = %s
        WHERE id = %s
    """, (title, content, datetime.now(), question_id))
    g.db.commit()

# 특정 답변을 조회
def get_answer_by_id(answer_id):
    cursor = g.db.cursor()
    cursor.execute("""
        SELECT a.*, p.username
        FROM answer a
        JOIN passwd p ON a.user_id = p.id
        WHERE a.id = %s
    """, (answer_id,))
    answer = cursor.fetchone()
    return answer

# 답변 수정
def update_answer(answer_id, content):
    cursor = g.db.cursor()
    cursor.execute("""
        UPDATE answer
        SET content = %s, modify_date = %s
        WHERE id = %s
    """, (content, datetime.now(), answer_id))
    g.db.commit()

# 질문 삭제
def delete_question(question_id):
    cursor = g.db.cursor()
    cursor.execute("DELETE FROM question WHERE id = %s", (question_id,))
    g.db.commit()

# 답변 삭제
def delete_answer(answer_id):
    cursor = g.db.cursor()
    cursor.execute("DELETE FROM answer WHERE id = %s", (answer_id,))
    g.db.commit()

# 검색을 위한 질문 조회
def search_questions(kw, offset, limit):
    cursor = g.db.cursor()
    search = f"%{kw}%"
    cursor.execute("""
        SELECT DISTINCT q.id, q.title, q.time, COUNT(a.id) as answer_count, p.username, q.user_id, q.password
        FROM question q
        LEFT JOIN answer a ON q.id = a.question_id
        LEFT JOIN passwd p ON q.user_id = p.id
        LEFT JOIN passwd pa ON a.user_id = pa.id
        WHERE q.title LIKE %s OR q.content LIKE %s OR p.username LIKE %s OR a.content LIKE %s OR pa.username LIKE %s
        GROUP BY q.id, p.username, q.user_id
        ORDER BY q.time DESC
        LIMIT %s OFFSET %s
    """, (search, search, search, search, search, limit, offset))
    questions = cursor.fetchall()
    return questions

# 사용자 프로필 업데이트
def update_user_profile(user_id, name, school, profile_image):
    cursor = g.db.cursor()
    cursor.execute("""
        UPDATE passwd
        SET name = %s, school = %s, profile_image = %s
        WHERE id = %s
    """, (name, school, profile_image, user_id))
    g.db.commit()