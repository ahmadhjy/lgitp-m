-- Lua script to test Django APIs using the http module
local http = require("socket.http")
local ltn12 = require("ltn12")
local json = require("dkjson")

-- Helper function to send HTTP requests
local function send_request(method, url, body, headers)
    local response_body = {}
    local req_body = body and json.encode(body) or nil
    local req_headers = headers or {}
    if body then
        req_headers["Content-Type"] = "application/json"
        req_headers["Content-Length"] = tostring(#req_body)
    end

    local res, code, response_headers, status = http.request {
        method = method,
        url = url,
        source = req_body and ltn12.source.string(req_body) or nil,
        headers = req_headers,
        sink = ltn12.sink.table(response_body)
    }

    return table.concat(response_body), code, response_headers, status
end

-- Base URL for the API
local base_url = "http://localhost:8000"

---- Step 1: Register a new customer account
--local register_url = base_url .. "/users/register/"
--local register_body = {username = "testcustomer", password = "testpass123", email = "testcustomer@example.com", is_customer=true, is_supplier=false}
--local register_response, register_code = send_request("POST", register_url, register_body)
--
--print("Register Response code: " .. register_code)
--print("Register Response body: " .. register_response)
--
--if register_code ~= 201 then
--    print("Failed to register customer.")
--    os.exit(1)
--end
--
-- Step 2: Login as supplier
local login_url = base_url .. "/users/login/"
local supplier_login_body = {username = "w", password = "pa$$ed123"}
local supplier_login_response, supplier_login_code = send_request("POST", login_url, supplier_login_body)

print("Supplier Login Response code: " .. supplier_login_code)
print("Supplier Login Response body: " .. supplier_login_response)

if supplier_login_code ~= 200 then
    print("Failed to login as supplier.")
    os.exit(1)
end

local supplier_token = json.decode(supplier_login_response).token

-- Step 3: Login as customer
local customer_login_body = {username = "testcustomer", password = "testpass123"}
local customer_login_response, customer_login_code = send_request("POST", login_url, customer_login_body)

print("Customer Login Response code: " .. customer_login_code)
print("Customer Login Response body: " .. customer_login_response)

if customer_login_code ~= 200 then
    print("Failed to login as customer.")
    os.exit(1)
end

local customer_token = json.decode(customer_login_response).token

-- Helper function to get headers with token
local function get_headers(token)
    return {["Authorization"] = "Token " .. token}
end

-- Endpoints and their request data
local endpoints = {
    ["get_categories"] = {url = base_url .. "/api/categories/", method = "GET"},
    ["get_activities"] = {url = base_url .. "/api/activities/", method = "GET"},
    ["get_packages"] = {url = base_url .. "/api/packages/", method = "GET"},
    ["get_package_days"] = {url = base_url .. "/api/packagedays/1/", method = "GET"}, -- Adjust package_id as needed
    ["get_tours"] = {url = base_url .. "/api/tours/", method = "GET"},
    ["get_tour_days"] = {url = base_url .. "/api/tourdays/1/", method = "GET"}, -- Adjust tour_id as needed
    ["get_daily_periods"] = {url = base_url .. "/api/periods/1/2024-06-05/", method = "GET"}, -- Adjust activity_id and date as needed
    ["create_activity_booking"] = {url = base_url .. "/api/bookingactivity/", method = "POST", body = {period_id = 1}}, -- Adjust period_id as needed
    ["supplier_activity_bookings"] = {url = base_url .. "/api/supplier/bookings/", method = "GET"},
    ["customer_activity_bookings"] = {url = base_url .. "/api/customer/bookings/", method = "GET"},
    ["confirm_activity_booking"] = {url = base_url .. "/api/supplier/bookings/1/confirm/", method = "POST"}, -- Adjust booking_id as needed
    ["confirm_payment"] = {url = base_url .. "/api/supplier/bookings/1/confirm-payment/", method = "POST"}, -- Adjust booking_id as needed
    ["create_tour_booking"] = {url = base_url .. "/api/bookingtour/", method = "POST", body = {tourday_id = 1}}, -- Adjust tourday_id as needed
    ["create_package_booking"] = {url = base_url .. "/api/bookingpackage/", method = "POST", body = {package_id = 1, start_date = "2024-06-01"}}, -- Adjust package_id and start_date as needed
    ["supplier_packages_bookings"] = {url = base_url .. "/api/supplier/packagesb/", method = "GET"},
    ["supplier_tours_bookings"] = {url = base_url .. "/api/supplier/toursb/", method = "GET"},
    ["customer_tour_bookings"] = {url = base_url .. "/api/customer/toursb/", method = "GET"},
    ["customer_package_bookings"] = {url = base_url .. "/api/customer/packagesb/", method = "GET"},
    ["confirm_package_booking"] = {url = base_url .. "/api/supplier/package/1/confirm/", method = "POST"}, -- Adjust booking_id as needed
    ["confirm_tour_booking"] = {url = base_url .. "/api/supplier/tour/1/confirm/", method = "POST"}, -- Adjust booking_id as needed
    ["confirm_package_payment"] = {url = base_url .. "/api/supplier/package/1/confirm-payment/", method = "POST"}, -- Adjust booking_id as needed
    ["confirm_tour_payment"] = {url = base_url .. "/api/supplier/tour/1/confirm-payment/", method = "POST"} -- Adjust booking_id as needed
}

-- Test endpoints for both supplier and customer
for name, endpoint in pairs(endpoints) do
    print("Testing endpoint: " .. name)
    local headers = {}
    if name:match("supplier") or name:match("confirm") then
        headers = get_headers(supplier_token)
    else
        headers = get_headers(customer_token)
    end

    local response, code, response_headers, status = send_request(endpoint.method, endpoint.url, endpoint.body, headers)
    print("Response code: " .. code)
    print("Response body: " .. response)
end
