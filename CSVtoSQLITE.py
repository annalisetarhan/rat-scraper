import sqlite3
import pandas
from pandas import DataFrame

# Create table
conn = sqlite3.connect('RemoteAssociates.db')
c = conn.cursor()

c.execute('''CREATE TABLE REMOTE_ASSOCIATES
            ([generated_id] INTEGER PRIMARY KEY,
            [cue1] text,
            [cue2] text,
            [cue3] text,
            [solution] text,
            [difficulty_phrase] text,
            [difficulty] integer,
            [status] integer)''')

# Import CSV data with new headers
read_associates = pandas.read_csv('./results.csv', names=['cue1', 'cue2', 'cue3', 'solution', 'difficulty_phrase'])

read_associates.to_sql('REMOTE_ASSOCIATES', conn, if_exists='append', index=False)

# Set difficulty based on difficulty_phrase
c.execute('''UPDATE REMOTE_ASSOCIATES
            SET difficulty = 0
            WHERE difficulty_phrase = 'Very Easy'
            ''')
c.execute('''UPDATE REMOTE_ASSOCIATES
            SET difficulty = 1
            WHERE difficulty_phrase = 'Easy'
            ''')
c.execute('''UPDATE REMOTE_ASSOCIATES
            SET difficulty = 2
            WHERE difficulty_phrase = 'Medium'
            ''')
c.execute('''UPDATE REMOTE_ASSOCIATES
            SET difficulty = 3
            WHERE difficulty_phrase = 'Hard'
            ''')
c.execute('''UPDATE REMOTE_ASSOCIATES
            SET difficulty = 4
            WHERE difficulty_phrase = 'Very Hard'
            ''')
            
# Set status to 0 (for eventual use by app)
c.execute('''UPDATE REMOTE_ASSOCIATES
            SET status = 0
            ''')
            
conn.commit()
conn.close()
