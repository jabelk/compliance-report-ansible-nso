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

# Custom compliance Report

ncs-make-package --service-skeleton python-and-template --action-example custom-compliance-report

