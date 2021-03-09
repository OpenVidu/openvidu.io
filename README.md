# openvidu.io

The _openvidu.io_ web is generated with [Jekyll](https://jekyllrb.com/).

# Local development

- Clone _openvidu.io_ repository
```
https://github.com/OpenVidu/openvidu.io
```
- To locally preview the changes, you can execute the following command in the root folder of the repository (you need [Docker](https://store.docker.com/search?type=edition&offering=community) installed) and visit [`localhost:4000`](http://localhost:4000):

```
docker run --rm --volume=$PWD:/srv/jekyll -p 4000:4000 -it jekyll/jekyll:4.2.0 jekyll serve
```
(Run `fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p` to increase the number of files that can be monitored if any problem appears when running this docker container)

# Documentation

The _openvidu.io_ documentation is generated with [MkDocs](http://www.mkdocs.org).

**To add documentation go to [openvidu.io-docs project](https://github.com/OpenVidu/openvidu.io-docs)**
