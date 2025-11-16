import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check if columns exist
cursor.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cursor.fetchall()]

print(f"Existing columns in students table: {columns}")

if 'first_name' not in columns:
    cursor.execute('ALTER TABLE students ADD COLUMN first_name VARCHAR(100) NULL')
    print('✓ Added first_name column')
    
if 'last_name' not in columns:
    cursor.execute('ALTER TABLE students ADD COLUMN last_name VARCHAR(100) NULL')
    print('✓ Added last_name column')

conn.commit()
conn.close()
print('✅ Database updated with student name fields')
