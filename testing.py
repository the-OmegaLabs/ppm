import os
import dbus

def check_authorization(action_id):
    bus = dbus.SystemBus()
    polkit = bus.get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
    polkit_iface = dbus.Interface(polkit, dbus_interface='org.freedesktop.PolicyKit1.Authority')

    # 使用当前进程的信息
    pid = os.getpid()  # 当前进程的 PID
    uid = os.getuid()  # 当前用户的 UID

    # 构造 Unix process subject
    subject = ('unix-process', {
        'pid': dbus.UInt32(pid, variant_level=1),
        'start-time': dbus.UInt64(0, variant_level=1),  # 通常设置为 0
        'uid': dbus.UInt32(uid, variant_level=1)       # 添加 UID
    })

    details = {}
    flags = dbus.UInt32(1)  # 1 表示允许用户交互
    cancellation_id = ''

    try:
        result = polkit_iface.CheckAuthorization(
            subject, action_id, details, flags, cancellation_id
        )
        is_authorized = result[0]
        return is_authorized
    except dbus.DBusException as e:
        print(f"DBus Error: {e}")
        return False

if __name__ == "__main__":
    action = "io.ppm.authentication"  # 替换为你要测试的 action
    if check_authorization(action):
        print("Authorized")
    else:
        print("Not Authorized")
