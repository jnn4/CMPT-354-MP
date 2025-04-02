from flask import Blueprint, request, jsonify
from models import Volunteer, Person, Staff, db
from sqlalchemy.exc import IntegrityError
from datetime import date
from werkzeug.security import generate_password_hash

volunteer_bp = Blueprint('volunteer', __name__, url_prefix='/volunteers')

# Get all volunteers
@volunteer_bp.route('/', methods=['GET'])
def get_all_volunteers():
    try:
        # Join Volunteer, Staff, and Person tables to get complete volunteer information
        volunteers = db.session.query(
            Volunteer.volunteer_id,
            Person.first_name,
            Person.last_name,
            Person.email,
            Person.phone_num,
            Volunteer.role,
            Volunteer.start_date,
            Volunteer.end_date
        ).join(Staff, Volunteer.volunteer_id == Staff.staff_id).join(Person, Staff.email == Person.email).all()

        # Format the response
        volunteer_list = [
            {
                "volunteer_id": v[0],
                "first_name": v[1],
                "last_name": v[2],
                "email": v[3],
                "phone_num": v[4],
                "role": v[5],
                "start_date": v[6].strftime('%Y-%m-%d') if v[6] else None,
                "end_date": v[7].strftime('%Y-%m-%d') if v[7] else None
            }
            for v in volunteers
        ]
        
        return jsonify(volunteer_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create a new volunteer
@volunteer_bp.route('/post', methods=['POST'])
def create_volunteer():
    try:
        data = request.get_json()

        # Extract data from request
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        phone = data.get('phone')
        role = data.get('role')
        availability = data.get('availability')
        skills = data.get('skills')

        # Validation
        if not all([first_name, last_name, email, phone, role]):
            return jsonify({"message": "First name, last name, email, phone, and role are required!"}), 400

        # Check if person already exists
        existing_person = Person.query.get(email)
        if existing_person:
            # Update existing person's information
            existing_person.first_name = first_name
            existing_person.last_name = last_name
            existing_person.phone_num = phone
        else:
            # Create new person
            new_person = Person(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_num=phone
            )
            db.session.add(new_person)
            db.session.flush()  # Get the person's email without committing

        # Check if person is already a staff member
        existing_staff = Staff.query.get(email)
        if existing_staff:
            return jsonify({"message": "You are already registered as a staff member!"}), 400

        # Create new staff member
        new_staff = Staff(
            email=email,
            position=role,
            password=generate_password_hash('volunteer123')  # Default password
        )
        db.session.add(new_staff)
        db.session.flush()  # Get the staff_id without committing

        # Check if person is already a volunteer
        existing_volunteer = Volunteer.query.filter_by(volunteer_id=new_staff.staff_id).first()
        if existing_volunteer:
            return jsonify({"message": "You are already registered as a volunteer!"}), 400

        # Create new volunteer
        new_volunteer = Volunteer(
            volunteer_id=new_staff.staff_id,
            role=role,
            start_date=date.today(),
            end_date=None  # No end date for new volunteers
        )
        db.session.add(new_volunteer)
        db.session.commit()

        return jsonify({
            "message": "Volunteer created successfully!",
            "volunteer_id": new_volunteer.volunteer_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "A database error occurred!"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get volunteer by ID
@volunteer_bp.route('/<int:volunteer_id>', methods=['GET'])
def get_volunteer_by_id(volunteer_id):
    try:
        volunteer = Volunteer.query.get(volunteer_id)
        if not volunteer:
            return jsonify({"message": "Volunteer not found!"}), 404

        return jsonify({
            "volunteer_id": volunteer.id,
            "name": volunteer.name,
            "contact": volunteer.contact,
            "skills": volunteer.skills,
            "availability": volunteer.availability
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update volunteer details
@volunteer_bp.route('/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    try:
        data = request.get_json()
        volunteer = Volunteer.query.get(volunteer_id)

        if not volunteer:
            return jsonify({"message": "Volunteer not found!"}), 404

        name = data.get('name', volunteer.name)
        contact = data.get('contact', volunteer.contact)
        skills = data.get('skills', volunteer.skills)
        availability = data.get('availability', volunteer.availability)

        # Update volunteer fields
        volunteer.name = name
        volunteer.contact = contact
        volunteer.skills = skills
        volunteer.availability = availability

        db.session.commit()

        return jsonify({
            "message": "Volunteer updated successfully!",
            "volunteer_id": volunteer.id,
            "name": volunteer.name,
            "contact": volunteer.contact,
            "skills": volunteer.skills,
            "availability": volunteer.availability
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a volunteer
@volunteer_bp.route('/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    try:
        volunteer = Volunteer.query.get(volunteer_id)
        if not volunteer:
            return jsonify({"error": "Volunteer not found"}), 404
        
        # Delete the volunteer
        db.session.delete(volunteer)
        db.session.commit()
        
        return jsonify({"message": "Volunteer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Populate the Volunteer table
@volunteer_bp.route('/populate', methods=['POST'])
def populate_volunteer():
    try:
        volunteer_data = [
            {"role": "Event Coordinator", "start_date": date(2025, 1, 10), "end_date": date(2025, 5, 10)},
            {"role": "Mentor", "start_date": date(2025, 2, 1), "end_date": date(2025, 6, 1)},
            {"role": "Workshop Leader", "start_date": date(2025, 3, 15), "end_date": date(2025, 7, 15)},
            {"role": "Event Coordinator", "start_date": date(2025, 4, 1), "end_date": None},  # Ongoing
            {"role": "Admin Assistant", "start_date": date(2025, 1, 20), "end_date": date(2025, 5, 20)},
            {"role": "Marketing Assistant", "start_date": date(2025, 2, 10), "end_date": date(2025, 6, 10)},
            {"role": "Volunteer Trainer", "start_date": date(2025, 3, 5), "end_date": date(2025, 7, 5)},
            {"role": "Event Coordinator", "start_date": date(2025, 4, 10), "end_date": None},  # Ongoing
            {"role": "Workshop Leader", "start_date": date(2025, 5, 1), "end_date": date(2025, 9, 1)},
            {"role": "Admin Assistant", "start_date": date(2025, 6, 1), "end_date": date(2025, 10, 1)}
        ]

        inserted_count = 0
        skipped_count = 0

        # Get all available staff to assign as volunteers
        staff_members = db.session.query(Staff).all()
        staff_list = [staff.staff_id for staff in staff_members]  # Extract staff IDs

        for i, data in enumerate(volunteer_data):
            if i >= len(staff_list):
                break  # Stop if we run out of staff members

            staff_id = staff_list[i]  # Assign a staff ID as volunteer_id

            # Check if this staff is already a volunteer
            existing_volunteer = db.session.query(Volunteer).filter_by(volunteer_id=staff_id).first()

            if not existing_volunteer:
                try:
                    new_volunteer = Volunteer(
                        volunteer_id=staff_id,
                        role=data["role"],
                        start_date=data["start_date"],
                        end_date=data["end_date"]
                    )
                    db.session.add(new_volunteer)
                    db.session.commit()
                    inserted_count += 1
                except IntegrityError:
                    db.session.rollback()
                    skipped_count += 1
            else:
                skipped_count += 1

        return jsonify({
            "message": "Volunteer population completed",
            "inserted": inserted_count,
            "skipped": skipped_count
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate Volunteer", "error": str(e)}), 500


