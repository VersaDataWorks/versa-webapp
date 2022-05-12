from addict import Dict
from versa_webapp.analytics_dashboard import actions, cfg_actions


model = Dict()
model.dbsession.id = "eggfry"
#model.run_dir = "/tmp/tmp5gbgkb_2"
# actions.START_DBSESSION(model)
cfg_actions.exec_actions(
    cfg_actions.cfg_actions[("/dbsession/start", True)], model)
# actions.CONNECT_DBSESSION(model)
