    === "Linux"
        ```bash
        chmod 600 <PATH_TO_THE_KEY>/openvidu_private_ssh_key_<STACK_NAME>.pem
        ```
    === "Powershell"
        ```powershell
        $KeyPath = "<PATH_TO_THE_KEY>" &&
        icacls $KeyPath /inheritance:r &&
        icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
        ```
