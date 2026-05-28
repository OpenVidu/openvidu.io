    === "Linux"
        ```bash
        chmod 600 <PATH_TO_THE_KEY>/openvidu_ssh_key_sn.pem
        ```
    === "Powershell"
        ```powershell
        $KeyPath = "<PATH_TO_THE_KEY>" &&
        icacls $KeyPath /inheritance:r &&
        icacls $KeyPath /grant:r "$($env:USERNAME):(R)"
        ```
