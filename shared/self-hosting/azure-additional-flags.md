### (Optional) Additional flags

Additional optional flags to pass to the OpenVidu installer (comma-separated, e.g., `--flag1=value, --flag2`).

=== "(Optional) Additional flags"

    Parameters in this section look like this:

    ![OpenVidu Meet credentials](../../../../assets/images/self-hosting/shared/azure-additional-flags.png)

    For example (optional), you can use `--force-utc-timezone` to force UTC as the timezone for OpenVidu. By default, OpenVidu uses the timezone configured on the host machine where it is installed. In general, UTC is recommended, and [Azure VMs already default to UTC](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync){:target="\_blank"}, so this flag is not usually necessary.