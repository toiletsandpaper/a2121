from sql_extended_objects import ExtObject as Object
from sql_extended_objects import ExtRequests as Database
from sql_extended_objects.sql_extended_objects import ExtUtils as DatabaseUtils

database = Database("student_siamese.sqlite")

database.commit(
    """
        CREATE TABLE IF NOT EXISTS `students` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT ,
            `first_name` TEXT(50) NOT NULL ,
            `last_name` TEXT(50) NOT NULL ,
            `middle_name` TEXT(50) NOT NULl ,
            `profile_name` TEXT(150) NOT NULL ,
            `photos` TEXT DEFAULT '[]'
            `university_id` INTEGER NOT NULL ,
            `university_name` TEXT(150) NOT NULL ,
            `group_id` INTEGER NOT NULL ,
            `group_name` TEXT(20) NOT NULL ,
            `email` TEXT(100) NOT NULL
        );
    """)
