# coding=UTF-8
import sys
import os
import re
import time
from jira import JIRA

#----------------------------------------------------------------------
def print_jira_status(jira, jql_open, jql_resolved, proj_name):

    all_proj_issues = jira.search_issues(jql_open)

    print ("{} Opening issues:".format(proj_name))
    A_Cout = 0
    B_Cout = 0
    C_Cout = 0
    pStr = 'X'

    for issue in all_proj_issues:
        pStr = str(issue.fields.priority)
        if(pStr == 'A'):
            A_Cout = A_Cout + 1
        elif(pStr == 'B'):
            B_Cout = B_Cout + 1
        elif(pStr == 'C'):
            C_Cout = C_Cout + 1
        # print "[%s] %s - %s assignee = %s" %(issue.fields.priority, issue, issue.fields.summary, issue.fields.assignee)
        print ("[{}] {} - {}".format(issue.fields.priority, issue, issue.fields.summary))


    print ("[Opening Issues] {}A {}B {}C ".format(A_Cout, B_Cout, C_Cout))

    all_proj_issues = jira.search_issues(jql_resolved)

    print ("\n{} Resolved issues:".format(proj_name))
    A_Cout = 0
    B_Cout = 0
    C_Cout = 0
    pStr = 'X'

    for issue in all_proj_issues:
        pStr = str(issue.fields.priority)
        if(pStr == 'A'):
            A_Cout = A_Cout + 1
        elif(pStr == 'B'):
            B_Cout = B_Cout + 1
        elif(pStr == 'C'):
            C_Cout = C_Cout + 1
        print ("[{}] {} - {} <{}>".format(issue.fields.priority, issue, issue.fields.summary, issue.fields.assignee))


    print ("[Resolved Issues] {}A {}B {}C ".format(A_Cout, B_Cout, C_Cout))


#----------------------------------------------------------------------
def search_auth_file(folder, auth_data, pass_data):
    print ("Target Path = {}".format(folder))
    p = re.compile(r'\[pass\]', re.IGNORECASE)
    a = re.compile(r'\[account\]', re.IGNORECASE)

    fp = open(folder,"r")
    zops = fp.readlines()
    for lineStr in zops:
        if(p.match(lineStr)):
            lineStr = lineStr.strip()
            pass_data.append(re.sub(p,r'',lineStr))

        if(a.match(lineStr)):
            lineStr = lineStr.strip()
            auth_data.append(re.sub(a,r'',lineStr))

    # print "pass = %s, account = %s" %(pass_data[0],auth_data[0])
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def connect_to_jira(auth, passw):
   jira_options = { 'server': 'http://partner-portal.vizio.com:85'}

   try:
       jira = JIRA(options=jira_options, basic_auth=(auth, passw))
   except Exception as e:
       jira = None

   return jira

#----------------------------------------------------------------------
def prasing_proj(jira_a, proj_s):
    print ("=============================================================")
    proj = proj_s
    jra = jira_a.project(proj)
    print ("Project name = " + (jra.name))                 # 'JIRA'
    print ("Project leader = " + (jra.lead.displayName))
    jql_open = 'project = ' + proj + ' AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
    jql_resolved = 'project = ' + proj + ' AND status = Resolved ORDER BY priority DESC, updated DESC'
    print_jira_status(jira_a,jql_open, jql_resolved, jra.name)
    print ("=============================================================")
