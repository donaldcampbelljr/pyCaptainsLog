DATABASE="database/game.db"

from sqlmodel import Field, SQLModel, create_engine, Session, Column, null, JSON
from typing import Optional


class StarSystem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    event_list: Optional[list] = Field(None, sa_type=JSON)
    # eventlist: list = Field(sa_column=Column(JSON),
    #                     default=null(),)
    # systemdict: Optional[dict] = Field(sa_column=Column(JSON),
    #                     default=null(),)
    #systemdict: Optional[dict] = Field(None, sa_type=JSON)

class StoryEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    intro_text: str
    strength: int
    event_type: str

class Planet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    intro_text: str
    event_list: Optional[list] = Field(None, sa_type=JSON)



def main():

    # Setup
    sqlite_url = f"sqlite:///{DATABASE}"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)


    add_star_system(engine)


    return 0

def add_star_system(engine):


    random_dict = {'a':1, 'b': 2}
    systemlist = [1,2,3,4,5,6,7]

    system1 = StarSystem(name="Urth System", event_list=systemlist)
    event1 = StoryEvent(name="UrthEvent", intro_text="Here is some intro text for the Urth Event.", strength=5, event_type="combat")
    planet1 = Planet(name="Urth", intro_text="Some intro text for planet Urth")

    with Session(engine) as session:

        session.add(event1)

        session.add(system1)

        session.add(planet1)
        
        session.commit()
        



    return 0


if __name__ == "__main__":
    main()
