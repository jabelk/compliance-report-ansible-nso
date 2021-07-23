# Compliance
git init
git add .
git commit -am "init"
user.name=jabelk
user.email=jabelk@cisco.com
git config --global user.email "jabelk@cisco.com"
git config --global user.name "jabelk"
git commit -am "init"
git branch -M main
git remote add origin https://github.com/jabelk/compliance-report-ansible-nso.git
git push -u origin main
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=360000000'

## Steps to reproduce


ansible-galaxy collection install cisco.nso

```
(py3venv) [developer@devbox compliance-report-ansible-nso]$ ansible-galaxy collection install cisco.nso
Process install dependency map
Starting collection install process
Installing 'cisco.nso:1.0.3' to '/home/developer/.ansible/collections/ansible_collections/cisco/nso'
(py3venv) [developer@devbox compliance-report-ansible-nso]$
```


developer@ncs(config)# devices device dist-rtr01 config banner motd
(<LINE>): This is a MOTD banner.
developer@ncs(config-config)# commit dry-run outformat xml
result-xml {
    local-node {
        data <devices xmlns="http://tail-f.com/ns/ncs">
               <device>
                 <name>dist-rtr01</name>
                 <config>
                   <banner xmlns="urn:ios">
                     <motd>This is a MOTD banner. </motd>
                   </banner>
                 </config>
               </device>
             </devices>
    }
}
developer@ncs(config-config)#


<banner xmlns="urn:ios">
    <motd>This is a MOTD banner. </motd>
</banner>


### Compliance report

devices template MOTD-BANNER
ned-id cisco-ios-cli-6.67
config
banner motd 
This is a MOTD abnner.
commit dry-run
commit


compliance reports report check-motd
compare-template MOTD-BANNER IOS-DEVICES
commit

compliance reports report check-motd run outformat xml

### via api report

curl -k --location --request POST 'https://10.10.20.49:443/restconf/data/tailf-ncs:compliance/reports/report=check-motd/run' \
--header 'Content-Type: application/yang-data+xml' \
--header 'Authorization: Basic YWRtaW46YWRtaW4=' \
--header 'Accept: application/yang-data+json' \
--header 'Authorization: Basic ZGV2ZWxvcGVyOkMxc2NvMTIzNDU=' \
--data '<input><outformat>html</outformat></input>'

ansible-galaxy collection install ansible.netcommon


build ansible using keypath
developer@ncs# show running-config compliance | display xpath
/compliance/reports/report[name='check-motd']/compare-template[template-name='MOTD-BANNER'][device-group='IOS-DEVICES']
developer@ncs# show running-config compliance | display restconf
/restconf/tailf-ncs:compliance/reports/report=check-motd/compare-template=MOTD-BANNER,IOS-DEVICES
developer@ncs# show running-config compliance | display keypath
/compliance/reports/report{check-motd}/compare-template{MOTD-BANNER IOS-DEVICES}


output from running compliance report:

{
    "changed": true,
    "invocation": {
        "module_args": {
            "input": {},
            "output_invalid": {},
            "output_required": {},
            "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "path": "/ncs:compliance/reports/report{check-motd}/run",
            "timeout": 300,
            "url": "https://10.10.20.49/jsonrpc",
            "username": "developer",
            "validate_certs": false,
            "validate_strict": false
        }
    },
    "output": {
        "compliance-status": "violations",
        "id": "3",
        "info": "Checking 3 devices and no services",
        "location": "https://localhost:443/compliance-reports/report_3_developer_1_2021-7-21T14:46:50:0.xml"
    }
}

Ansible  unable to use file module to open NSO's compliance report because it has unsafe characters in the filename breaking the path for ansible
```
changed: [localhost] => {
    "changed": true,
    "invocation": {
        "module_args": {
            "input": {},
            "output_invalid": {},
            "output_required": {},
            "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "path": "/ncs:compliance/reports/report{check-motd}/run",
            "timeout": 300,
            "url": "http://localhost:8080/jsonrpc",
            "username": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "validate_certs": false,
            "validate_strict": false
        }
    },
    "output": {
        "compliance-status": "violations",
        "id": "9",
        "info": "Checking 3 devices and no services",
        "location": "http://localhost:8080/compliance-reports/report_9_********_1_2021-7-22T16:11:38:0.xml"
    }
}

TASK [SET EXTRACTED PATH TO VAR] ****************************************************************************************
task path: /home/developer/compliance-report-ansible-nso/pb_compliance_report.yaml:32
ok: [localhost] => {
    "ansible_facts": {
        "compliance_status": "violations",
        "report_path": "~/nso-instance/state/compliance-reports/report_9_********_1_2021-7-22T16:11:38:0.xml"
    },
    "changed": false
}

TASK [DISPLAY PATH FOR LOG] *********************************************************************************************
task path: /home/developer/compliance-report-ansible-nso/pb_compliance_report.yaml:37
ok: [localhost] => {
    "changed": false,
    "report_path": "~/nso-instance/state/compliance-reports/report_9_********_1_2021-7-22T16:11:38:0.xml"
}

TASK [DISPLAY REPORT STATUS] ********************************************************************************************
task path: /home/developer/compliance-report-ansible-nso/pb_compliance_report.yaml:42
ok: [localhost] => {
    "changed": false,
    "compliance_status": "violations"
}

TASK [SET EXTRACTED PATH TO VAR] ****************************************************************************************
task path: /home/developer/compliance-report-ansible-nso/pb_compliance_report.yaml:47
[WARNING]: Unable to find '~/nso-instance/state/compliance-reports/report_9_********_1_2021-7-22T16:11:38:0.xml' in
expected paths (use -vvvvv to see paths)

File lookup using None as file
fatal: [localhost]: FAILED! => {
    "msg": "An unhandled exception occurred while running the lookup plugin 'file'. Error was a <class 'ansible.errors.AnsibleError'>, original message: could not locate file in lookup: ~/nso-instance/state/compliance-reports/report_9_********_1_2021-7-22T16:11:38:0.xml"
}
```
the file exists and is able to be opened, but cannot escape it

```
(py3venv) [developer@devbox compliance-report-ansible-nso]$ more ~/nso-instance/state/compliance-reports/report_7_admin_1_2021-7-22T16\:4\:13\:0.xml
<?xml version='1.0'?><article xmlns='http://docbook.org/ns/docbook' version='5.0'><articleinfo><modespec><![CDATA[reportc
ookie : g2gCbQAAAABtAAAACmNoZWNrLW1vdGQ=]]></modespec></articleinfo><info><title></title><pubdate>2021-7-22 16:4:13</pubd
ate><author><firstname>admin</firstname></author></info><sect1><title>Summary</title><para>Compliance result titled "" de
fined by report "check-motd"</para><para>Resulting in <command>violations</command></para><para>Checking 3 devices and no
 services</para><para>Produced 2021-7-22 16:4:13</para><para>From : Oldest available information</para><para>To : 2021-7-
22 16:4:13</para><sect2><title>Template discrepancies</title><sect3><title>MOTD-BANNER</title><para>Discrepancies in devi
ce</para><para>dist-rtr01</para><para>dist-rtr02</para><para>internet-rtr01</para></sect3></sect2></sect1><sect1><title>D
etails</title><sect2><title>Template discrepancies details</title><sect3><title>MOTD-BANNER</title><sect4><title>Device d
ist-rtr01</title><informalexample><screen><![CDATA[ config {
     banner {
+        motd "This is a MOTD abnner.";
     }
 }
]]></screen></informalexample></sect4><sect4><title>Device dist-rtr02</title><informalexample><screen><![CDATA[ config {
     banner {
+        motd "This is a MOTD abnner.";
     }
 }
]]></screen></informalexample></sect4><sect4><title>Device internet-rtr01</title><informalexample><screen><![CDATA[ confi
g {
     banner {
+        motd "This is a MOTD abnner.";
     }
 }
]]></screen></informalexample></sect4></sect3></sect2></sect1></article>
(py3venv) [developer@devbox compliance-report-ansible-nso]$
```




# Custom compliance Report

ncs-make-package --service-skeleton python-and-template --action-example custom-compliance-report

