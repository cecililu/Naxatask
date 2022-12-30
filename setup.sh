#!/bin/bash

: << 'COMMENT'
-- author   Naxa
-- detail   This script prepares project for local development and production environment.
COMMENT

function createEntrypoint {
    if [ $DEPLOY_TYPE -eq 2 ];
    then
        echo "Enter port for Web App:"
        read WEB_APP_PORT
        export WEB_APP_PORT=$WEB_APP_PORT
        export PROJECT_NAME=$PROJECT_NAME;
        echo "";

        cp -p docker-entrypoint.prod.sh entrypoint.sh;
        cp -p docker-compose.prod.yml docker-compose.yml;
        envsubst < docker-compose.yml | tee docker-compose.yml;
        cp -p uwsgi.ini uwsgi.$PROJECT_NAME.ini;
        envsubst < entrypoint.sh | tee entrypoint.sh;
    else
        cp -p docker-entrypoint.local.sh entrypoint.sh
        cp -p docker-compose.local.yml docker-compose.yml
    fi
}

function makeProject {
    cp -rp Dockerfile_sample Dockerfile
    cp -rp env_sample .env
    cp -rp pg_env_sample.txt .pg_env
    createEntrypoint
}

function makeGISProject {
    cp -rp requirements_gis.txt requirements.txt
    cp -rp apt_requirements_gis.txt apt_requirements.txt
    makeProject
}


function makeNonGISProject {
    cp -rp requirements_nongis.txt requirements.txt
    cp -rp apt_requirements_nongis.txt apt_requirements.txt
    makeProject
}

function readDeploymentType {
    echo "Please Choose the deployment type:";
    echo "   [1] Local";
    echo "   [2] Production";
    read DEPLOY_TYPE;

    if [ $DEPLOY_TYPE -eq 1 ];
    then
        echo "Preparing project for local development";
    elif [ $DEPLOY_TYPE -eq 2 ];
    then
        echo "Preparing project for Production";
    else
        echo "Bad deployment type input please choose 1 or 2.";
        exit 1;
    fi
    echo "";
}

function readProjectType {
    echo "Please Choose the project type:";
    echo "   [1] GIS";
    echo "   [2] NON-GIS";
    read PROJECT_TYPE;

    if [ $PROJECT_TYPE -eq 1 ];
    then
        echo "Preparing project as GIS";
        echo "";
        makeGISProject
    elif [ $PROJECT_TYPE -eq 2 ];
    then
        echo "Preparing project as Non-GIS";
        echo "";
        makeNonGISProject
    else
        echo "Bad project type input please choose 1 or 2.";
        exit 1;
    fi
    echo "";
}

function readProjectName {
    echo "Please give project a name:";
    read PROJECT_NAME;
    echo "";
}


readProjectName
readDeploymentType
readProjectType

echo "Boilerplate files generated please review following files:"
echo "  1. .env"
echo "  2. .pg_env"
echo "  3. docker-compose.yml"
echo "  4. entrypoint.sh"
echo 'run `docker compose up -d`'