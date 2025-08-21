# Docker UI
### Ever wished you could manage your docker containers from a simple web UI?
Now you can!

This project aims to simplify the workflow, when working with docker compose files / docker stacks.
Easily manage your containers, create compose files without writing a single line of code (WiP) or just change a deployment and all of that just in your browser.

The entire project is developed from the ground up, using Fastapi, Svelte and the docker sdk at its core. It's designed in a modular manner making adding features fast and easy.

## Screenshots:
App Managment Screen             |  Details Screen
:-------------------------:|:-------------------------:
![App Managment Screen](https://test-ui.wilu.lan64.de/screenshots/apps.png) | ![Details Screen](https://test-ui.wilu.lan64.de/screenshots/details.png)
Configuration Menu | Container Screen
![Configuration Menu](https://test-ui.wilu.lan64.de/screenshots/git.png) | ![Container Screen](https://test-ui.wilu.lan64.de/screenshots/details2.png)

## Features:
- [x] Advanced Permission System
- [x] Notification System
- [x] See Running Docker Compose Files / Apps
- [x] Inspect Apps
- [x] See Docker logs
- [x] Swagger UI endpoint

## Work in Progress:
- [ ] App Creation Wizard
- [ ] Manual App Creation

## Planned:
- Container view
- Settings and Account page
- Git integration for stack deployments
- Docker Swarm integration

**Try the demo yourself: https://test-ui.wilu.lan64.de**

Notice: I run the servers myself, I apologize for any service disruptions.

## Installation:
### Install with Docker:
Image: [Docker Hub](https://hub.docker.com/repository/docker/wilu2301/docker-ui/general)

**1. Create a docker stack file**

docker-ui.yaml:
```yaml
services:
  ui:
    image: wilu2301/docker-ui:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /usr/bin/docker:/usr/bin/docker:ro
    restart: always
    ports:
      - 9000:9000
```

**2.Run the stack**

```bash
docker stack deploy --compose-file docker-ui.yml docker-ui
```



Made with 💙 by wilu

