#!/bin/sh

ant compile
ant jar
ant clean
chmod +x *.jar
