import streamlit as st
import app_db_setup as dbs
import pandas as pd

def load_data():
    connection = dbs.init_db()
    print("CONNECTION: ", connection)
    query = "SELECT * FROM magicians_all;"
    magicians_all_df = pd.read_sql_query(query, connection)
    query = "SELECT * FROM locations;"
    locations_df = pd.read_sql_query(query, connection)
    query = "SELECT * FROM magicians_rounds;"
    magicians_rounds_df = pd.read_sql_query(query, connection)
    query = "SELECT * FROM shows;"
    shows_df = pd.read_sql_query(query, connection)
    connection.close()
    return magicians_all_df, locations_df, magicians_rounds_df, shows_df


def draw_map(df):
    st.map(df[["latitude", "longitude"]], zoom = 0)
    

def reveal_magicians(mag_all_df, mag_rounds_df, loc_df):
    merged_df = pd.merge(mag_all_df, mag_rounds_df, 
                                        left_on="id", right_on="fk_magician_id")
    merged_df.drop_duplicates(subset=["name"], inplace=True)
    mag_loc_df = pd.merge(merged_df, loc_df, 
                            left_on="fk_location_id", right_on="id")[["name", "city", "country"]]
    st.write(mag_loc_df)


def list_shows_from_db():
    st.header("Find magic shows using DB tables:")
    magician = st.text_input("Magician name:", "")
    if magician == "":
        return
    connection = dbs.init_db()
    cur = connection.cursor()
    cur.execute("SELECT * FROM magicians WHERE name = '%s'" % magician)
    magician_id = cur.fetchone()[0]
    query = """SELECT * FROM shows WHERE fk_magician_1_id = %s
                    OR fk_magician_2_id = %s;""" % (str(magician_id), str(magician_id))
    df = pd.read_sql_query(query, connection)
    if len(df) > 0:
        st.write(df)
    else:
        st.info("Sorry, no shows found 😥.")


def list_shows_from_df(magicians_df, shows_df):
    st.header("Find magic shows using dataframes:")
    magician = st.text_input("Magician_df name:", "")
    if magician == "":
        return
    magician_id = magicians_df[magicians_df["name"] == magician]["id"].values[0]
    selected_shows_df = shows_df[(shows_df["fk_magician_1_id"] == magician_id) |
                                 (shows_df["fk_magician_2_id"] == magician_id)]
    if len(selected_shows_df) > 0:
        st.write(selected_shows_df)
    else:
        st.info("Sorry, no shows found 😥.")
