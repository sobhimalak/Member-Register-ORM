import sqlite3
import streamlit as st

conn = sqlite3.connect("Database.db")
query = (""" CREATE TABLE IF NOT EXISTS members (
                    id_num INTEGER PRIMARY KEY NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    address TEXT,
                    post_number TEXT,
                    subscription TEXT) """)
conn.execute(query)
conn.close()

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

tab1, tab2, tab3 = st.tabs(["Add Member", "Members In Database", "Search Members"])

with tab1:
    st.header("Please enter the required information below")

    first_name, last_name = st.columns(2)
    address, post_number = st.columns(2)

    first_name = first_name.text_input("First name:", key = 'first_name')
    last_name = last_name.text_input("Last name:")
    address = address.text_input("Address:")
    post_number = post_number.text_input("Post Number:")
    subscription = st.radio("Subscription", ["Paid", "Not Paid"])

    st.write(first_name, last_name)
    st.write(address, post_number)

    st.write('<style>'
             'div.row-widget.stRadio > div{flex-direction:row;}'
             'div.stButton > button:first-child {width: 100%;height: 3em;border-radius:0; }'
             '</style>',
             unsafe_allow_html = True)

    if st.button("Submit"):
        # Insert the data into the database
        cursor.execute(
            "INSERT INTO members (first_name, last_name, address, post_number, subscription) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, address, post_number, subscription)
            )
        conn.commit()
        st.success("Form submitted successfully!")

with tab2:
    st.header("Filter Members")
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()

    # Create a radio button group to select the filter criteria
    filter_criteria = st.radio("Filter by:", ["All", "Paid", "Not Paid"])
    # Filter the data based on the radio button selection
    if filter_criteria == "Paid":
        rows = [row for row in rows if row[5] == "Paid"]
    elif filter_criteria == "Not Paid":
        rows = [row for row in rows if row[5] == "Not Paid"]

    st.table(rows)

with tab3:
    st.header("Search for required information below")
    search_term = st.text_input("Enter search term:")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members WHERE '
                   'first_name LIKE ? OR last_name LIKE ?'
                   'OR address LIKE ? OR subscription LIKE ?'
                   'OR id_num LIKE ?', (f'%{search_term}%',
                                        f'%{search_term}%', f'%{search_term}%',
                                        f'%{search_term}%', f'%{search_term}%'))
    rows = cursor.fetchall()
    st.header("Search Results")
    st.table(rows)

conn.close()
