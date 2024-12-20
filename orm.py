

from sqlmodel import Field, SQLModel, create_engine, Session, Column, null, JSON, select
from typing import Optional
from constants import DATABASE


class StarSystem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    forward_unlocked: bool = False
    #event_list: Optional[list] = Field(None, sa_type=JSON)
    # eventlist: list = Field(sa_column=Column(JSON),
    #                     default=null(),)
    # systemdict: Optional[dict] = Field(sa_column=Column(JSON),
    #                     default=null(),)
    #systemdict: Optional[dict] = Field(None, sa_type=JSON)

class StoryEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    intro_text: str
    health: int
    strength: int
    event_type: str

class Planet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    intro_text: str
    event_id: str #story event id associated with the planet
    #event_list: Optional[list] = Field(None, sa_type=JSON)

class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    intro_text: str
    strength: int
    card_type: str

def main():

    # # Setup
    # sqlite_url = f"sqlite:///{DATABASE}"
    # engine = create_engine(sqlite_url, echo=True)
    # SQLModel.metadata.create_all(engine)


    # add_star_system(engine)

    # star_system = retrieve_star_system(name = "Urth System", engine = engine)

    # print(f"Here is retrieved the star system {star_system.name}")

    # star_system_2 = retrieve_single_entity(StarSystem, "Urth System", engine=engine )
    # print("\n\n-------------------------------------------------")
    # print(f"Here is retrieved the star system {star_system_2.name}")

    # result = entity_exists(StarSystem, "Alpha Centauri", engine=engine)

    # print(result)


    return 0

# def create_engine(database_url):
    
#     engine = create_engine(database_url, echo=True)

#     return engine

def create_orm():
    sqlite_url = f"sqlite:///{DATABASE}"
    try:
        engine = create_engine(sqlite_url, echo=True)
        model = SQLModel.metadata.create_all(engine)
    except Exception:
        print("Cannot create engine. Is the sqllite databse url correct?")
    

    return model, engine

def retrieve_star_system(name, engine):
    print("DEBUG: retrieve_star system")
    with Session(engine) as session:
        statement = select(StarSystem).where(StarSystem.name == name)
        results = session.exec(statement).first()
    return results   
     
def retrieve_single_entity(table_name,entity_name, engine):
    print("DEBUG: SINGLE ENTITY")
    with Session(engine) as session:
        statement = select(table_name).where(table_name.name == entity_name)
        results = session.exec(statement).first()
    
    return results

def entity_exists(table_name,entity_name, engine):

    """ Checks if Entity exists in the database."""
    
    with Session(engine) as session:
        statement = select(table_name).where(table_name.name == entity_name)
        results = session.exec(statement).first()

    if results:
        return True
    else:
        return False


def add_star_syste_db(engine,starsystem):


    # random_dict = {'a':1, 'b': 2}
    # systemlist = [1,2,3,4,5,6,7]

    system1 = StarSystem(name=starsystem.name, forward_unlocked=True)

    # system1 = StarSystem(name="Urth System", forward_unlocked=True)
    # event1 = StoryEvent(name="UrthEvent", intro_text="Here is some intro text for the Urth Event.", strength=5, health=9,event_type="combat")
    # planet1 = Planet(name="Urth", intro_text="Some intro text for planet Urth", event_id="random-event_identifier")
    # card1 = Card(name="card1", intro_text="card1 intro text", strength=6, card_type="science")

    with Session(engine) as session:

        session.add(system1)
        
        session.commit()
        



    return 0


if __name__ == "__main__":
    main()
