import sqlite3
import datetime

# The database file name
DB_FILE = 'zillow_data.db'

def setup_db(conn):
    """
    Creates the necessary tables in the database.
    This function should be run once to set up the schema.
    """
    cursor = conn.cursor()

    # Create listing_agents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listing_agents (
        agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT,
        address TEXT,
        phone TEXT,
        comments TEXT
    );
    """)

    # Create properties table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        property_id TEXT PRIMARY KEY,
        property_name TEXT,
        url TEXT NOT NULL UNIQUE,
        listing_agent_id INTEGER,
        FOREIGN KEY (listing_agent_id) REFERENCES listing_agents (agent_id)
    );
    """)

    # Create scrape_results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scrape_results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id TEXT NOT NULL,
        scrape_date TEXT NOT NULL,
        days_on_market INTEGER,
        views INTEGER,
        saves INTEGER,
        FOREIGN KEY (property_id) REFERENCES properties (property_id)
    );
    """)
    conn.commit()

def update_scrape_results(conn, property_id, days_on_market, views, saves):
    """
    Inserts a new record into the scrape_results table.

    Args:
        conn: The database connection object.
        property_id (str): The unique ID of the property.
        days_on_market (int): The number of days the property has been on the market.
        views (int): The number of views.
        saves (int): The number of saves.
    """
    try:
        # Get a cursor object
        cursor = conn.cursor()

        # Generate a timestamp for the scrape date
        scrape_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # SQL statement to insert data into the table using a parameterized query
        sql = """
        INSERT INTO scrape_results (property_id, scrape_date, days_on_market, views, saves)
        VALUES (?, ?, ?, ?, ?);
        """
        
        # Execute the SQL statement with the data
        cursor.execute(sql, (property_id, scrape_date, days_on_market, views, saves))
        
        # Commit the transaction to save the changes to the database
        conn.commit()
        print(f"Successfully inserted scrape results for property '{property_id}'.")

    except sqlite3.Error as e:
        print(f"An error occurred while inserting data: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    try:
        # Connect to the SQLite database. It will create the file if it doesn't exist.
        conn = sqlite3.connect(DB_FILE)
        print(f"Connected to database: {DB_FILE}")

        # Set up the tables (run this once)
        setup_db(conn)

        # To test the foreign key constraint, we must first add a property.
        # This is a one-time step for a new property ID.
        try:
            conn.execute("INSERT INTO properties (property_id, property_name, url) VALUES (?, ?, ?)", 
                         ('200000', '123 Test St', 'https://www.zillow.com/test-property'))
            conn.commit()
            print("Added a sample property to the 'properties' table.")
        except sqlite3.IntegrityError:
            print("Sample property already exists.")

        # Sample data from a Zillow scrape
        scraped_data = {
            'property_id': '200000',
            'days_on_market': 204,
            'views': 1188,
            'saves': 61
        }
        
        # Call the function to update the scrape results table
        update_scrape_results(
            conn, 
            scraped_data['property_id'],
            scraped_data['days_on_market'],
            scraped_data['views'],
            scraped_data['saves']
        )

        # --- Verification Step ---
        print("\nVerifying the data was inserted:")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scrape_results WHERE property_id = '200000'")
        results = cursor.fetchall()
        for row in results:
            print(row)

    except sqlite3.Error as e:
        print(f"A connection error occurred: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")


def insert_property(conn, property_id, property_name, url, listing_agent_id=None):
    """
    Inserts a new property record into the properties table.
    
    Args:
        conn: The SQLite database connection object.
        property_id (str): The unique Zillow Property ID (ZPID).
        property_name (str): A descriptive name for the property.
        url (str): The full Zillow listing URL.
        listing_agent_id (int, optional): The ID of the listing agent. Defaults to None.
    
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO properties (property_id, property_name, url, listing_agent_id)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(sql, (property_id, property_name, url, listing_agent_id))
        conn.commit()
        print(f"✅ Successfully inserted new property: {property_name} ({property_id})")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Property with ID {property_id} or URL {url} already exists. Skipping.")
        return False
    except sqlite3.Error as e:
        print(f"❌ An error occurred inserting a new property: {e}")
        return False

# Example usage:
# conn = sqlite3.connect('zillow_data.db')
# insert_property(conn, '123456', '123 Main St, Anytown', 'https://www.zillow.com/home/123456')
# conn.close()


def insert_agent(conn, agent_name, address=None, phone=None, comments=None):
    """
    Inserts a new listing agent record into the listing_agents table.
    
    Args:
        conn: The SQLite database connection object.
        agent_name (str): The name of the agent.
        address (str, optional): The agent's address. Defaults to None.
        phone (str, optional): The agent's phone number. Defaults to None.
        comments (str, optional): Any additional comments. Defaults to None.

    Returns:
        int or None: The agent_id of the new record, or None if the insertion failed.
    """
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO listing_agents (agent_name, address, phone, comments)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(sql, (agent_name, address, phone, comments))
        conn.commit()
        agent_id = cursor.lastrowid
        print(f"✅ Successfully inserted new agent: {agent_name} with ID {agent_id}")
        return agent_id
    except sqlite3.Error as e:
        print(f"❌ An error occurred inserting a new agent: {e}")
        return None

# Example usage:
# conn = sqlite3.connect('zillow_data.db')
# new_agent_id = insert_agent(conn, 'Jane Doe', phone='555-1234')
# conn.close()


def update_property(conn, property_id, property_name=None, url=None, listing_agent_id=None):
    """
    Updates an existing property record.
    
    Args:
        conn: The SQLite database connection object.
        property_id (str): The unique ZPID of the property to update.
        property_name (str, optional): The new name for the property.
        url (str, optional): The new URL.
        listing_agent_id (int, optional): The new listing agent ID.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        cursor = conn.cursor()
        updates = []
        params = []
        
        if property_name is not None:
            updates.append("property_name = ?")
            params.append(property_name)
        if url is not None:
            updates.append("url = ?")
            params.append(url)
        if listing_agent_id is not None:
            updates.append("listing_agent_id = ?")
            params.append(listing_agent_id)

        if not updates:
            print("⚠️ No fields provided for update.")
            return False

        sql = f"UPDATE properties SET {', '.join(updates)} WHERE property_id = ?;"
        params.append(property_id)
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ Successfully updated property with ID: {property_id}")
            return True
        else:
            print(f"❌ No property found with ID: {property_id}")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ An error occurred while updating the property: {e}")
        return False

# Example usage:
# conn = sqlite3.connect('zillow_data.db')
# update_property(conn, '123456', listing_agent_id=1)
# conn.close()


def update_agent(conn, agent_id, agent_name=None, address=None, phone=None, comments=None):
    """
    Updates an existing agent record.
    
    Args:
        conn: The SQLite database connection object.
        agent_id (int): The ID of the agent to update.
        agent_name (str, optional): The new name for the agent.
        address (str, optional): The new address.
        phone (str, optional): The new phone number.
        comments (str, optional): New comments.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    try:
        cursor = conn.cursor()
        updates = []
        params = []
        
        if agent_name is not None:
            updates.append("agent_name = ?")
            params.append(agent_name)
        if address is not None:
            updates.append("address = ?")
            params.append(address)
        if phone is not None:
            updates.append("phone = ?")
            params.append(phone)
        if comments is not None:
            updates.append("comments = ?")
            params.append(comments)

        if not updates:
            print("⚠️ No fields provided for update.")
            return False
        
        sql = f"UPDATE listing_agents SET {', '.join(updates)} WHERE agent_id = ?;"
        params.append(agent_id)
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ Successfully updated agent with ID: {agent_id}")
            return True
        else:
            print(f"❌ No agent found with ID: {agent_id}")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ An error occurred while updating the agent: {e}")
        return False

# Example usage:
# conn = sqlite3.connect('zillow_data.db')
# update_agent(conn, 1, agent_name='Jane Doe, Realtor')
# conn.close()