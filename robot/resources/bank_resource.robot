*** Settings ***
# Shared resource – config from config.py (no CLI params)
Documentation     Shared resource for Bank test suite (Robot Framework)
Variables         ${EXECDIR}${/}config.py
Library           libs.robot_bank_library.BankingLibrary    ${BASE_URL}    ${BROWSER}    headless=${HEADLESS}
