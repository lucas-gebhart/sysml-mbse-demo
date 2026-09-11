from pathlib import Path

import pytest

from sysml_demo.ingest import load
from sysml_demo.v2.profile import index_profile

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

TINY_XMI = """<?xml version='1.0' encoding='UTF-8'?>
<xmi:XMI xmlns:uml='http://www.omg.org/spec/UML/20131001' xmlns:xmi='http://www.omg.org/spec/XMI/20131001'
         xmlns:sysml='http://www.omg.org/spec/SysML/20181001/SysML'
         xmlns:Demo_Profile='https://example.org/Demo_Profile.xmi'>
  <xmi:Documentation><xmi:exporter>MagicDraw UML</xmi:exporter><xmi:exporterVersion>19.0</xmi:exporterVersion></xmi:Documentation>
  <uml:Model xmi:id='m' name='Tiny'>
    <packagedElement xmi:type='uml:Package' xmi:id='pkg' name='1 - Structure'>
      <packagedElement xmi:type='uml:Class' xmi:id='veh' name='Vehicle'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='veh_eng' name='engine' type='eng' aggregation='composite'>
          <lowerValue xmi:type='uml:LiteralInteger' xmi:id='lv1' value='1'/>
          <upperValue xmi:type='uml:LiteralUnlimitedNatural' xmi:id='uv1' value='2'/>
        </ownedAttribute>
        <ownedAttribute xmi:type='uml:Property' xmi:id='veh_mass' name='mass' type='real'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='veh_part' name='part' type='eng' aggregation='composite'/>
        <ownedAttribute xmi:type='uml:Port' xmi:id='veh_p' name='power in' type='pwr'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Class' xmi:id='eng' name='Engine'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='eng_pst' name='piston' type='pst' aggregation='composite'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='eng_veh' name='vehicle' type='veh'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Class' xmi:id='pst' name='Piston'/>
      <packagedElement xmi:type='uml:Class' xmi:id='pwr' name='PowerIF'/>
      <packagedElement xmi:type='uml:DataType' xmi:id='real' name='Real'/>
      <packagedElement xmi:type='uml:Class' xmi:id='orphan' name='Orphan'/>
      <packagedElement xmi:type='uml:Package' xmi:id='empty' name='Empty'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='reqs' name='2 - Requirements'>
      <packagedElement xmi:type='uml:Class' xmi:id='r1' name='Range'/>
      <packagedElement xmi:type='uml:Class' xmi:id='r2' name='Range'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='sat' client='veh' supplier='r1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='dangling' client='veh'>
        <supplier xmi:idref='nowhere'/>
      </packagedElement>
    </packagedElement>
  </uml:Model>
  <sysml:Block xmi:id='s1' base_Class='veh'/>
  <sysml:Block xmi:id='s2' base_Class='eng'/>
  <sysml:Block xmi:id='s10' base_Class='pst'/>
  <sysml:InterfaceBlock xmi:id='s3' base_Class='pwr'/>
  <sysml:Block xmi:id='s9' base_Class='orphan'/>
  <sysml:ValueType xmi:id='s4' base_DataType='real'/>
  <sysml:Requirement xmi:id='s5' base_Class='r1' Id='R-1' Text='The vehicle shall travel 500 km.'/>
  <sysml:Requirement xmi:id='s6' base_Class='r2' Id='R-2' Text=''/>
  <sysml:Satisfy xmi:id='s7' base_Abstraction='sat'/>
  <Demo_Profile:Vehicle xmi:id='s8' base_Class='veh' owner='ACME'/>
</xmi:XMI>
"""


@pytest.fixture(scope="session")
def tiny(tmp_path_factory):
    p = tmp_path_factory.mktemp("m") / "Tiny.xmi"
    p.write_text(TINY_XMI)
    return load(p)


@pytest.fixture(scope="session")
def csrm():
    return load(MODELS / "CSRM.mdzip")


@pytest.fixture(scope="session")
def csrm_profile():
    return index_profile(load(MODELS / "CSRM-Profile.mdzip"))


@pytest.fixture(scope="session")
def dels():
    return load(MODELS / "DELS.xml")
