import os
import csv
import sys
import sqlite3
# import unicode
from time import time
from app import app, models, db
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
# Base = declarative_base()
sqlite3.connect(os.path.abspath("app.db"))

db = SQLAlchemy(app)

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    spell_name = db.Column(db.String)
    school = db.Column(db.String)
    casting_time = db.Column(db.String)
    range = db.Column(db.String)
    components = db.Column(db.String)
    duration = db.Column(db.String)
    description = db.Column(db.String)
    caster_class = db.Column(db.String)

    def __repr__(self):
        return "<Spell %r>" % (self.spell_name)

def commit_to_db(filename):
    t = time()

    # engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))
    # Base.metadata.create_all(engine)
    #
    # session = sessionmaker()
    # session.configure(bind=engine)
    # s = session()

    with open(filename) as f:
        try:
            content = csv.reader(f, delimiter=',')
            for index, line in enumerate(content):
                if line[3] == "CastingTime":
                    print 'header: ' + index
                    pass
                record = models.Spell(**{
                    'level' : str(line[0]),
                    'spell_name' : unicode(line[1], 'utf-8'),
                    'school' : str(line[2]),
                    'casting_time' : str(line[3]),
                    'range' : str(line[4]),
                    'components' : str(line[5]),
                    'duration' : str(line[6]),
                    'description' : unicode(line[7], 'utf-8'),
                    'caster_class' : str(line[8])
                })
                # s.add(record)
                db.session.add(record)
            # s.commit()
            db.session.commit()
            print 'commited %s spell list' % (filename)
        except:
            print "threw an error: %s" % (str(sys.exc_info()[1]))
            # s.rollback()
            db.session.rollback()
            print 'rolled back %s ' % (filename)
        finally:
            # s.close()
            db.session.close()
        print "time elapsed: " + str(time() - t) + " s"


commit_to_db("csvs/wizard.csv")
if __name__ == "__main__":
    db.create_all()
    for file in os.listdir("csvs"):
        if '.csv' in file:
            print file
            commit_to_db("csvs/" + file)
