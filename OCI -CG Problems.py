#!/usr/bin/env python
# coding: utf-8

# In[39]:


##OCI Cloud Guard

import json
import csv
import io
from datetime import datetime

import oci
from oci.config import from_file

#constants
OCI_CONFIG_FILE_LOC = '<Provide Path to CONFIG File>'
OCI_CONFIG_PROFILE_NAME = 'DEFAULT'
OCI_COMPARTMENT_ID = '<Tenancy-OCID>'
OCI_CG_PROBLEM_SUMMARY_FILENAME = 'OCI-CG-ProblemSummary.xlsx'
OCI_CG_BUCKET_NAME = '<Pls-Provide Bucket Name>'
OCI_OBJ_STORAGE_NAMESPACE_NAME = '<Pls-Provide Bucket NameSpace>'
OCI_COMPARTMENT_SUBTREE = True
OCI_COMPARTMENT_ACCESSLEVEL = 'ACCESSIBLE'
OCI_PROBLEMS_LIMIT = 5000


# Using the default profile from a different file
config = from_file(file_location=OCI_CONFIG_FILE_LOC, profile_name=OCI_CONFIG_PROFILE_NAME)

#CG Client
cgClient = oci.cloud_guard.CloudGuardClient(config)

#get the OCI CG list of problems
problems = cgClient.list_problems(compartment_id = OCI_COMPARTMENT_ID,compartment_id_in_subtree=OCI_COMPARTMENT_SUBTREE,access_level=OCI_COMPARTMENT_ACCESSLEVEL,limit=OCI_PROBLEMS_LIMIT).data
cg_problems = problems.items
cg_probList = len(problems.items)
jsondata =  json.loads(str(cg_problems))
print(jsondata)

output = io.StringIO()
csv_writer = csv.writer(output)

count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())

data_file.close()

object_storage_client = oci.object_storage.ObjectStorageClient(config)
put_object_response = object_storage_client.put_object(namespace_name=OCI_OBJ_STORAGE_NAMESPACE_NAME,bucket_name=OCI_CG_BUCKET_NAME,object_name=OCI_CG_PROBLEM_SUMMARY_FILENAME,put_object_body=output.getvalue())

# Get the data from response
print(put_object_response.headers)

