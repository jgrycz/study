#! /bin/bash

APP_NAME="leds_and_buttons.py"
OUTPUT_FILE_PATH="/tmp/leds_and_buttons.log"

log() {
    echo  $*
}

fatal() {
    echo $*
    exit 1
}

usage() {
    cat << EOF
        usage: $(basename $0) [start|stop|restart]

        --help - prints this help and exits
        start - starts app
        stop - stops app
        restart - stops and start
        status - checks status

        examles:
            $(basename $0) start
            $(basename $0) stop
            $(basename $0) restart
            $(basename $0) status

EOF
}

is_app_running() {
    PID=$(pgrep -f $APP_NAME)
    RC=$?
    if [[ $RC != 0 ]]; then
        return 1
    else
        return 0
    fi
}

start_app() {
    if  is_app_running; then
        fatal "app $APP_NAME is already running, can not start another instance"
    fi
    log "starting app $APP_NAME"
    if [[ ! -f $APP_NAME ]]; then
        fatal "can not find app $APP_NAME"
    fi
    setsid nohup python $APP_NAME > $OUTPUT_FILE_PATH 2>&1 &
    log "app $APP_NAME has been started"
    log "waiting 3 seconds to check if app is stable"
    sleep 3

    if ! is_app_running; then
        fatal "app $APP_NAME has stopped working - something is wrong"
    fi
}

stop_app() {
    if ! is_app_running; then
        log "app $APP_NAME is not running, not need to stop it"
        return 0
    fi

    log "stoping app $APP_NAME"
    APP_PID=$(pgrep -f $APP_NAME)
    log "app $APP_NAME is running on $APP_PID"
    log "killing $APP_NAME"
    kill $APP_PID
    sleep 3

    if ! is_app_running; then
        log "app $APP_NAME has been stopped"
        return 0
    fi

    log "killing non gracefully $APP_NAME"
    kill -9 $PID
}

restart_app() {
    stop_app
    start_app
}

status_app() {
    log "checking app $APP_NAME status"
    if is_app_running; then
        APP_PID=$(pgrep -f $APP_NAME)
        log "app $APP_NAME is running with PID: $APP_PID"
    else
        log "app $APP_NAME is not running"
    fi
}

if [[ $# < 1 ]]; then
    fatal "too few arguments"
fi
if [[ $# > 1 ]]; then
    fatal "too many arguments"
fi

ACTION=
case $1 in
    -h|-help|--help )
        usage ;;
    start|stop|restart|status )
        ACTION=${1}_app ;;
    *)
        fatal "argument $1 is not handled" ;;
esac

$ACTION

