import webapp_framework as wf


@wf.UpdateAppStateAndUI
def LOAD_DATAMODEL(appstate, event_data):
    # appstate.active_datamodels.append()

    # TODO: this is where we actually call versa
    # to build an orm

    print(f"action.LOAD_DATAMODEL called {appstate}")
    wf.dupdate(appstate, "/loaded_datamodel", "newdatamodel")
    pass


wf.make_react(LOAD_DATAMODEL, wf.ReactTag_ModelUpdate)
