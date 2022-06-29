from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE bar (
            id SERIAL NOT NULL PRIMARY KEY,
            name varchar(128) NOT NULL
        );
        CREATE TABLE foo (
            id SERIAL NOT NULL PRIMARY KEY,
            status varchar(128) NOT NULL,
            bar_id integer REFERENCES bar(id) NOT NULL
        );
        """,
        """
        DROP TABLE foo CASCADE;
        DROP TABLE bar CASCADE;
        """,
    )
]
