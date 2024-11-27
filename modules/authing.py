import os
import dbus

def run_as_root(args):
    os.system(f"sudo sh -c 'cd {os.getcwd()}; /bin/python3 {args}'") 

def check_is_root(): # return true when user is root
    return os.getuid() == 0 

def polkit_authorization(): # useless.
    bus = dbus.SystemBus()
    polkit = bus.get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
    polkit_iface = dbus.Interface(polkit, dbus_interface='org.freedesktop.PolicyKit1.Authority')

    pid = os.getpid() 
    uid = os.getuid() 

    # build unix process subject
    subject = ('unix-process', {
        'pid': dbus.UInt32(pid, variant_level=1),
        'start-time': dbus.UInt64(0, variant_level=1), 
        'uid': dbus.UInt32(uid, variant_level=1)       
    })

    details = {}
    flags = dbus.UInt32(1) 
    cancellation_id = ''

    try:
        result = polkit_iface.CheckAuthorization(
            subject, "io.ppm.authentication", details, flags, cancellation_id
        )
        is_authorized = result[0]
        return is_authorized
    except dbus.DBusException as e:
        print(f"DBus Error: {e}")
        return False

def generate_policies(): # useless too.
    policy = """
<!-- ppm Authentication policies -->

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
  "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
  "http://www.freedesktop.org/standards/PolicyKit/1.0/policyconfig.dtd">
<policyconfig>
  <action id="io.ppm.authentication">
    <description>Modify system packages with ppm.</description>
    <message>Authentication is required to perform system package modifications.</message>
    <defaults>
      <!-- Default policies -->
      <allow_any>no</allow_any>           <!-- Block non-admin users -->
      <allow_inactive>yes</allow_inactive> <!-- Block inactive sessions -->
      <allow_active>auth_admin</allow_active> <!-- Allow only active admin sessions -->
    </defaults>
    <annotate key="org.freedesktop.policykit.exec.path">/usr/bin/ppm</annotate>
    <annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
  </action>
</policyconfig>"""

    with open("/usr/share/polkit-1/actions/io.ppm.authentication.policy", 'w') as f:
        f.write(policy)

