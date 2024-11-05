To run this server application, you need [PHP](https://www.php.net/manual/en/install.php){:target="\_blank"} and [Composer](https://getcomposer.org/download/){:target="\_blank"} installed on your device.

1. Navigate into the server directory
```bash
cd openvidu-livekit-tutorials/application-server/php
```
2. Install dependencies
```bash
composer install
```
3. Run the application
```bash
composer start
```

!!! warning

    LiveKit PHP SDK requires library [BCMath](https://www.php.net/manual/en/book.bc.php){:target="\_blank"}. This is available out-of-the-box in PHP for Windows, but a manual installation might be necessary in other OS. Run **`sudo apt install php-bcmath`** or **`sudo yum install php-bcmath`**
