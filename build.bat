# AMD64
docker build -t maanex/wumpum:manifest-amd64 --build-arg ARCH=amd64/ .
docker push maanex/wumpum:manifest-amd64

# ARM32V7
docker build -t maanex/wumpum:manifest-arm32v7 --build-arg ARCH=arm32v7/ .
docker push maanex/wumpum:manifest-arm32v7

# ARM64V8
docker build -t maanex/wumpum:manifest-arm64v8 --build-arg ARCH=arm64v8/ .
docker push maanex/wumpum:manifest-arm64v8


# Create Manifest
docker manifest create maanex/wumpum:manifest-latest --amend maanex/wumpum:manifest-amd64 --amend maanex/wumpum:manifest-arm32v7 --amend maanex/wumpum:manifest-arm64v8


# Push
docker manifest push maanex/wumpum:manifest-latest
