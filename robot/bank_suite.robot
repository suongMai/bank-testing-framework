*** Settings ***
# Data-driven test suite: test data in robot/data/test_data.json
Documentation     XYZ Bank suite – Customer Deposit, Withdrawal, Manager Add Customer
Resource          resources/bank_resource.robot
Suite Setup       Open Bank Login Page
Suite Teardown    Close Browser

*** Variables ***
${TEST_DATA_FILE}    ${EXECDIR}${/}robot${/}data${/}test_data.json

*** Test Cases ***
Customer Deposit Success
    [Documentation]    Login as customer, deposit amount, check message and balance (data from JSON)
    [Tags]    customer    deposit    smoke    data_driven
    @{deposits}=    Get Deposit Test Data    ${TEST_DATA_FILE}
    FOR    ${customer_name}    ${amount}    IN    @{deposits}
        Run Deposit Test With Data    ${customer_name}    ${amount}
    END

Customer Withdrawal Success
    [Documentation]    Deposit then withdraw, check message and balance (data from JSON)
    [Tags]    customer    withdrawal    smoke    data_driven
    @{withdrawals}=    Get Withdrawal Test Data    ${TEST_DATA_FILE}
    FOR    ${customer_name}    ${deposit_amount}    ${withdraw_amount}    IN    @{withdrawals}
        Run Withdrawal Test With Data    ${customer_name}    ${deposit_amount}    ${withdraw_amount}
    END

Manager Add Customer Success
    [Documentation]    Login as manager, add customer, check alert (data from JSON)
    [Tags]    manager    add_customer    smoke    data_driven
    @{customers}=    Get Add Customer Test Data    ${TEST_DATA_FILE}
    FOR    ${first_name}    ${last_name}    ${post_code}    IN    @{customers}
        Run Add Customer Test With Data    ${first_name}    ${last_name}    ${post_code}
    END
