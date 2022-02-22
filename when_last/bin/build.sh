#!/bin/zsh

set -e

platform=$1

echo "creating"
briefcase create $platform

echo "building"
briefcase build $platform

if [ "$platform" = "macOS" ] || [ "$platform" = "" ]; then
  echo "signing for macOS"
  codesign --force --deep --sign - "macOS/app/When Last/When Last.app"
fi

echo "Updating"
briefcase update $platform

echo "Building installer"
briefcase package $platform --adhoc-sign
