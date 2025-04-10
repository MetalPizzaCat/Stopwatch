#!/bin/sh

[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

cp -r dist/goblinstopwatch package/opt/goblinstopwatch
cp stopwatch_icon.svg package/usr/share/icons/hicolor/scalable/apps/goblinstopwatch.svg
cp goblinstopwatch.desktop package/usr/share/applications

# Change permissions
find package/opt/goblinstopwatch -type f -exec chmod 644 -- {} +
find package/opt/goblinstopwatch -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/goblinstopwatch/goblinstopwatch

rm -f goblinstopwatch.deb
fpm 