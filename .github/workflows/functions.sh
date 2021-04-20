#!/usr/bin/bash

function _msg()
{
    echo -n "$(date +"[%Y-%m-%d %H:%M:%S.%3N]") $@"
    echo -e "\e[0m";
}

# Error messages, red text
function error()
{
    echo -en "\e[31m"
    _msg "$@"
}

# Warning messages, yellow text
function warning()
{
    echo -en "\e[33m"
    _msg "$@"
}

# Info messages, green text
function info()
{
    echo -en "\e[32m"
    _msg "$@"
}

# Debug messages, regular white text but only if debugging is enabled.
function debug()
{
    if [[ "${CI_DEBUG}" == "true" ]]
    then
        _msg "$@"
    fi
}
