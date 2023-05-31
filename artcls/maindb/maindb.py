import psycopg2


class DatabWorker:
    __slots__ = ['db_name', 'user', 'password', 'conn', 'host', 'port', 'table_name']

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str, conn=None) -> None:
        """Initialize DatabWorker object.

        Args:
            db_name (str): database name.
            user (str): postgres user.
            password (str): password database.
            host (str): host database.
            port (str): port database.
            conn : psycopg2 connection object.

        Returns:
            None
        """
        self.db_name = db_name
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        self.conn = conn

    def __call__(self, data_to_write: list[tuple], table_name: str = 'all_artickle_table') -> None:
        """Writes data to the database.

        Args:
            data_to_write (list[tuple]): data to be entered into the database.
            table_name (str): Name of datatable.

        Returns:
            None
        """
        self.__data_writer(data_artickle=data_to_write, user_table=table_name)
        print('Data written successfully DB')

    def __create_table(self, table_name: str = 'all_artickle_table') -> None:
        """Creates a table named table_name.

        Args:
            table_name (str): The name of the table to be created.

        Returns:
            None
        """
        with self.conn.cursor() as cursor:
            cursor.execute("""CREATE TABLE {}
                (id serial,
                NAME TEXT NOT NULL,
                HREF TEXT NOT NULL,
                TAGS TEXT,
                CLASS TEXT NOT NULL);""".format(table_name))
        self.conn.commit()

    def __table_exists(self, table_name: str = 'all_artickle_table') -> bool:
        """Checks if the table_name exists.

        Args:
            table_name (str): the name of the table whose existence is checked.

        Returns:
            bool: Returns a log type indicating the existence of the table.
        """
        with self.conn.cursor() as cursor:
            cursor.execute("select exists(select 1 from information_schema.tables where table_name=%s)", [table_name])
            place_holder = cursor.fetchone()
        return place_holder[0]

    def __data_writer(self, data_artickle: list[tuple], user_table: str) -> None:
        """Adds data_artickle data to a table named user_table.

        Args:
            data_artickle (list[tuple]): Data to add to table, format example [(4, 'LG', 800), (5, 'One Plus 6', 950)].
            user_table (str): The name of the table where the data will be stored.

        Returns:
            None
        """
        self.conn = psycopg2.connect(dbname=self.db_name,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host,
                                     port=self.port)

        if not self.__table_exists(table_name=user_table):
            self.__create_table(table_name=user_table)

        with self.conn.cursor() as curs:
            sql_insert_query = """INSERT INTO {} (name, href, tags, class)
                                                  VALUES (%s,%s,%s,%s) """.format(user_table)
            curs.executemany(sql_insert_query, data_artickle)

        self.conn.commit()
        self.conn.close()
