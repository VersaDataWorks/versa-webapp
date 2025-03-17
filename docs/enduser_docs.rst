#. start server to host files
   /home/kabiraatmonallabs/Databank/versa-dl/content
   

. ~/Execution/versadataworks/env.sh
. ~/Execution/versadataworks/venv/bin/activate

uvicorn --host devboxchuwi --port 8000 --ssl-keyfile /home/kabiraatmonallabs/Execution/ofjustpy/server.key --ssl-certfile /home/kabiraatmonallabs/Execution/ofjustpy/server.crt --reload     --reload-dir ./ --reload-dir  /home/kabiraatmonallabs/Development/VersaDataWorks/versa-webapp/versa_webapp  versa_webapp.wp_csvdata_input_v2:app

uvicorn --host devboxchuwi --port 8000 --ssl-keyfile /home/kabiraatmonallabs/Execution/ofjustpy/server.key --ssl-certfile /home/kabiraatmonallabs/Execution/ofjustpy/server.crt --reload     --reload-dir ./ --reload-dir  /home/kabiraatmonallabs/Development/VersaDataWorks/versa-webapp/versa_webapp  versa_webapp.wp_save_csvpack_v2:app

