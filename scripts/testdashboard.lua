local http = require("socket.http")
local ltn12 = require("ltn12")
local json = require("dkjson")

local base_url = "http://localhost:8000/api"
local auth_url = "http://localhost:8000/users"

-- Utility function to make HTTP requests
local function make_request(url, method, headers, body)
    local response_body = {}
    local res, code, response_headers, status = http.request {
        url = url,
        method = method,
        headers = headers,
        source = body and ltn12.source.string(body),
        sink = ltn12.sink.table(response_body)
    }
    return table.concat(response_body), code, response_headers, status
end

-- Register User
local function register_user(username, password)
    local url = auth_url .. "/register/"
    local body = json.encode({username = username, password = password})
    local headers = {
        ["Content-Type"] = "application/json",
        ["Content-Length"] = #body
    }
    return make_request(url, "POST", headers, body)
end

-- Login User
local function login_user(username, password)
    local url = auth_url .. "/login/"
    local body = json.encode({username = username, password = password})
    local headers = {
        ["Content-Type"] = "application/json",
        ["Content-Length"] = #body
    }
    return make_request(url, "POST", headers, body)
end

-- Get Token from login response
local function get_token_from_login_response(response)
    local data = json.decode(response)
    return data.token
end

-- Get Supplier Activity Bookings
local function get_supplier_activity_bookings(token)
    local url = base_url .. "/supplier/bookings/"
    local headers = {
        ["Authorization"] = "Token " .. token
    }
    return make_request(url, "GET", headers)
end

-- Get Customer Activity Bookings
local function get_customer_activity_bookings(token)
    local url = base_url .. "/customer/bookings/"
    local headers = {
        ["Authorization"] = "Token " .. token
    }
    return make_request(url, "GET", headers)
end

-- Confirm Activity Booking
local function confirm_activity_booking(token, booking_id)
    local url = base_url .. "/supplier/bookings/" .. booking_id .. "/confirm/"
    local headers = {
        ["Authorization"] = "Token " .. token
    }
    return make_request(url, "POST", headers)
end

-- Confirm Payment
local function confirm_payment(token, booking_id)
    local url = base_url .. "/supplier/bookings/" .. booking_id .. "/confirm-payment/"
    local headers = {
        ["Authorization"] = "Token " .. token
    }
    return make_request(url, "POST", headers)
end

-- Testing the APIs
local function test_apis()
    -- Register a new user
    local register_response, register_code = register_user("testuser", "testpassword")
    print("Register Response: ", register_response, "Code: ", register_code)

    -- Login the user
    local login_response, login_code = login_user("testuser", "testpassword")
    print("Login Response: ", login_response, "Code: ", login_code)
    
    -- Get the token
    local token = get_token_from_login_response(login_response)
    print("Token: ", token)
    
    -- Get supplier activity bookings
    local supplier_bookings_response, supplier_bookings_code = get_supplier_activity_bookings(token)
    print("Supplier Bookings Response: ", supplier_bookings_response, "Code: ", supplier_bookings_code)

    -- Get customer activity bookings
    local customer_bookings_response, customer_bookings_code = get_customer_activity_bookings(token)
    print("Customer Bookings Response: ", customer_bookings_response, "Code: ", customer_bookings_code)

    -- Assuming booking_id is 1 for testing confirm endpoints
    local booking_id = 1

    -- Confirm activity booking
    local confirm_booking_response, confirm_booking_code = confirm_activity_booking(token, booking_id)
    print("Confirm Booking Response: ", confirm_booking_response, "Code: ", confirm_booking_code)

    -- Confirm payment
    local confirm_payment_response, confirm_payment_code = confirm_payment(token, booking_id)
    print("Confirm Payment Response: ", confirm_payment_response, "Code: ", confirm_payment_code)
end

-- Run the tests
test_apis()
