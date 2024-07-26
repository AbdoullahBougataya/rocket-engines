package main

import (
    "database/sql"
    "encoding/json"
    "fmt"
    _ "github.com/mattn/go-sqlite3"
    "log"
)

type Record struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func main() {
    db, err := sql.Open("sqlite3", "./your-database.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    rows, err := db.Query("SELECT id, name, email FROM your_table")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    var records []Record

    for rows.Next() {
        var record Record
        err := rows.Scan(&record.ID, &record.Name, &record.Email)
        if err != nil {
            log.Fatal(err)
        }
        records = append(records, record)
    }

    if err = rows.Err(); err != nil {
        log.Fatal(err)
    }
