#import webapp_framework as wf
import ofjustpy_react as ojr
# This action requires updating the appstate and the ui


@ojr.UpdateAppStateAndUI
def LOAD_DATAMODEL(appstate, event_data):
    # appstate.active_datamodels.append()

    # TODO: this is where we actually call versa
    # to build an orm

    print(f"action.LOAD_DATAMODEL called {appstate}")
    ojr.dupdate(appstate, "/loaded_datamodel", "newdatamodel")
    pass


ojr.make_react(LOAD_DATAMODEL, ojr.ReactTag_AppstateUpdate)
