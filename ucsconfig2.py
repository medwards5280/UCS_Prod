
#import ucsmsdk
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.org.OrgOrg import OrgOrg
from ucsmsdk.mometa.compute import ComputeChassisDiscPolicy
from ucsmsdk.mometa.cpmaint.CpmaintMaintPolicy import CpmaintMaintPolicy
from ucsmsdk.mometa.fabric import FabricLanCloud
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.mometa.fabric.FabricEthLanPc import FabricEthLanPc
from ucsmsdk.mometa.fabric.FabricEthLanPcEp import FabricEthLanPcEp
from ucsmsdk.mometa.compute.ComputeChassisDiscPolicy import ComputeChassisDiscPolicy
from ucsmsdk.mometa.comm import CommDns
from ucsmsdk.mometa.comm.CommDnsProvider import CommDnsProvider
from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider
from ucsmsdk.mometa.comm.CommDateTime import CommDateTime
from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss
from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import BiosVfFrontPanelLockout
from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import BiosVfConsistentDeviceNameControl
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootSan import LsbootSan
from ucsmsdk.mometa.lsboot.LsbootSanCatSanImage import LsbootSanCatSanImage
from ucsmsdk.mometa.lsboot.LsbootSanCatSanImagePath import LsbootSanCatSanImagePath
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock
from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock
from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac
from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy
from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock
from ucsmsdk.mometa.fabric.FabricVsan import FabricVsan
from ucsmsdk.mometa.vnic.VnicSanConnTempl import VnicSanConnTempl
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef
from ucsmsdk.mometa.vnic.VnicEther import VnicEther
from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
from ucsmsdk.mometa.vnic.VnicFc import VnicFc
from ucsmsdk.mometa.fabric.FabricVCon import FabricVCon
from ucsmsdk.mometa.ls.LsPower import LsPower

import sys, random, threading, webbrowser
from flask import Flask, render_template, redirect, request
import shelve
shelve = shelve.open('ucsshelve')

def rangeexpand(txt):
    lst = []
    for r in txt.split(','):
        if '-' in r[1:]:
            r0, r1 = r[1:].split('-', 1)
            lst += range(int(r[0] + r0), int(r1) + 1)
        else:
            lst.append(str(r))
    return lst
	
def add(a,b):
	if a + b < 10:
		return a + b
	elif a + b == 10:
		return "A"
	elif a + b == 11:
		return "B"
	elif a + b == 12:
		return "C"		
	elif a + b == 13:
		return "D"
	elif a + b == 14:
		return "E"
	elif a + b == 15:
		return "F"

app = Flask(__name__)
@app.route('/configureucs', methods = ['POST'])
def configureucs():
	ipaddress = request.form['ipaddress']
	username = request.form['username']
	password = request.form['password']	
	shelve['ipaddress'] = ipaddress
	shelve['username'] = username
	shelve['password'] = password
	
	#Login to UCS
	handle = UcsHandle(ipaddress, username, password)
	handle.login()


	#Global Configuration Settings


	# DNS Configuration
	dnsserver = request.form['dnsserver']
	dnsserver2 = request.form['dnsserver2']
	if dnsserver != "":
		mo = CommDnsProvider(parent_mo_or_dn="sys/svc-ext/dns-svc", name=dnsserver)
		handle.add_mo(mo)
		handle.commit()
		
	if dnsserver2 != "":	
		mo = CommDnsProvider(parent_mo_or_dn="sys/svc-ext/dns-svc", name=dnsserver2)
		handle.add_mo(mo)
		handle.commit()
		
	#NTP Configuration
	ntpserver = request.form['ntpserver']
	if ntpserver != "":
		mo = CommNtpProvider(parent_mo_or_dn="sys/svc-ext/datetime-svc", name=ntpserver)
		handle.add_mo(mo)
		handle.commit()

	#Time Zone Configuration
	timezonex = request.form['timezone']
	mo = CommDateTime(parent_mo_or_dn="sys/svc-ext", timezone=timezonex)
	handle.add_mo(mo, True)
	handle.commit()

	# Uplink Ports
	uplinkrange = request.form['uplinkrange']
	uplinkChannelA = request.form['channelA']
	uplinkChannelB = request.form['channelB']
	
	# Configure Uplinks for Fabric A
	mo = FabricEthLanPc(parent_mo_or_dn="fabric/lan/A", port_id=uplinkChannelA)
	for x in rangeexpand(uplinkrange):	
		y = str(x)
		mo_1 = FabricEthLanPcEp(parent_mo_or_dn=mo, admin_state="enabled", auto_negotiate="yes",
		eth_link_profile_name="default", name="", port_id=y, slot_id="1")
		handle.add_mo(mo)
	handle.commit()
	
	# Configure Uplinks for Fabric B
	mo = FabricEthLanPc(parent_mo_or_dn="fabric/lan/B", port_id=uplinkChannelB)
	for x in rangeexpand(uplinkrange):	
		y = str(x)
		mo_1 = FabricEthLanPcEp(parent_mo_or_dn=mo, admin_state="enabled", auto_negotiate="yes",
		eth_link_profile_name="default", name="", port_id=y, slot_id="1")
		handle.add_mo(mo)
	handle.commit()

	# Create Chassis Discovery Policy
	mo = ComputeChassisDiscPolicy(parent_mo_or_dn="org-root", link_aggregation_pref="port-channel")
	handle.add_mo(mo, True)
	handle.commit()

	
	#Create Sub Organization
	OrgName = request.form['OrgName']
	shelve['OrgName'] = OrgName
	mo = OrgOrg(parent_mo_or_dn="org-root", name=OrgName)
	handle.add_mo(mo)
	handle.commit()
		
	# Create Maintenance Policy
	maintpolicyname = request.form['maintpolicy']
	shelve['maintpolicyname'] = maintpolicyname
	mo = LsmaintMaintPolicy(parent_mo_or_dn="org-root/org-" + OrgName, name=maintpolicyname, uptime_disr="user-ack")
	handle.add_mo(mo)
	handle.commit()

	# # Configure CIMC Management IPs

	cimc_name = request.form['cimc_name']	
	shelve['cimc_name'] = cimc_name
	cimc_start = request.form['cimc_start']
	cimc_end = request.form['cimc_end']
	cimc_mask = request.form['cimc_mask']	
	cimc_gw = request.form['cimc_gw']
	if cimc_name != "":
		mo = IppoolPool(parent_mo_or_dn="org-root/org-" + OrgName, name=cimc_name)
		mo_1 = IppoolBlock(parent_mo_or_dn=mo, def_gw=cimc_gw, r_from=cimc_start, subnet=cimc_mask, prim_dns=dnsserver, sec_dns=dnsserver2, to=cimc_end)
		handle.add_mo(mo)
		handle.commit()

	# # Configure VLANs
	vlanrange = request.form['vlanrange']
	for x in rangeexpand(vlanrange):		
		y = str(x)
		mo = FabricVlan(parent_mo_or_dn="fabric/lan", compression_type="included", default_net="no", id=y, mcast_policy_name="", name="VLAN" + y, policy_owner="local", pub_nw_name="", sharing="none")
		handle.add_mo(mo)
		handle.commit()
		
# # Create CDP Network Control Policy
	mo = NwctrlDefinition(parent_mo_or_dn="org-root/org-" + OrgName, cdp="enabled", name="Enable_CDP")
	mo_1 = DpsecMac(parent_mo_or_dn=mo, descr="", forge="allow", name="", policy_owner="local")
	handle.add_mo(mo)
	handle.commit()	

## Boot Policies and Storage Settings
	wwnnpoolnumber = 0
	wwpnpoolnumbera = 0
	wwpnpoolnumberb = 0
	LocalBootPolicyName = request.form['LocalBootPolicyName']
	CTLWWN1A = request.form['CTLWWN1A']
	CTLWWN2A = request.form['CTLWWN2A']
	CTLWWN1B = request.form['CTLWWN1B']	
	CTLWWN2B = request.form['CTLWWN2B']	
	shelve['LocalBootPolicyName'] = LocalBootPolicyName
	SanBootPolicyName = request.form['SanBootPolicyName']
	shelve['SanBootPolicyName'] = SanBootPolicyName
	if SanBootPolicyName != "":
		mo = LsbootPolicy(parent_mo_or_dn="org-root/org-" + OrgName, name=SanBootPolicyName)
		mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-remote", lun_id="0", order="1")
		mo_2 = LsbootSan(parent_mo_or_dn=mo, order="2")
		mo_2_1 = LsbootSanCatSanImage(parent_mo_or_dn=mo_2, type="primary", vnic_name="fc0")
		mo_2_1_1 = LsbootSanCatSanImagePath(parent_mo_or_dn=mo_2_1, type="primary", wwn=CTLWWN1A)
		mo_2_1_2 = LsbootSanCatSanImagePath(parent_mo_or_dn=mo_2_1, type="secondary", wwn=CTLWWN1B)
		mo_2_2 = LsbootSanCatSanImage(parent_mo_or_dn=mo_2, type="secondary", vnic_name="fc1")
		mo_2_2_1 = LsbootSanCatSanImagePath(parent_mo_or_dn=mo_2_2, type="primary", wwn=CTLWWN2A)
		mo_2_2_2 = LsbootSanCatSanImagePath(parent_mo_or_dn=mo_2_2, type="secondary", wwn=CTLWWN2B)
		mo_3 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-remote-cimc", lun_id="0", order="3")
		handle.add_mo(mo)
		handle.commit()
		
	if LocalBootPolicyName != "":
		mo = LsbootPolicy(parent_mo_or_dn="org-root/org-" + OrgName, name=LocalBootPolicyName)
		mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-remote", lun_id="0", order="1")
		mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="2")
		mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
		mo_2_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_2_1, order="2")
		mo_3 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-remote-cimc", lun_id="0", order="3")
		handle.add_mo(mo)
		handle.commit()		
	boottype = request.form['boot']
	if boottype == "SANBoot":
	
	if boottype == "LocalBoot":
	
	### Local Boot Settings		

	###SAN Boot Settings

	###Create WWNN Pool
		WWNPoolName = request.form['wwnnpoolname']
		shelve['WWNPoolName'] = WWNPoolName	
		WWNPoolName = WWNPoolName + os + TemplateType
		a = wwnnpoolnumber
		if a > 0:
			b = 1
		else:
			b = 0
		wwnnpoolnumber = add(a,b)
		wwnnpoolnumber = str(wwnnpoolnumber)
		
		mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-" + OrgName, name=WWNPoolName, purpose="node-wwn-assignment")
		mo_1 = FcpoolBlock(parent_mo_or_dn=mo, r_from="20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":00", to="20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF")
		handle.add_mo(mo)
		handle.commit()
		
		shelve['wwnnpoolnumber'] = wwnnpoolnumber		
		wwnnpoolnumber = int(wwnnpoolnumber)

	# #Create WWPN Pool for Fabric A
		WWPNPoolName = request.form['wwpnpoolname']
		shelve['WWPNPoolName'] = WWPNPoolName			
		WWPNPoolName = WWPNPoolName + os + TemplateType
		a = wwpnpoolnumbera
		if a > 0:
			b = 1
		else:
			b = 0	
		wwpnpoolnumbera = add(a,b)
		wwpnpoolnumbera = str(wwpnpoolnumbera)
		mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-" + OrgName, name=WWPNPoolName + "A")
		mo_1 = FcpoolBlock(parent_mo_or_dn=mo, r_from="20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00", to="20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF")
		handle.add_mo(mo)
		handle.commit()

		shelve['wwpnpoolnumbera'] = wwpnpoolnumbera	
		wwpnpoolnumbera = int(wwpnpoolnumbera)

	# #Create WWPN Pool for Fabric B
		a = wwpnpoolnumberb
		if a > 0:
			b = 1
		else:
			b = 0	
		wwpnpoolnumberb = add(a,b)
		wwpnpoolnumberb = str(wwpnpoolnumberb)
		mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-" + OrgName, name=WWPNPoolName + "B")
		mo_1 = FcpoolBlock(parent_mo_or_dn=mo, r_from="20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00", to="20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF")
		handle.add_mo(mo)
		handle.commit()
		shelve['wwpnpoolnumberb'] = wwpnpoolnumberb	
		wwpnpoolnumberb = int(wwpnpoolnumberb)			

		VSANA = request.form['VSANA']
		FCOEVSANA = request.form['FCOEA']
		VSANB = request.form['VSANB']
		FCOEVSANB = request.form['FCOEB']
		shelve["VSANA"] = VSANA
		shelve["VSANB"] = VSANB
		shelve["FCOEVSANA"] = FCOEVSANA
		shelve["FCOEVSANB"] = FCOEVSANB
		
		
	# # Create Fabric A VSAN		
		mo = FabricVsan(parent_mo_or_dn="fabric/san/A", fc_zone_sharing_mode="coalesce", fcoe_vlan=FCOEVSANA, id=VSANA, name=VSANA, policy_owner="local", zoning_state="disabled")
		handle.add_mo(mo)
		handle.commit()

	# # Create Fabric B VSAN
		mo = FabricVsan(parent_mo_or_dn="fabric/san/B", fc_zone_sharing_mode="coalesce", fcoe_vlan=FCOEVSANB, id=VSANB, name=VSANB, policy_owner="local", zoning_state="disabled")
		handle.add_mo(mo)
		handle.commit()

	# #Create vHBA Template Fabric A
		vHBATemplate = os + TemplateType
		mo = VnicSanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, ident_pool_name=WWPNPoolName + "A", name=vHBATemplate + "HBA_A", switch_id="A", templ_type="updating-template")
		mo_1 = VnicFcIf(parent_mo_or_dn=mo, name=VSANA)
		handle.add_mo(mo)
		handle.commit()

	# #Create vHBA Template Fabric B
		mo = VnicSanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, ident_pool_name=WWPNPoolName + "B", name=vHBATemplate + "HBA_B", switch_id="B", templ_type="updating-template")
		mo_1 = VnicFcIf(parent_mo_or_dn=mo, name=VSANB)
		handle.add_mo(mo)
		handle.commit()
	
	
# # Server Profile Settings (Mac Address Pools, BIOS, UUID, vNIC )
	os = request.form['os']
	TemplateType = request.form['TemplateType']
	if os == 'ESX':	
		MacPoolName = request.form['macpoolname']
		SiteID = request.form['siteid']
		DomainID = request.form['domainid']
		shelve['MacPoolName'] = MacPoolName
		shelve['SiteID'] = SiteID
		shelve['DomainID'] = DomainID
		
		macpoolnumberA = 0
		macpoolnumberB = 0
		UUIDPoolNumber = 0

		#Create BIOS Policy
		BiosPolicyName = request.form['bios']
		shelve['BiosPolicyName'] = BiosPolicyName
		mo = BiosVProfile(parent_mo_or_dn="org-root/org-" + OrgName, name=BiosPolicyName + os)
		mo_1 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="disabled")
		mo_2 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
		mo_3 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
		mo_4 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
		mo_5 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
		handle.add_mo(mo)
		handle.commit()
			
	# #Create Mac Addres Pool for VMware Management on Fabric A	

		a = macpoolnumberA
		if a > 0:
			b = 1
		else:
			b = 0	
		macpoolnumberA = add(a,b)
		macpoolnumberA = str(macpoolnumberA)
		mo = MacpoolPool(parent_mo_or_dn="org-root/org-" + OrgName, name=MacPoolName + "MGMT")
		mo_1 = MacpoolBlock(parent_mo_or_dn=mo, r_from="00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00", to="00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA +":FF")
		handle.add_mo(mo)
		handle.commit()
		shelve['macpoolnumberA'] = macpoolnumberA
		macpoolnumberA = int(macpoolnumberA)
		
	# #Create vNIC Template for VMware Managment Interface

		mgmtvnic =  os + TemplateType + "_MGMT"
		shelve['mgmtvnic'] = mgmtvnic
		vlanrange = request.form['vlanmgmt']
				
		mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, ident_pool_name=MacPoolName + "MGMT", name=mgmtvnic, switch_id="A-B", templ_type="updating-template", nw_ctrl_policy_name="Enable_CDP")
		mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name=vlanrange)
		handle.add_mo(mo, True)
		handle.commit()
		
	# #Create Mac Addres Pool for vMotion on  Fabric B
		a = macpoolnumberB
		if a > 0:
			b = 1
		else:
			b = 0		
		macpoolnumberB = add(a,b)
		macpoolnumberB = str(macpoolnumberB)
		MacPoolNamevMotion = MacPoolName + "_vMotion"
		
		mo = MacpoolPool(parent_mo_or_dn="org-root/org-" + OrgName, name=MacPoolNamevMotion)
		mo_1 = MacpoolBlock(parent_mo_or_dn=mo, r_from="00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00", to="00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB +":FF")
		handle.add_mo(mo)
		handle.commit()

	# #Create vNIC Template for VMware vMotion 
		motionvnic = os + TemplateType + "_vMotion"
		shelve['motionvnic'] = motionvnic
		vlanrange = request.form['vlanmotion']		
		mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, ident_pool_name=MacPoolNamevMotion, name=motionvnic, switch_id="B-A", templ_type="updating-template", nw_ctrl_policy_name="Enable_CDP")
		mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name=vlanrange)
		handle.add_mo(mo, True)
		handle.commit()

		shelve['macpoolnumberB'] = macpoolnumberB	
		macpoolnumberB = int(macpoolnumberB)	
			

	# #Create Mac Addres Pool for VMware Data Interfaces - Fabric A

		a = macpoolnumberA
		b = 1
		macpoolnumberA = add(a,b)		
		macpoolnumberA = str(macpoolnumberA)
		MacPoolNameESX = MacPoolName + TemplateType
		
		mo = MacpoolPool(parent_mo_or_dn="org-root/org-" + OrgName, name=MacPoolNameESX + "A")
		mo_1 = MacpoolBlock(parent_mo_or_dn=mo, r_from="00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00", to="00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA +":FF")
		handle.add_mo(mo)
		handle.commit()

		shelve['macpoolnumberA'] = macpoolnumberA
		macpoolnumberA = int(macpoolnumberA)
		
	# #Create Mac Addres Pool for VMware Data Interfaces - Fabric B

		a = macpoolnumberB
		b = 1
		macpoolnumberB = add(a,b)
		macpoolnumberB = str(macpoolnumberB)

		mo = MacpoolPool(parent_mo_or_dn="org-root/org-" + OrgName, name=MacPoolNameESX + "B")
		mo_1 = MacpoolBlock(parent_mo_or_dn=mo, r_from="00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00", to="00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB +":FF")
		handle.add_mo(mo)
		handle.commit()

		shelve['macpoolnumberB'] = macpoolnumberB	
		macpoolnumberB = int(macpoolnumberB)

	# #vNIC Template

	# # Create vNIC Template for VMware Data Interfaces

		datavnic = os + TemplateType
		mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, ident_pool_name=MacPoolNameESX + "A", name=datavnic + "A", switch_id="A", templ_type="updating-template", nw_ctrl_policy_name="Enable_CDP")
		handle.add_mo(mo, True)
		handle.commit()

		mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, ident_pool_name=MacPoolNameESX + "B", name=datavnic + "B", switch_id="B", templ_type="updating-template", nw_ctrl_policy_name="Enable_CDP")
		handle.add_mo(mo, True)
		handle.commit()

		# #Add VLANs for vNIC template 

		vlanrange = request.form['vlandata']

		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, name=datavnic + "A")
			mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="VLAN" + y)
			handle.add_mo(mo, True)
			handle.commit()

		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-" + OrgName, name=datavnic + "B")
			mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="VLAN" + y)
			handle.add_mo(mo, True)	
			handle.commit()		

	# # Create UUID Pool
		UUIDPoolName = request.form['uuidpoolname']
		UUIDPoolName = UUIDPoolName + os + TemplateType
		a = UUIDPoolNumber
		if a > 0:
			b = 1
		else:
			b = 0	
		UUIDPoolNumber = add(a,b)
		UUIDPoolNumber = str(UUIDPoolNumber)
		mo = UuidpoolPool(parent_mo_or_dn="org-root/org-" + OrgName, name="UUID")
		mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, r_from="0000-000000000001", to="0000-000000000100")
		handle.add_mo(mo)
		handle.commit()
		

		shelve['UUIDPoolNumber'] = UUIDPoolNumber
		shelve['UUIDPoolName'] = UUIDPoolName
		UUIDPoolNumber = int(UUIDPoolNumber)	

	# # Create Service Profle Template

		TemplateName = os + TemplateType + "_SANBoot"
		mo = LsServer(parent_mo_or_dn="org-root/org-" + OrgName, bios_profile_name=BiosPolicyName, boot_policy_name=SanBootPolicyName, ext_ip_pool_name=cimc_name, ext_ip_state="pooled", ident_pool_name=UUIDPoolName, local_disk_policy_name="default", maint_policy_name=maintpolicyname, name=TemplateName, type="updating-template")
		mo_1 = VnicConnDef(parent_mo_or_dn=mo, san_conn_policy_name="")
		mo_2 = VnicEther(parent_mo_or_dn=mo, adaptor_profile_name="VMWare", name="Management", nw_templ_name=mgmtvnic, order="1", switch_id="A-B")
		mo_3 = VnicEther(parent_mo_or_dn=mo, adaptor_profile_name="VMWare", name="vMotion", nw_templ_name=motionvnic, order="2", switch_id="B-A")
		mo_4 = VnicEther(parent_mo_or_dn=mo, adaptor_profile_name="VMWare", name="DataA", nw_templ_name=datavnic + "A", order="3")
		mo_5 = VnicEther(parent_mo_or_dn=mo, adaptor_profile_name="VMWare", name="DataB", nw_templ_name=datavnic + "B", order="4", switch_id="B")
		mo_6 = VnicFcNode(parent_mo_or_dn=mo, addr="pool-derived", ident_pool_name=WWNPoolName)
		mo_7 = VnicFc(parent_mo_or_dn=mo, adaptor_profile_name="VMWare", name="fc0", nw_templ_name=vHBATemplate + "HBA_A", order="5")
		mo_7_1 = VnicFcIf(parent_mo_or_dn=mo_7, name="default")
		mo_8 = VnicFc(parent_mo_or_dn=mo, adaptor_profile_name="VMWare", name="fc1", nw_templ_name=vHBATemplate + "HBA_A", order="6")
		mo_8_1 = VnicFcIf(parent_mo_or_dn=mo_8, name="default")
		mo_9 = FabricVCon(parent_mo_or_dn=mo, fabric="NONE", id="1", inst_type="auto", placement="physical", select="all", share="shared", transport="ethernet,fc")
		mo_10 = FabricVCon(parent_mo_or_dn=mo, fabric="NONE", id="2", inst_type="auto", placement="physical", select="all", share="shared", transport="ethernet,fc")
		mo_11 = FabricVCon(parent_mo_or_dn=mo, fabric="NONE", id="3", inst_type="auto", placement="physical", select="all", share="shared", transport="ethernet,fc")
		mo_12 = FabricVCon(parent_mo_or_dn=mo, fabric="NONE", id="4", inst_type="auto", placement="physical", select="all", share="shared", transport="ethernet,fc")
		mo_13 = LsPower(parent_mo_or_dn=mo, state="admin-up")
		handle.add_mo(mo)
		handle.commit()
		
	return render_template('templateconfig.html')

# @app.route('/configuremore', methods = ['POST'])
# def configuremore():

	# ipaddress = shelve['ipaddress']
	# username = shelve['username'] 
	# password = shelve['password']
	# SiteID = shelve['SiteID']
	# DomainID = shelve['DomainID']
	# OrgName = shelve['OrgName']
	# maintpolicyname = shelve['maintpolicyname']
	# BiosPolicyName = shelve['BiosPolicyName']
	# LocalBootPolicyName = shelve['LocalBootPolicyName']
	# SanBootPolicyName = shelve['SanBootPolicyName']
	# cimc_name = shelve['cimc_name']
	# WWNPoolName	= shelve['WWNPoolName'] 
	# WWPNPoolName =	shelve['WWPNPoolName']	
	
	# MacPoolName = shelve['MacPoolName']
	# macpoolnumberA = shelve['macpoolnumberA']
	# macpoolnumberB = shelve['macpoolnumberB']
	# wwpnpoolnumbera = shelve['wwpnpoolnumbera']
	# wwpnpoolnumberb = shelve['wwpnpoolnumberb']
	# wwnnpoolnumber = shelve['wwnnpoolnumber']
	
	# mgmtvnic = shelve['mgmtvnic']
	# motionvnic = shelve['motionvnic']
	# UUIDPoolName = 	shelve['UUIDPoolName'] 
	# UUIDPoolNumber = shelve['UUIDPoolNumber'] 
	
	# VSANA = shelve["VSANA"]
	# VSANB = shelve["VSANB"]
	# FCOEVSANA = shelve["FCOEVSANA"]
	# FCOEVSANB = shelve["FCOEVSANB"]

	
	# #Login to UCS
	# handle = UcsHandle()
	# handle.Login(ipaddress, username, password, noSsl=True, port=80, dumpXml=YesOrNo.FALSE)


	# #Global Configuration Settings

	# # Create Mac Address, WWN, WWPN and UUID Pools
	# os = request.form['os']
	# TemplateType = request.form['TemplateType']
	# if os == 'ESX':	

	# #Create Mac Addres Pool for VMware Management on Fabric A	

	# #Create Mac Addres Pool for Fabric A

		# a = int(macpoolnumberA)
		# if a > 0:
			# b = 1
		# else:
			# b = 0
		# macpoolnumberA = add(a,b)
		# macpoolnumberA = str(macpoolnumberA)
		# MacPoolNameESX = MacPoolName + TemplateType
		

		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		# mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 # "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "A", "Name":MacPoolNameESX + "A", "Descr":""})
		# mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA +":FF", "From":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00",
		 # "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "A/block-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":FF"})
		# handle.CompleteTransaction()
		# shelve['macpoolnumberA'] = macpoolnumberA
		# macpoolnumberA = int(macpoolnumberA)
		
	# #Create Mac Addres Pool for Fabric B

		# a = int(macpoolnumberB)
		# if a > 0:
			# b = 1
		# else:
			# b = 0
		# macpoolnumberB = add(a,b)
		# macpoolnumberB = str(macpoolnumberB)

		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		# mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 # "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "B", "Name":MacPoolNameESX + "B", "Descr":""})
		# mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF", "From":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00",
		 # "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "B/block-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF"})
		# handle.CompleteTransaction()
		# shelve['macpoolnumberB'] = macpoolnumberB	
		# macpoolnumberB = int(macpoolnumberB)

	# #vNIC Template

	# # Create vNIC Template for VMware Data Interfaces

		# datavnic = os + TemplateType
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		# mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "A",
		 # "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A", "QosPolicyName":"",
		 # "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 # "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":datavnic + "A", "SwitchId":"A"})
		# handle.CompleteTransaction()

		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		# mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "B",
		 # "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B", "QosPolicyName":"",
		 # "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 # "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":datavnic + "B", "SwitchId":"B"})
		# handle.CompleteTransaction()

		# #Add VLANs for vNIC template 

		# vlanrange = request.form['vlandata']
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		# mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "A",
		# "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A",
		 # "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 # "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"A"}, True)
		# for x in rangeexpand(vlanrange):		
			# y = str(x)
			# mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 # "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A/if-" + y}, True)
		# handle.CompleteTransaction()
			
		# handle.StartTransaction()	
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		# mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "B",
		# "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B",
		 # "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 # "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"B"}, True)
		# for x in rangeexpand(vlanrange):		
			# y = str(x)
			# mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 # "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B/if-" + y}, True)
		# handle.CompleteTransaction()
		

	# #Create WWNN Pool
		# WWNPoolName = WWNPoolName + os + TemplateType
		# a = int(wwnnpoolnumber)
		# b = 1

		# wwnnpoolnumber = add(a,b)
		# wwnnpoolnumber = str(wwnnpoolnumber)
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		# mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", 
		# "Purpose":"node-wwn-assignment","Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName, "Name":WWNPoolName})
		# mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":00",
		 # "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName + "/block-20:00:00:25:B5:" + SiteID + DomainID + ":FF" + wwnnpoolnumber + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF"})
		# handle.CompleteTransaction()
		# shelve['wwnnpoolnumber'] = wwnnpoolnumber		
		# wwnnpoolnumber = int(wwnnpoolnumber)

	# #Create WWPN Pool for Fabric A
		# WWPNPoolName = WWPNPoolName + os + TemplateType
		# a = int(wwpnpoolnumbera)
		# b = 1

		# wwpnpoolnumbera = add(a,b)
		# wwpnpoolnumbera = str(wwpnpoolnumbera)
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		# mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", "Purpose":"port-wwn-assignment",
		# "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName + "A", "Name":WWPNPoolName + "A"})
		# mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00",
		 # "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "A/block-20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF"})
		# handle.CompleteTransaction()
		# shelve['wwpnpoolnumbera'] = wwpnpoolnumbera	
		# wwpnpoolnumbera = int(wwpnpoolnumbera)

	# #Create WWPN Pool for Fabric B
		# a = int(wwpnpoolnumberb)
		# b = 1

		# wwpnpoolnumberb = add(a,b)
		# wwpnpoolnumberb = str(wwpnpoolnumberb)
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		# mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", "Purpose":"port-wwn-assignment",
		# "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "B", "Name":WWPNPoolName + "B"})
		# mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00",
		 # "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "B/block-20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF"})
		# handle.CompleteTransaction()
		# shelve['wwpnpoolnumberb'] = wwpnpoolnumberb	
		# wwpnpoolnumberb = int(wwpnpoolnumberb)			
		
	# # Create UUID Pool
		# UUIDPoolName = UUIDPoolName + os + TemplateType
		# a = int(UUIDPoolNumber)
		# b = 1

		# UUIDPoolNumber = add(a,b)
		# UUIDPoolNumber = str(UUIDPoolNumber)	
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' OrgName,"})
		# mo = handle.AddManagedObject(obj, "uuidpoolPool", {"Descr":"", "Prefix":"derived", "AssignmentOrder":"default",
		 # "Dn":"org-root/org-" + OrgName + "/uuid-pool-" + UUIDPoolName, "PolicyOwner":"local", "Name":UUIDPoolName})
		# mo_1 = handle.AddManagedObject(mo, "uuidpoolBlock", {"To":""  + SiteID + DomainID + "0" + UUIDPoolNumber + "-0000000000FF", "From":""  + SiteID + DomainID + "0" + UUIDPoolNumber + "-000000000001",
		 # "Dn":"org-root/org-" + OrgName + "/uuid-pool-" + UUIDPoolName + "/block-from-"  + SiteID + DomainID + "0" + UUIDPoolNumber + "-000000000001-to-"  + SiteID + DomainID + "0" + UUIDPoolNumber + "0-0000000000FF"})
		# handle.CompleteTransaction()

		# shelve['UUIDPoolNumber'] = UUIDPoolNumber			
		# UUIDPoolNumber = str(UUIDPoolNumber)	
		
	# #Create vHBA_Fabric A
		# vHBATemplate = os + TemplateType
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		# mo = handle.AddManagedObject(obj, "vnicSanConnTempl", {"StatsPolicyName":"default",
		 # "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "IdentPoolName": WWPNPoolName + "A",
		 # "MaxDataFieldSize":"2048", "TemplType":"initial-template",
		 # "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_A", "PinToGroupName":"", "Name":vHBATemplate + "HBA_A", "SwitchId":"A"})
		# mo_1 = handle.AddManagedObject(mo, "vnicFcIf", {"Name":VSANA, "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_A/if-default"}, True)
		# handle.CompleteTransaction()

	# #Create vHBA_Fabric B
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		# mo = handle.AddManagedObject(obj, "vnicSanConnTempl", {"StatsPolicyName":"default",
		 # "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "IdentPoolName": WWPNPoolName + "B",
		 # "MaxDataFieldSize":"2048", "TemplType":"initial-template",
		 # "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_B", "PinToGroupName":"", "Name":vHBATemplate + "HBA_B", "SwitchId":"B"})
		# mo_1 = handle.AddManagedObject(mo, "vnicFcIf", {"Name":VSANB, "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_B/if-default"}, True)
		# handle.CompleteTransaction()
		
	# # Create Service Profle Template
		# os = request.form['os']
		# TemplateType = request.form['TemplateType']
		# TemplateName = os + TemplateType
		# handle.StartTransaction()
		# obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		# mo = handle.AddManagedObject(obj, "lsServer", {"ResolveRemote":"yes", "MgmtFwPolicyName":"", 
		# "StatsPolicyName":"default", "HostFwPolicyName":"", "PowerPolicyName":"default", "Name":TemplateName, "IdentPoolName":UUIDPoolName,
		 # "BootPolicyName":"SANBoot", "UsrLbl":"", "ExtIPState":"pooled", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName,
		 # "KvmMgmtPolicyName":"", "BiosProfileName":BiosPolicyName, "DynamicConPolicyName":"",
		 # "VmediaPolicyName":"", "MaintPolicyName":maintpolicyname, "AgentPolicyName":"", "MgmtAccessPolicyName":"", "Type":"updating-template",
		 # "ExtIPPoolName":cimc_name, "Descr":"", "VconProfileName":"", "SolPolicyName":"", "Uuid":"0", "LocalDiskPolicyName":"default", "PolicyOwner":"local",
		 # "SrcTemplName":"", "ScrubPolicyName":""})
		# mo_1 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/assign-ethernet-vnic-" + mgmtvnic,
		 # "VnicName":mgmtvnic, "Transport":"ethernet", "AdminVcon":"any", "Order":"1"}, True)
		# mo_2 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + datavnic + "A",
		 # "VnicName":datavnic + "A", "Transport":"ethernet", "AdminVcon":"any", "Order":"2"}, True)
		# mo_3 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + datavnic + "B",
		 # "VnicName":datavnic + "B", "Transport":"ethernet", "AdminVcon":"any", "Order":"3"}, True)
		# mo_4 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + motionvnic,
		# "VnicName":motionvnic, "Transport":"ethernet", "AdminVcon":"any", "Order":"4"}, True)
		# mo_5 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-fc-vnic-fc0", "VnicName":"fc0",
		 # "Transport":"fc", "AdminVcon":"any", "Order":"5"}, True)
		# mo_6 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-fc-vnic-fc1", "VnicName":"fc1",
		 # "Transport":"fc", "AdminVcon":"any", "Order":"6"}, True)
		# mo_7 = handle.AddManagedObject(mo, "vnicEther", {"Order":"1", "Name":mgmtvnic, "IdentPoolName":"", "Mtu":"1500",
		 # "AdaptorProfileName":"VMWare", "SwitchId":"A-B", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 # "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + mgmtvnic, "AdminVcon":"any", "StatsPolicyName":"default", "NwCtrlPolicyName":"",
		 # "PinToGroupName":"", "NwTemplName":mgmtvnic})
		# mo_8 = handle.AddManagedObject(mo, "vnicEther", {"Order":"2", "Name":datavnic + "A", "IdentPoolName":"", "Mtu":"1500",
		 # "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 # "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + datavnic + "A", "AdminVcon":"any", "StatsPolicyName":"default",
		 # "NwCtrlPolicyName":"", "PinToGroupName":"", "NwTemplName":datavnic + "A"})
		# mo_9 = handle.AddManagedObject(mo, "vnicEther", {"Order":"3", "Name":datavnic + "B", "IdentPoolName":"", "Mtu":"1500",
		 # "AdaptorProfileName":"VMWare", "SwitchId":"B", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 # "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + datavnic + "B", "AdminVcon":"any", "StatsPolicyName":"default", "NwCtrlPolicyName":"",
		 # "PinToGroupName":"", "NwTemplName":datavnic + "B"})
		# mo_10 = handle.AddManagedObject(mo, "vnicEther", {"Order":"4", "Name":motionvnic, "IdentPoolName":"", "Mtu":"1500",
		 # "AdaptorProfileName":"VMWare", "SwitchId":"B-A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 # "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + motionvnic, "AdminVcon":"any", "StatsPolicyName":"default",
		 # "NwCtrlPolicyName":"", "PinToGroupName":"", "NwTemplName":motionvnic})
		# mo_11 = handle.AddManagedObject(mo, "vnicFc", {"Order":"5", "Name":"fc0", "AdminVcon":"any", "MaxDataFieldSize":"2048",
		 # "IdentPoolName":"", "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 # "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc0", "PersBind":"disabled", "StatsPolicyName":"default",
		 # "PersBindClear":"no", "PinToGroupName":"", "NwTemplName":vHBATemplate + "HBA_A"})
		# mo_11_1 = handle.AddManagedObject(mo_11, "vnicFcIf", {"Name":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc0/if-default"}, True)
		# mo_12 = handle.AddManagedObject(mo, "vnicFc", {"Order":"6", "Name":"fc1", "AdminVcon":"any", "MaxDataFieldSize":"2048",
		 # "IdentPoolName":"", "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 # "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc1", "PersBind":"disabled", "StatsPolicyName":"default",
		 # "PersBindClear":"no", "PinToGroupName":"", "NwTemplName":vHBATemplate + "HBA_B"})
		# mo_12_1 = handle.AddManagedObject(mo_12, "vnicFcIf", {"Name":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc1/if-default"}, True)
		# mo_13 = handle.AddManagedObject(mo, "vnicFcNode", {"IdentPoolName":WWPNPoolName, "Addr":"pool-derived",
		 # "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-node"}, True)
		# mo_14 = handle.AddManagedObject(mo, "lsPower", {"State":"admin-up", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/power"}, True)
		# mo_15 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 # "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-1", "Id":"1"}, True)
		# mo_16 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 # "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-2", "Id":"2"}, True)
		# mo_17 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 # "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-3", "Id":"3"}, True)
		# mo_18 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 # "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-4", "Id":"4"}, True)
		# handle.CompleteTransaction()
	return render_template('templateconfig.html')

		
@app.route("/")
def main():
	return render_template('index.html')
if __name__ == "__main__":
	app.run(debug=True)
	





