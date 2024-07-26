package main

import (
    "database/sql"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
)

func main() {
    // Open the database connection
    database, err := sql.Open("sqlite3", "../db/database.db")
    if err != nil {
        fmt.Println("Error opening database:", err)
        return
    }
    defer database.Close()

    // Perform a query
    rows, err := database.Query("SELECT * FROM rocket_engines")
    if err != nil {
        fmt.Println("Error performing query:", err)
        return
    }
    defer rows.Close()
}
