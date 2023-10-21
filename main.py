import sqlite3 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# Setup
# create a file in the same directory called hci.db
# run init_db() function below
# run seed_db function below



def init_db():
    
    # Define the database name
    database_name = "hci.db"  # You can change the name as needed

    # Create a connection to the SQLite database
    conn = sqlite3.connect(database_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Define the SQL command to create the FAQ table
    create_table_sql = """
   CREATE TABLE IF NOT EXISTS faq_table (
    id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);
    """

    # Execute the SQL command to create the table
    cursor.execute(create_table_sql)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    print(f"Database '{database_name}' and table 'faq_table' created successfully.")
def seed_db():
    # Define the database name
    database_name = "hci.db"

    # Create a connection to the SQLite database
    conn = sqlite3.connect(database_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Sample FAQ data
    faq_data = [
        ("Where can I replace my school ID?", "You can replace your school ID at the IEET office."),
        ("Where can I pick up my logbook?", "You can pick up your logbook at the SCC office."),
        ("What is the exam schedule for this semester?", "The exam schedule is available on the university website."),
        # Add more FAQ data here
    ]

    # Insert the sample FAQ data into the database
    for question, answer in faq_data:
        cursor.execute("INSERT INTO faq_table (question, answer) VALUES (?, ?)", (question, answer))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    print("Sample FAQ data inserted into the database.")


# Step 1: Database Interaction (adapted for SQLite)
def query_database(student_question):

    # Connect to the SQLite database
    conn = sqlite3.connect('hci.db')  # Replace 'faq_database.db' with your SQLite database file

    cursor = conn.cursor()

    # Execute an SQL query to retrieve questions and answers
    query = f'SELECT id, question, answer FROM faq_table where question like "%{student_question[0]}%"'
    for (index, value) in enumerate(student_question):
        if(index == 0):
            continue 
        else:
            query += f' or question like "%{value}%"'  # Or...abit tricky..
        
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# Step 2: Natural Language Processing
def preprocess_text(text:str)-> list[str]:
    # Implement text preprocessing (e.g., tokenization, lowercasing, removing stop words, etc.)
    # Here, we'll keep it simple with lowercase and tokenization.
    return text.lower().split()

# Step 3: Feature Extraction and Similarity Calculation
def calculate_relevance(student_question, possible_answers):
 
    tfidf_vectorizer = TfidfVectorizer()
   
    tfidf_matrix = tfidf_vectorizer.fit_transform([student_question] + possible_answers)
    
    cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_indices = cosine_similarities.argsort()[::-1]
    
    return ranked_indices



# Step 4: Ranking by Relevance
def rank_answers(student_question,  possible_answers):
    if(len(possible_answers)==0):
        return []

    ranked_indices = calculate_relevance(student_question, [i[1] for i in possible_answers])
    
    ranked_answers = [possible_answers[i] for i in ranked_indices]

    return ranked_answers

# Student's question
print("Question in the context of:")
print("1. logbook")
print("2. schoolId")
print("3. exam timetable")
student_question = input("your question: ") 

possible_answers = query_database(preprocess_text(student_question))
print(possible_answers)


# # Step 4: Rank answers by relevance
ranked_answers = rank_answers(student_question,  possible_answers)

# # Present the most relevant answer to the student
if ranked_answers:
    most_relevant_answer = ranked_answers[0]
    print("Most relevant answer:", {"question":student_question,"answer":most_relevant_answer[2]})
else:
    print("No relevant answer found.")
