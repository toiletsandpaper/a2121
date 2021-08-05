from sql_extended_objects import ExtObject as Object
from sql_extended_objects import ExtRequests as Database
from sql_extended_objects.sql_extended_objects import ExtUtils as DatabaseUtils

database = Database("student_siamese.sqlite")

database.commit(
    """
        CREATE TABLE IF NOT EXISTS `students` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT ,
            `photos` TEXT DEFAULT '[]' ,
            `username` TEXT(100) NOT NULL ,
            `password` TEXT(100) NOT NULL
        );
    """)
