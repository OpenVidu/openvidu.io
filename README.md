# openvidu.io

The _openvidu.io_ web is generated with [Jekyll](https://jekyllrb.com/).

# Local development

- Clone _openvidu.io_ repository
```
https://github.com/OpenVidu/openvidu.io
```
- To locally preview the changes, you can execute the following command in the root folder of the repository (you need [Docker](https://store.docker.com/search?type=edition&offering=community) installed) and visit [`localhost`](http://localhost:80):

```
docker run -p 80:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

# Documentation

The _openvidu.io_ documentation is generated with [MkDocs](http://www.mkdocs.org).

**To add documentation go to [openvidu.io-docs project](https://github.com/OpenVidu/openvidu.io-docs)**
