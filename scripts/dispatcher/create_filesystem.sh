ROOT="/tmp/cs/risk"
APP_DIR=${ROOT}"/app/mars/releases"
ENVS="FT11 FT12 FT13 LT11 LT12 LT13"
VERSIONS="18.2.0 18.3.0 18.3.5"

set -e

log (){
    echo "  $(date '+%F %T.%3N') $@"
}

clean_filesystem (){
    log "Removing $ROOT"
    rm -rf $ROOT 2> /dev/null
}

create_envs (){
    log "Creating app dir: $APP_DIR"
    mkdir -p "$APP_DIR"
    for ENV in $ENVS; do
        log "Working on $ENV"
        ENV_PATH="${APP_DIR}/${ENV}"
        log "Creating $ENV_PATH"
	    mkdir "$ENV_PATH"
        for VER in $VERSIONS; do
            log "Creating ${ENV_PATH}/${VER}"
            mkdir "${ENV_PATH}/${VER}"
            create_version_files "${ENV_PATH}/${VER}"
        done
    done
}

create_symlinks (){
    log "Creating symlinks"
    for ENV in $ENVS; do
        log "Linking 18.3.5 as latest in $ENV"
        ln -s "${APP_DIR}/${ENV}/18.3.5" "${APP_DIR}/${ENV}/latest"
    done

    log "Linking FT13 as last_distributed"
    ln -s "${APP_DIR}/FT13" "${APP_DIR}/last_distributed"
}

create_version_files (){
    MARS_PATH=$1
    log "Touching ${MARS_PATH}/.bin_version"
    touch ${MARS_PATH}/.bin_version
    echo "$(basename ${MARS_PATH}).14" > ${MARS_PATH}/.bin_version

    log "Touching ${MARS_PATH}/.cfg_version"
    touch ${MARS_PATH}/.cfg_version
    echo "$(basename ${MARS_PATH}).13-xml" > ${MARS_PATH}/.cfg_version
}

create_3rd_party_versions (){
    log "Touching ${APP_DIR}/../.3rd_party_version file"
    touch ${APP_DIR}/../.3rd_party_version
    echo "45678" > ${APP_DIR}/../.3rd_party_version

    log "Touching ${APP_DIR}/../.3rd_party_scripts_version file"
    touch ${APP_DIR}/../.3rd_party_scripts_version
    echo "18.3.5.1" > ${APP_DIR}/../.3rd_party_scripts_version
}

clean_filesystem
create_envs
create_symlinks
create_3rd_party_versions
