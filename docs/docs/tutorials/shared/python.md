To run this server application, you need [Python 3](https://www.python.org/downloads/){:target="\_blank"} installed on your device.

1.  Navigate into the server directory

    ```bash
    cd openvidu-livekit-tutorials/application-server/python
    ```

2.  Create a python virtual environment

    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment

    === ":fontawesome-brands-windows:{.icon .lg-icon .tab-icon} Windows"

        ```powershell
        .\venv\Scripts\activate
        ```

    === ":simple-apple:{.icon .lg-icon .tab-icon} macOS"

        ```bash
        . ./venv/bin/activate
        ```

    === ":simple-linux:{.icon .lg-icon .tab-icon} Linux"

        ```bash
        . ./venv/bin/activate
        ```

4.  Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

5.  Run the application

    ```bash
    python app.py
    ```
