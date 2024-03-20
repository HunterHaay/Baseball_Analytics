import pyodbc

# Specify the file path to the MS Access database
database_path = "C:/Users/wagnerbl20/Downloads/lahman_1871-2022.mdb"

try:
    # Connect to the MS Access database
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + database_path)
    cursor = conn.cursor()

    # SQL query to select necessary columns from the Batting table
    sql_query = """
        SELECT playerID, AB, BB, HBP, SF, SH
        FROM Batting;
    """

    # Execute the SQL query
    cursor.execute(sql_query)

    # Dictionary to store plate appearances for each player
    plate_appearances = {}

    # Calculate plate appearances for each player
    for row in cursor.fetchall():
        player_id, ab, bb, hbp, sf, sh = row
        pa = (ab or 0) + (bb or 0) + (hbp or 0) + (sf or 0) + (sh or 0)
        if player_id in plate_appearances:
            plate_appearances[player_id] += pa
        else:
            plate_appearances[player_id] = pa

    # Display plate appearances for each player
    for player_id, pa in plate_appearances.items():
        print(f"PlayerID: {player_id}, Plate Appearances: {pa}")

except pyodbc.Error as e:
    print("Error connecting to the database:", e)

finally:
    # Close the database connection
    if conn:
        conn.close()
