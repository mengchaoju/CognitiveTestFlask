from sqlalchemy.ext.automap import automap_base
from app import engine

Base = automap_base()
Base.prepare(engine, reflect=True)
staff = Base.classes.staff
participants = Base.classes.participants
recall_trial=Base.classes.recall_trial
copy_trial=Base.classes.copy_trial
security=Base.classes.security
trials=Base.classes.trials


