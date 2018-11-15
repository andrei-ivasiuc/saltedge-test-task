import mysql.connector
import json


class Model(object):
    """
    Model class used for interactions with events DB
    """

    db_credentials = None

    def __init__(self):
        """
        Constructor, populates db connection credentials
        """
        with open('db_credentials.json') as f:
            self.db_credentials = json.load(f)

    def save_event(self, event):
        """
        Saves event to DB
        :param event: dict()
        :return: void()
        """
        keys = event.keys()
        values = event.values()
        # Adding auto-filled "created" column
        keys.append("created")
        query = "INSERT INTO `events` ({0}) VALUES({1}, NOW());".format(
            # Escaping column names
            ", ".join(["`{}`".format(k) for k in keys]),
            # Preparing values format
            ", ".join(["%s"]*len(values))
        )
        self.query(query, values)

    def get_events(self):
        """
        Retrieves last 20 events from DB
        :return: list()
        """
        rows = []
        query = "SELECT * FROM `events` ORDER BY `created` DESC LIMIT 0, 20;"
        # Iterates over rows, unpacks values
        for (id, action, body, created) in self.query(query):
            # If date column is not empty, converts date to string
            if created:
                created = created.strftime('%d-%m-%Y %H:%M:%S')
            rows.append(dict(zip(['id', 'action', 'body', 'created'], (id, action, body, created))))
        return rows

    def get_events_stats(self):
        """
        Retrieves events stats grouped by action
        :return: dict()
        """
        stats = {}
        query = "SELECT `action`, COUNT(`action`) FROM `events` GROUP BY `action`;"
        # Iterates over rows, unpacks values
        for (action, count) in self.query(query):
            stats[action] = count
        return stats

    def query(self, query, args=[]):
        """
        Perform mysql query

        Note: due to Flask architecture, and use of threads,
        mysql connection should be created per each request.

        :param query:
        :param args:
        :return: list()
        """
        result = []
        connection = mysql.connector.connect(**self.db_credentials)
        cursor = connection.cursor()
        cursor.execute(query, args)
        # If this is select query, fetch results
        if not len(args):
            result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result
