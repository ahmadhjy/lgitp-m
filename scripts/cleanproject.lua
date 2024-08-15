local lfs = require("lfs")

-- Function to delete a directory and its contents
local function delete_directory(path)
    for file in lfs.dir(path) do
        if file ~= "." and file ~= ".." then
            local file_path = path .. "/" .. file
            local attr = lfs.attributes(file_path)
            if attr.mode == "directory" then
                delete_directory(file_path)
            else
                os.remove(file_path)
            end
        end
    end
    lfs.rmdir(path)
end

-- Function to recursively search and delete specified directories
local function search_and_delete(root_path, target)
    for file in lfs.dir(root_path) do
        if file ~= "." and file ~= ".." then
            local file_path = root_path .. "/" .. file
            local attr = lfs.attributes(file_path)
            if attr.mode == "directory" then
                if file == target then
                    print("Deleting directory: " .. file_path)
                    delete_directory(file_path)
                else
                    search_and_delete(file_path, target)
                end
            end
        end
    end
end

-- Function to delete db.sqlite3 from the root of the folder
local function delete_db_file(root_path)
    local db_file = root_path .. "/db.sqlite3"
    if lfs.attributes(db_file) then
        print("Deleting file: " .. db_file)
        os.remove(db_file)
    else
        print("db.sqlite3 not found in the root folder")
    end
end

-- Main function
local function clean_project(root_path)
    -- Delete all migrations folders
    search_and_delete(root_path, "migrations")
    -- Delete all __pycache__ folders
    search_and_delete(root_path, "__pycache__")
    -- Delete db.sqlite3 from the root of the folder
    delete_db_file(root_path)
end

-- Define the root path of the project folder
local project_root_path = "../backend/"

-- Run the clean project function
clean_project(project_root_path)
