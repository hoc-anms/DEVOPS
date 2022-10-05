"""
event-options {
    policy EBGP_DOWN {
        events rpd_bgp_neighbor_state_changed;
        attributes-match {
            rpd_bgp_neighbor_state_changed.peer-name matches 10.0.12.2;
        }
        then {
            event-script example_event_script.py;
        }
    }
    event-script {
        file example_event_script.py {
            python-script-user netconf;
        }
    }
}
"""
from junos import Junos_Context
from junos import Junos_Trigger_Event
from lxml import etree


def main():
    with open("/var/tmp/event_script_example.txt", 'a') as fh:
        fh.write("\nThis is an example event script output\n")
        fh.write("The context is:\n")
        fh.write(str(Junos_Context))
        fh.write("The XML data of the even is:\n")
        fh.write(etree.tostring(Junos_Trigger_Event))
        fh.write('=' * 60 + '\n')


if __name__ == '__main__':
    main()

