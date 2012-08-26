#!/bin/bash

# TODO Add client-side environment set
PUBLIC_STUDENT="public-student"
URL="http://localhost/lessons"
#URL="http://www.myelinprice.com/lessons"

git clone $URL/$PUBLIC_STUDENT/$1/$2.git
