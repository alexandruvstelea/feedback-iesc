from flask import Blueprint, jsonify, request
from models.courses import Course
from __init__ import db
from sqlalchemy import exc

course_bp = Blueprint("courses", __name__)


@course_bp.route("/courses", methods=["POST"])
def create_course():
    subject_id = request.form["subject_id"]
    type = request.form["type"]
    room_id = request.form["room_id"]
    day = request.form["day"]
    week_type = request.form["week_type"]
    start = request.form["start"]
    end = request.form["end"]
    start_end = [start, end]
    try:
        new_course = Course(subject_id, type, room_id, day, week_type, start_end)
        db.session.add(new_course)
        db.session.commit()
        return {"response": "New course added to database"}
    except:
        db.session.rollback()
        return {"response": "An error has occured"}, 404


@course_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = db.session.query(Course).all()
    courses_list = []
    for course in courses:
        courses_list.append(
            {
                "id": course.id,
                "subject_id": course.subject_id,
                "type": course.type,
                "room_id": course.room_id,
                "day": course.day,
                "week_type": course.week_type,
                "start": course.start_end[0].strftime("%H:%M"),
                "end": course.start_end[1].strftime("%H:%M"),
            }
        )
    return jsonify(courses_list)


@course_bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    new_subject_id = request.form["new_subject_id"]
    new_type = request.form["new_type"]
    new_room_id = request.form["new_room_id"]
    new_day = request.form["new_day"]
    new_week_type = request.form["new_week_type"]
    new_start = request.form["new_start"]
    new_end = request.form["new_end"]
    new_start_end = [new_start, new_end]
    try:
        affected_rows = (
            db.session.query(Course)
            .filter_by(id=course_id)
            .update(
                {
                    "subject_id": new_subject_id,
                    "type": new_type,
                    "room_id": new_room_id,
                    "day": new_day,
                    "week_type": new_week_type,
                    "start_end": new_start_end,
                }
            )
        )
    except exc.IntegrityError:
        db.session.rollback()
        return {"response": "An error has occured"}, 404
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Course with ID={course_id} updated."}
    else:
        return {"response": f"No course with ID={course_id} to update."}


@course_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    affected_rows = db.session.query(Course).filter_by(id=course_id).delete()
    if affected_rows > 0:
        db.session.commit()
        return {"response": f"Course with ID={course_id} deleted."}
    else:
        return {"response": f"No course with ID={course_id} to delete."}

