package main

import (
	"database/sql"
	"fmt"
	"github.com/mattn/go-sqlite3"
)

func main()
{
	database, err := sql.Open("sqlite3", "../db/database.db")
	if err != nil {
        fmt.Println("Error opening database:", err)
        return
    }
    defer database.Close()

	rows, err := database.Query("SELECT Id, Engine FROM rocket_engines")
    if err != nil {
        fmt.Println("Error performing query:", err)
        return
    }
    defer rows.Close()

	for rows.Next() {
        var id int
        var engine string
        err = rows.Scan(&id, &engine)
        if err != nil {
            fmt.Println("Error scanning row:", err)
            return
        }
        fmt.Printf("ID: %d, Engine: %s\n", id, engine)
    }

    err = rows.Err()
    if err != nil {
        fmt.Println("Error during iteration:", err)
    }
	// ChatGPT was here.
}
