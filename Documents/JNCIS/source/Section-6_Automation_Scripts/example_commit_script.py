"""
system {
    scripts {
        commit {
            file example_commit_script.py;
        }
        language python;
    }
}
"""
from junos import Junos_Configuration
import jcs


def main():
    root = Junos_Configuration

    if not(root.xpath("./protocols/isis")):
        jcs.emit_error("ISIS must be enabled")
    if not(root.xpath("./protocols/bgp")):
        jcs.emit_warning("BGP is not configured. Are you sure the config is correct?")
        jcs.syslog('daemon.error', "Warning config was committed with no BGP configuration stanza")


if __name__ == '__main__':
    main()
