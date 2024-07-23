Running versa-webapp
^^^^^^^^^^^^^^^^^^^^
#. Start csv data server
   
.. code-block::
   python3 -m http.server --bind 192.168.0.114 9000

#. Start webserver and connect to invoke wp_csvdata_input_v2

.. code-block::

   cd /home/kabiraatmonallabs/Development/VersaDataWorks/versa-webapp/run_app
   uvicorn --host devboxchuwi --port 8000 --ssl-keyfile /home/kabiraatmonallabs/Execution/ofjustpy/server.key --ssl-certfile /home/kabiraatmonallabs/Execution/ofjustpy/server.crt --reload     --reload-dir ./ --reload-dir  /home/kabiraatmonallabs/Development/VersaDataWorks/chartjs-customizer-ofjustpy/src/chartjs_customizer  versa_webapp.wp_csvdata_input_v2:app


Execution flow
^^^^^^^^^^^^^^
#. Show webpage csvdata_input_v2
#. User inputs the url of csv data in textinput at `/csvinput/csvurl`
   - clicks `/csvinput/form`
   - invokes the REACTLOOP with `"/csvinput/panel", (csvurl, None)`

#. REACTLOOP :      /csvinput/panel
   - update uistate
   - update appstate
     /csvinput/url_and_content
   - invoke action
     - ANALYZE_CSV_CONTENT
       - GEN_CSV_METADATAREPORT
	 - update appstate
	   - appstate.metadata_report
	   - appstate.metadata_edits
	   - appstate.op_status
	   - appstate.op
   #. Run the sub-REACTLOOP
      - collect appstate changes
	- /op, /op_status, etc.
      - run actions
	- SET_REDIRECT
	  - which creates the endpoint and
	    redirects to /csv_schema_metadata
	    
#. Show webpage /csv_schema_metadata
   - computed metadata is displayed
   - user inputs schema modifications
   - clicks the /gencsvcfg_form
   - invokes the REACTLOOP with `"/csv_schema_metadata/gencsvcfg_panel",  res`

     
#. REACTLOOP: `/csv_schema_metadata/gencsvcfg_panel`
   - update uistate
   - update appstate
     - /csv_schema_metadata/gencsvcfg_panel
   - invoke actions
     - CSV_METADATA_AS_XML
       - update appstate
	 - appstate.op_status
	 - appstate.op
#. Run the sub-REACTLOOP
   - collect appstate changes
     - /op = "CSV_METADATA_AS_XML"
     - /op_status, etc.
   - run actions
     - SET_REDIRECT
       - which creates and saves the endpoint
	 

   - TBD

Vocabulary
----------
#. csv_datamodel_label
   - would go into schem_xdef: `<model>??csv_datamodel_label??</model>`

     
#. metadata_fn/edcfg.schema_xfn
   - `csv_datamodel_label + ".md"`

     
#. schema_xdef

   .. code-block::

      <?xml version="1.0" ?>
      <metadata>       
                 
        <model>dummy_model</model>

        <delimiter>comma</delimiter>

        <columns>

                <column>
                        <name>col0</name>
                        <type>string</type>
                </column>

                <column>
                        <name>col1</name>
                        <type>int</type>
                </column>

                <column>
                        <name>col2</name>
                        <type>int</type>
                </column>

        </columns>

        <primarykey>
	</primarykey>

	</metadata>

#. schema_xelem   
   schema_xelem: <Element 'file' at 0x1a8f97a1350>
   .. code-block::
       <?xml version="1.0" ?>
      <file>
	      <location>./51a3b0789c97a.html</location>
	      <metadata>dummy_model.md</metadata>
	      <model_name>dummy_model</model_name>
	      <filetype>
		      <filetype>csv</filetype>
		      <strict_formatted>True</strict_formatted>
		      <delimiter>comma</delimiter>
		      <crop_head>0</crop_head>

	      </filetype>
      </file>


#. dpcfg_xelem

   .. code-block:: xml

      <?xml version="1.0" ?>
      <edconfig>
	      <files>
		      <file>
			      <location>./51a3b0789c97a.html</location>
			      <metadata>dummy_model.md</metadata>
			      <model_name>dummy_model</model_name>
			      <filetype>
				      <filetype>csv</filetype>
				      <strict_formatted>True</strict_formatted>
				      <delimiter>comma</delimiter>
				      <crop_head>0</crop_head>

			      </filetype>
		      </file>
	      </files>
      </edconfig>


#. edcfg.dpcfg_xfn
   - appstate.save_csvpack.model_name + ".csvpack"



#. xistr
  .. code-block:: xml
     
     <xi:include href="dummy_model.csvpack" parse="xml"/>
     
#. model_name

schema_xdef -- the metadata description
metadata_
   
Building the csv metadata content
---------------------------------
#. Consists of two files
   - the metadata file
     - dummy_model.md
   - the edcfg file
     - dummy_model.csvpack
     
