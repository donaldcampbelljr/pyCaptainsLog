DATABASE="database/game.db"

from sqlmodel import Field, SQLModel, create_engine, Session


class StarSystem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class SystemEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    introtext: str



def main():

    # Setup
    sqlite_url = f"sqlite:///{DATABASE}"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)


    add_star_system(engine)


    return 0

def add_star_system(engine):

    system1 = StarSystem(name="Urth")
    event1 = SystemEvent(name="UrthEvent", introtext="Here is some intro text for the Urth Event.")

    with Session(engine) as session:

        session.add(event1)

        session.add(system1)
        
        session.commit()
        



    return 0


if __name__ == "__main__":
    main()
