from sqlalchemy import Engine, create_engine, Column, Text, Integer, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session, Session
from contextlib import contextmanager


class Base(DeclarativeBase):
    pass


class ConnectionConfigModel(Base):
    __tablename__ = 'connection_configs'

    id = Column(Integer, primary_key=True)
    host = Column(Text)
    token = Column(Text)

    def to_dict(self):
        return {
            "id": self.id,
            "host": self.host,
            "token": self.token
        }


class RecordModel(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    color_r = Column(Integer)
    color_g = Column(Integer)
    color_b = Column(Integer)
    conductivity = Column(Float)
    ph = Column(Float)
    temperature = Column(Float)
    tds = Column(Float)
    turbidity = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "color_r": self.color_r,
            "color_g": self.color_g,
            "color_b": self.color_b,
            "conductivity": self.conductivity,
            "ph": self.ph,
            "temperature": self.temperature,
            "tds": self.tds,
            "turbidity": self.turbidity
        }


class DatabaseManager:
    _engine: Engine | None = None
    _Session:  scoped_session[Session] | None = None

    @classmethod
    def init(cls, db_url="sqlite:///storage/app.sqlite"):
        if not cls._engine:
            import os
            os.makedirs('storage', exist_ok=True)
            cls._engine = create_engine(db_url)
            cls._Session = scoped_session(sessionmaker(bind=cls._engine))
            Base.metadata.create_all(cls._engine)

    @classmethod
    @contextmanager
    def _session(cls):
        if cls._Session is None:
            raise RuntimeError(
                "Database not initialized. Call DatabaseManager.init() first.")
        session = cls._Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # ---- CRUD Genérico ----
    @classmethod
    def add(cls, obj: Base):
        with cls._session() as s:
            s.add(obj)

    @classmethod
    def get(cls, model: Base, obj_id):
        with cls._session() as s:
            return s.get(model, obj_id).to_dict()  # type: ignore

    @classmethod
    def get_first(cls, model: Base):
        with cls._session() as s:
            r = s.query(model).first()  # type: ignore
            if r:
                return r.to_dict()
            return None

    @classmethod
    def get_all(cls, model: Base):
        with cls._session() as s:
            list_records = s.query(model).all()  # type: ignore
            return [record.to_dict() for record in list_records]

    @classmethod
    def update(cls, model: Base, obj_id, **kwargs):

        with cls._session() as s:

            obj = s.get(model, obj_id)  # type: ignore

            if obj:
                for k, v in kwargs.items():
                    setattr(obj, k, v)
                return True
            return False
