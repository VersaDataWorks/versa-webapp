from addict import Dict
from versa_webapp.analytics_dashboard import actions


model = Dict()
model.session_id = "eggfry"
model.run_dir = "/tmp/tmp5gbgkb_2"
# actions.START_DBSESSION(model)
actions.CONNECT_DBSESSION(model)
