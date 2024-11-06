
import random
import pandas as pd
import csv
import logging
import psycopg2

conn = psycopg2.connect(
    dbname="Lab3",
    user="postgres",
    password="Password1",
    host="localhost",
    port="5432"
)

"""cursor = conn.cursor()

# Drop existing tables (if needed) and recreate them with the correct schema
cursor.execute('''DROP TABLE IF EXISTS LecturerSubjects CASCADE''')
cursor.execute('''DROP TABLE IF EXISTS Lecturers CASCADE''')
cursor.execute('''DROP TABLE IF EXISTS Subjects CASCADE''')
cursor.execute('''DROP TABLE IF EXISTS Groups CASCADE''')
cursor.execute('''DROP TABLE IF EXISTS Rooms CASCADE''')
# Recreate tables in PostgreSQL
cursor.execute('''CREATE TABLE IF NOT EXISTS Groups (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    num_students INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Subjects (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    hours_lecture INTEGER NOT NULL,
                    hours_practice INTEGER NOT NULL,
                    requires_split BOOLEAN NOT NULL,
                    group_id INTEGER REFERENCES Groups(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Lecturers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    max_hours_per_week INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS LecturerSubjects (
                    lecturer_id INTEGER REFERENCES Lecturers(id),
                    subject_name VARCHAR(50) NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Rooms (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    capacity INTEGER NOT NULL)''')

# Commit the schema creation
conn.commit()"""

# Function to insert data
"""def save_data(groups, group_subjects, lecturers, rooms):
    for group in groups:
        cursor.execute("INSERT INTO Groups (name, num_students) VALUES (%s, %s) RETURNING id", 
                       (group.name, group.num_students))
        group_id = cursor.fetchone()[0]

        for subject in group_subjects[group.name]:
            cursor.execute('''INSERT INTO Subjects (name, hours_lecture, hours_practice, requires_split, group_id)
                              VALUES (%s, %s, %s, %s, %s)''', 
                           (subject.name, subject.hours_lecture, subject.hours_practice, subject.requires_split, group_id))

    for lecturer in lecturers:
        cursor.execute("INSERT INTO Lecturers (name, max_hours_per_week) VALUES (%s, %s) RETURNING id", 
                       (lecturer.name, lecturer.max_hours_per_week))
        lecturer_id = cursor.fetchone()[0]

        for subject in lecturer.subjects:
            cursor.execute("INSERT INTO LecturerSubjects (lecturer_id, subject_name) VALUES (%s, %s)", 
                           (lecturer_id, subject))

    for room in rooms:
        cursor.execute("INSERT INTO Rooms (name, capacity) VALUES (%s, %s)", 
                       (room.room_id, room.capacity))

    # Commit the data
    conn.commit()"""


# Configure logging to a file
logging.basicConfig(
    filename='genome_generation.log',  # Specify the log file name
    filemode='w',  # 'w' for overwrite mode, 'a' for append mode
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)
# Клас для зберігання груп
class Group:
    def __init__(self, name, num_students):
        self.name = name
        self.num_students = num_students
        self.subgroups = []

    def create_subgroups(self):
        # Завжди створюємо рівно дві підгрупи, незалежно від кількості студентів
        self.subgroups = [Group(f"{self.name} Subgroup {i + 1}", self.num_students // 2) for i in range(2)]


# Клас для зберігання викладачів
class Lecturer:
    def __init__(self, name, subjects, max_hours_per_week,is_lect=False, lect_room = 0):
        self.is_lect = is_lect
        self.lecture_room = lect_room
        self.name = name
        self.subjects = subjects  # список предметів, які може викладати
        self.max_hours_per_week = max_hours_per_week  # максимальна кількість годин на тиждень


# Клас для зберігання предметів
class Subject:
    def __init__(self, name, hours_lecture, hours_practice, requires_split=False):
        self.name = name
        self.hours_lecture = hours_lecture
        self.hours_practice = hours_practice
        self.requires_split = requires_split


# Клас для зберігання аудиторій
class Room:
    def __init__(self, room_id, capacity):
        self.room_id = room_id
        self.capacity = capacity


# Генерація даних
"""def generate_data():
    groups = [
        Group("Group 1", 30),
        Group("Group 2", 28),
        Group("Group 3", 32),
        Group("Group 4", 25),
        Group("Group 5", 27)
    ]

    group_subjects = {
        "Group 1": [
            Subject("Math", 30, 15, True),
            Subject("Physics", 25, 10, False)
        ],
        "Group 2": [
            Subject("Chemistry", 20, 10, True),
            Subject("Biology", 15, 10, False)
        ],
        "Group 3": [
            Subject("Math", 30, 15, True),
            Subject("Chemistry", 20, 10, True)
        ],
        "Group 4": [
            Subject("Physics", 25, 10, False),
            Subject("Biology", 15, 10, False)
        ],
        "Group 5": [
            Subject("Math", 30, 15, True),
            Subject("Chemistry", 20, 10, True),
            Subject("Biology", 15, 10, False)
        ]
    }

    lecturers = [
        Lecturer("Dr. Smith", ["Math", "Physics"], max_hours_per_week=10),
        Lecturer("Dr. Jones", ["Chemistry", "Biology"], max_hours_per_week=8)
    ]

    rooms = [Room(f"Room {i + 1}", random.randint(25, 35)) for i in range(6)]

    return groups, group_subjects, lecturers, rooms"""


def generate_genome_for_slot(groups_, group_subjects_, lecturers_, rooms_, time_slot):
    for group in groups_:
        group.create_subgroups()

    available_subgroups = [subgroup for group in groups_ for subgroup in group.subgroups]
    available_lecturers = lecturers_[:]
    available_rooms = rooms_[:]

    slot_genome = []



    while available_subgroups and available_lecturers and available_rooms:
        logging.info(f"Generating genome for Time Slot {time_slot}")
        logging.info(f"Available Subgroups: {[sg.name for sg in available_subgroups]}")
        logging.info(f"Available Lecturers: {[lecturer.name for lecturer in available_lecturers]}")
        logging.info(f"Available Rooms: {[room.room_id for room in available_rooms]}")
        subgroup = random.choice(available_subgroups)
        original_group_name = subgroup.name.rsplit(" Subgroup", 1)[0]
        #print(original_group_name)
        if original_group_name not in group_subjects_:
            available_subgroups.remove(subgroup)
            logging.warning(
                f"Original group name {original_group_name} not found in subjects. Skipping subgroup {subgroup.name}.")
            continue

        subject = random.choice(group_subjects_[original_group_name])
        valid_lecturers = [l for l in available_lecturers if subject.name in l.subjects]

        logging.info(f"Selected Subject: {subject.name} for Group: {original_group_name}")

        if not valid_lecturers:
            available_subgroups.remove(subgroup)
            logging.warning(
                f"No valid lecturers available for subject {subject.name}. Skipping subgroup {subgroup.name}.")
            continue

        lecturer = random.choice(valid_lecturers)
        room = random.choice(available_rooms)

        logging.info(f"Selected Lecturer: {lecturer.name} for Subject: {subject.name} in Room: {room.room_id}")
        """slot_genome.append({
            "group": subgroup.name,
            "subject": subject.name,
            "lecturer": lecturer.name,
            "room": room.room_id,
        })"""
        if subject.requires_split:
            """if (lecturer.is_lect == False):
                slot_genome.append({
                    "group": subgroup.name,
                    "subject": subject.name,
                    "lecturer": lecturer.name,
                    "room": room.room_id,
                })"""
            slot_genome.append({
                "group": subgroup.name,
                "subject": subject.name,
                "lecturer": lecturer.name,
                "room": room.room_id,
            })
            available_lecturers.remove(lecturer)
            available_subgroups.remove(subgroup)
            available_rooms.remove(room)

        else:
            """if (lecturer.is_lect == False):
                slot_genome.append({
                    "group": original_group_name,
                    "subject": subject.name,
                    "lecturer": lecturer.name,
                    "room": room.room_id,
                })
                lecturer.is_lect = True
                lecturer.lecture_room = room.room_id
            else:
                slot_genome.append({
                    "group": original_group_name,
                    "subject": subject.name,
                    "lecturer": lecturer.name,
                    "room": lecturer.lecture_room,
                })"""
            """slot_genome.append({
                "group": original_group_name,
                "subject": subject.name,
                "lecturer": lecturer.name,
                "room": room.room_id,
            })"""
            slot_genome.append({
                "group": original_group_name,
                "subject": subject.name,
                "lecturer": lecturer.name,
                "room": room.room_id,
            })
            available_subgroups = [sg for sg in available_subgroups if
                                   sg.name != subgroup.name and sg.name != f"{original_group_name} Subgroup {2 if subgroup.name.endswith('1') else 1}"]
            available_rooms.remove(room)
            available_lecturers.remove(lecturer)

    logging.info(f"Generated {len(slot_genome)} entries for Time Slot {time_slot}.")
    logging.info(f"Slot Genome Entries: {slot_genome}")
    return slot_genome


def generate_weekly_genome(groups_, group_subjects_, lecturers_, rooms_):
    weekly_genome = {}

    for time_slot in range(1, 21):  # 20 time slots
        weekly_genome[time_slot] = generate_genome_for_slot(groups_, group_subjects_, lecturers_, rooms_, time_slot)

    return weekly_genome


def initialize_population(groups, group_subjects, lecturers, rooms, population_size=10):
    population = []
    for _ in range(population_size):
        genome = generate_weekly_genome(groups, group_subjects, lecturers, rooms)
        population.append(genome)
    write_population_to_csv(population)
    #write_population_to_db(population)
    return population

def write_population_to_csv(population, filename='population.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(['Time Slot', 'Group', 'Subject', 'Lecturer', 'Room'])

        # Iterate over the population
        for genome in population:
            for time_slot, slots in genome.items():
                for slot in slots:
                    writer.writerow([time_slot, slot['group'], slot['subject'], slot['lecturer'], slot['room']])
def fitness(schedule, groups, lecturers, rooms, group_subjects):
       
    score = 0

    # Жорсткі обмеження
    for time_slot, slots in schedule.items():
        for slot in slots:
            # Визначення назви групи
            if "Subgroup" in slot["group"]:
                group_name = slot["group"].rsplit(" Subgroup", 1)[0]
            else:
                group_name = slot["group"]

            group = next((g for g in groups if g.name == group_name), None)
            if group is None:
                continue

            room = next((r for r in rooms if r.room_id == slot["room"]), None)
            if room is None:
                continue

            if group.num_students > room.capacity:
                score -= 100  # Штраф за перевищення місткості аудиторії

    # Нежорсткі обмеження
    group_subject_hours = {
        group.name: {subject.name: {"lecture": 0, "practice": 0} for subject in group_subjects[group.name]} for group in
        groups}

    # Розподіл годин у розкладі
    for time_slot, slots in schedule.items():
        for slot in slots:
            group_name = slot["group"].rsplit(" Subgroup", 1)[0]
            
            if group_name not in group_subjects:
                #print(f"KeyError: '{group_name}' not found in group_subjects")
                continue

            subject = next((s for s in group_subjects[group_name] if s.name == slot["subject"]), None)
            if subject is None:
                #print(f"Subject not found for slot: {slot}")
                continue

            # Оновлення годин залежно від типу заняття
            if "lecture" in slot["subject"].lower():
                group_subject_hours[group_name][subject.name]["lecture"] += 1.5
            else:
                group_subject_hours[group_name][subject.name]["practice"] += 1.5

    # Штраф за недотримання годин
    for group in groups:
        for subject in group_subjects[group.name]:
            actual_lecture_hours = group_subject_hours[group.name][subject.name]["lecture"]
            actual_practice_hours = group_subject_hours[group.name][subject.name]["practice"]

            lecture_deficit = abs(actual_lecture_hours - subject.hours_lecture)
            practice_deficit = abs(actual_practice_hours - subject.hours_practice)

            score -= lecture_deficit * 1000  # Штраф за пропущені/перевищені години лекцій
            score -= practice_deficit * 1000  # Штраф за пропущені/перевищені години практики

    # Додання штрафу за "вікна" (гепи) у розкладі для викладачів та студентів
    lecturer_schedules = {lecturer.name: [] for lecturer in lecturers}
    group_schedules = {group.name: [] for group in groups}

    # Збираємо розклади для викладачів та груп
    for time_slot, slots in schedule.items():
        for slot in slots:
            lecturer_schedules[slot["lecturer"]].append(time_slot)
            group_name = slot["group"].rsplit(" Subgroup", 1)[0]
            group_schedules[group_name].append(time_slot)

    # Розраховуємо штрафи за "вікна" у розкладі
    for schedule_type, schedules in [("lecturer", lecturer_schedules), ("group", group_schedules)]:
        for name, times in schedules.items():
            times.sort()  # Сортуємо час для розрахунку прогалин
            gaps = sum(1 for i in range(1, len(times)) if times[i] - times[i - 1] > 1)
            score -= gaps * 5  # Коригуємо штраф залежно від необхідності

    return score

def fitness2(schedule, groups, lecturers, rooms, group_subjects):
    score=fitness(schedule, groups, lecturers, rooms, group_subjects)
    return 1/(1+score)

# Основний алгоритм
def genetic_algorithm(groups, group_subjects, lecturers, rooms, fitness_func, generations=1000):
    # Initialize the population
    population = initialize_population(groups, group_subjects, lecturers, rooms)

    for generation in range(generations):
        # Sort the population based on the fitness function
        population = sorted(population, key=lambda x: fitness_func(x, groups, lecturers, rooms, group_subjects), reverse=True)
        
        # Select the top half of the population
        new_population = population[:len(population) // 2]
        
        # Generate new individuals to fill the population
        while len(new_population) < len(population):
            parent1 = random.choice(population[:len(population) // 2])
            parent2 = random.choice(population[:len(population) // 2])
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)
        
        population = new_population

    # Return the best schedule based on the provided fitness function
    best_schedule = max(population, key=lambda x: fitness_func(x, groups, lecturers, rooms, group_subjects))
    return best_schedule


# Функція перехрестя
def crossover(parent1, parent2):
    child = {}
    for time_slot in range(1, 21):
        if time_slot in parent1 and time_slot in parent2:
            child[time_slot] = random.choice([parent1[time_slot], parent2[time_slot]])
    return child


# Функція мутації
def mutate2(genome):
    # Можливість зміни одного з часів або предметів
    time_slot = random.choice(list(genome.keys()))
    if genome[time_slot]:
        genome[time_slot] = random.choice([generate_genome_for_slot(groups, group_subjects, lecturers, rooms, time_slot)])
def mutate(genome):
    # Randomly select a time slot to apply mutation
    time_slot = random.choice(list(genome.keys()))
    if not genome[time_slot]:
        return

    slots = genome[time_slot]
    mutation_applied = False

    for slot in slots:
        group_name = slot["group"].rsplit(" Subgroup", 1)[0]  # Remove "Subgroup" if present
        group = next((g for g in groups if g.name == group_name), None)
        room = next((r for r in rooms if r.room_id == slot["room"]), None)
        lecturer = next((l for l in lecturers if l.name == slot["lecturer"]), None)

        # Non-trivial mutation: Room adjustment for capacity
        if room and group and group.num_students > room.capacity:
            # Find a larger room
            larger_rooms = [r for r in rooms if r.capacity >= group.num_students]
            if larger_rooms:
                new_room = random.choice(larger_rooms)
                logging.info(f"Mutating room for {slot['group']} from {room.room_id} to {new_room.room_id}")
                slot["room"] = new_room.room_id
                mutation_applied = True

        # Non-trivial mutation: Lecturer adjustment for workload
        if lecturer and lecturer.max_hours_per_week < sum(1 for s in genome.values() for g in s if g['lecturer'] == lecturer.name):
            # Find an alternative lecturer for the subject
            qualified_lecturers = [l for l in lecturers if slot["subject"] in l.subjects and l != lecturer]
            if qualified_lecturers:
                new_lecturer = random.choice(qualified_lecturers)
                logging.info(f"Mutating lecturer for {slot['subject']} from {lecturer.name} to {new_lecturer.name}")
                slot["lecturer"] = new_lecturer.name
                mutation_applied = True

    # If no mutation was applied, perform a random re-assignment mutation
    if not mutation_applied:
        genome[time_slot] = generate_genome_for_slot(groups, group_subjects, lecturers, rooms, time_slot)

def write_schedule_to_csv(schedule, filename='best_schedule.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(['Time Slot', 'Group', 'Subject', 'Lecturer', 'Room'])

        # Iterate over the schedule
        for time_slot, slots in schedule.items():
            for slot in slots:
                # Assuming each slot has the keys 'group', 'subject', 'lecturer', and 'room'
                writer.writerow([time_slot, slot['group'], slot['subject'], slot['lecturer'], slot['room']])

    print(f"Schedule saved to {filename}")

# Retrieve and transform data from the database
def load_data():
    # Load Groups
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, num_students FROM Groups")
    group_records = cursor.fetchall()
    groups = [Group(name, num_students) for _, name, num_students in group_records]
    
    print("Groups:")
    for group in groups:
        print(f"Name: {group.name}, Students: {group.num_students}")
    
    # Load Subjects by Group
    cursor.execute("SELECT name, hours_lecture, hours_practice, requires_split, group_id FROM Subjects")
    subject_records = cursor.fetchall()
    group_subjects = {}
    for group in groups:
        group_subjects[group.name] = [
            Subject(name, hours_lecture, hours_practice, requires_split)
            for name, hours_lecture, hours_practice, requires_split, group_id in subject_records
            if group_id == group_records[groups.index(group)][0]  # Match group_id with the correct group
        ]
    
    print("\nSubjects by Group:")
    for group_name, subjects in group_subjects.items():
        print(f"Group: {group_name}")
        for subject in subjects:
            print(f"  Subject: {subject.name}, Hours Lecture: {subject.hours_lecture}, "
                  f"Hours Practice: {subject.hours_practice}, Requires Split: {subject.requires_split}")
    
    # Load Lecturers and their Subjects
    cursor.execute("SELECT id, name, max_hours_per_week FROM Lecturers")
    lecturer_records = cursor.fetchall()
    lecturers = []
    for lecturer_id, name, max_hours_per_week in lecturer_records:
        cursor.execute("SELECT subject_name FROM LecturerSubjects WHERE lecturer_id = %s", (lecturer_id,))
        subjects = [row[0] for row in cursor.fetchall()]
        lecturers.append(Lecturer(name, subjects, max_hours_per_week))
    
    print("\nLecturers and their Subjects:")
    for lecturer in lecturers:
        print(f"Lecturer: {lecturer.name}, Max Hours per Week: {lecturer.max_hours_per_week}")
        for subject in lecturer.subjects:
            print(f"  Teaches: {subject}")
    
    # Load Rooms
    cursor.execute("SELECT name, capacity FROM Rooms")
    room_records = cursor.fetchall()
    rooms = [Room(name, capacity) for name, capacity in room_records]
    
    
    
    # Close the connection
    cursor.close()
    # conn.close()

    return groups, group_subjects, lecturers, rooms

def save_schedule2(schedule_data):
    for entry in schedule_data:
        time_slot, group, subject, lecturer, room = entry
        cursor.execute('''
            INSERT INTO Schedule (time_slot, group_name, subject_name, lecturer_name, room_name)
            VALUES (%s, %s, %s, %s, %s)
        ''', (time_slot, group, subject, lecturer, room))

    # Commit the data
    conn.commit()

def save_schedule_to_db(schedule, table_name='Schedule'):
    # Connect to PostgreSQL
    global conn
    cursor = conn.cursor()

    # Clear the table before inserting new data
    cursor.execute(f"DELETE FROM {table_name}")
    
    # Commit the delete operation
    conn.commit()

    # Iterate over the schedule and insert the new data
    for time_slot, slots in schedule.items():
        for slot in slots:
            group = slot['group']
            subject = slot['subject']
            lecturer = slot['lecturer']
            room = slot['room']

            # Insert the data into the table
            cursor.execute(f'''
                INSERT INTO {table_name} (time_slot, group_name, subject_name, lecturer_name, room_name)
                VALUES (%s, %s, %s, %s, %s)
            ''', (time_slot, group, subject, lecturer, room))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    print(f"Schedule saved to {table_name} table in the database.")

# Основна частина
if __name__ == "__main__":
    #groups, group_subjects, lecturers, rooms = generate_data()
    #save_data(groups, group_subjects, lecturers, rooms)
    # Load and print data
    groups, group_subjects, lecturers, rooms = load_data()
    best_schedule = genetic_algorithm(groups, group_subjects, lecturers, rooms, fitness_func=fitness2)
    #print(best_schedule)
    #write_schedule_to_csv(best_schedule)
    save_schedule_to_db(best_schedule)
